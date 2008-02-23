import os
import sys
import ctypes
import pprint
import logging
import comtypes
import comtypes.client
from msdia_details import msdia

sys.path.append( r'../..' )
#sys.path.append( r'C:\dev\language-binding\pygccxml_dev' )

from pygccxml import utils
from pygccxml import declarations

import details


SymTagEnum = 12

def AsDiaSymbol( x ):
    return ctypes.cast( x, ctypes.POINTER( msdia.IDiaSymbol ) )


def print_files( session ):
    files = iter( session.findFile( None, '', 0 ) )
    for f in files:
        f = ctypes.cast( f, ctypes.POINTER(msdia.IDiaSourceFile) )
        print 'File: ', f.fileName


class pdb_reader_t(object):
    def __init__(self, pdb_file_path ):
        self.logger = utils.loggers.pdb_reader
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug( 'creating DiaSource object' )
        self.__dia_source = comtypes.client.CreateObject( msdia.DiaSource )
        self.logger.debug( 'loading pdb file: %s' % pdb_file_path )
        self.__dia_source.loadDataFromPdb(pdb_file_path)
        self.logger.debug( 'opening session' )
        self.__dia_session = self.__dia_source.openSession()
        self.logger.debug( 'opening session - done' )
        self.__global_ns = declarations.namespace_t( '::' )        
        self.__classes = {}
        self.__namespaces = {'': self.__global_ns}

        
    def read(self):
        self.__populate_scopes()
        
    @property
    def dia_global_scope(self):
        return self.__dia_session.globalScope

    @property
    def global_ns(self):
        return self.__global_ns
    
    def __find_udt( self, name ):
        self.logger.debug( 'testing whether name( "%s" ) is UDT symbol' % name )
        flags = msdia.NameSearchOptions.nsfCaseSensitive
        found = self.dia_global_scope.findChildren( msdia.SymTagUDT, name, flags )
        if found.Count == 1:                      
            self.logger.debug( 'name( "%s" ) is UDT symbol' % name )
            return AsDiaSymbol( found.Item(0) )
        elif 1 < found.Count:
            raise RuntimeError( "duplicated UDTs with name '%s', were found" % name )
            #~ self.logger.debug( 'name( "%s" ) is UDT symbol' % name )
            #~ return [AsDiaSymbol( s ) for s in  iter(found)]
            #~ for s in iter(found):
                #~ s = 
                #~ print s.name
                #~ print details.guess_class_type(s.udtKind)
        else:    
            self.logger.debug( 'name( "%s" ) is **NOT** UDT symbol' % name )            
            return None
    
    def __list_main_classes( self ):
        #in this context main classes, are classes that were defined within a namespace
        #as opposite to the classes defined in other classes
        classes = []
        dia_classes = self.dia_global_scope.findChildren( msdia.SymTagUDT, None, 0 )
        for dia_class in iter( dia_classes ):
            dia_class = AsDiaSymbol( dia_class )        
            name_splitter = details.get_name_splitter( dia_class.name )            
            for index, scope in enumerate( name_splitter.scope_names ):                
                if scope in self.__namespaces:
                    continue
                else:
                    udt = self.__find_udt( scope )
                    if udt:
                        classes.append( udt )
                        if index:
                            self.__namespaces[ name_splitter.scope_names[index-1] ] = None
                        break
                    else:
                        self.__namespaces[ scope ] = None
            else:
                classes.append( dia_class )
                if name_splitter.scope_names:
                    self.__namespaces[ name_splitter.scope_names[-1] ] = None
        return classes
    
    def __add_inner_classes( self, parent_class ):
        self.logger.debug( 'adding inner classes to "%s"' % parent_class.decl_string )
        for symbol_id in parent_class.dia_symbols:
            self.logger.debug( '\tdia symbol id: %d' % symbol_id )
            dia_symbol = self.__dia_session.symbolById( symbol_id )
            found = dia_symbol.findChildren( msdia.SymTagUDT, None, 0 )
            for inner_dia_class in iter(found):
                inner_dia_class = AsDiaSymbol( inner_dia_class )
                self.logger.debug( '\t\tinner UDT found - %s' % inner_dia_class.name )
                inner_name_splitter = details.get_name_splitter( inner_dia_class.name )
                try:
                    inner_klass = parent_class.class_( inner_name_splitter.name, recursive=False )
                    inner_klass.dia_symbols.add( inner_dia_class.symIndexId )
                except parent_class.declaration_not_found_t:
                    inner_klass = self.__create_class( inner_dia_class )
                    parent_class.adopt_declaration( inner_klass
                                                    , details.guess_access_type( inner_dia_class.access ) )
                    self.__classes[ inner_dia_class.name ] = inner_klass
        self.logger.debug( 'adding inner classes to "%s" - done' % parent_class.decl_string )                                             

    def __create_enum( self, enum_smbl ):
        name_splitter = details.get_name_splitter( enum_smbl.name )
        enum_decl = declarations.enumeration_t( name_splitter.name )
        values = enum_smbl.findChildren( msdia.SymTagData, None, 0 )
        for v in iter(values):
            v = AsDiaSymbol(v)
            if v.classParent.symIndexId != enum_smbl.symIndexId:
                continue
            enum_decl.append_value( v.name, v.value )
        if enum_decl.values:
            return enum_decl
        else:
            #for some reason same enum could appear under global namespace and 
            #under the class, it was defined in. This is a criteria I use to distinguish
            #between those cases
            return None

    def __add_enums( self, parent_symbol_id ):
        parent_symbol = self.__dia_session.symbolById( parent_symbol_id )
        self.logger.debug( 'adding enums to "%s" ' % parent_symbol.name )
        for enum_smbl in iter( parent_symbol.findChildren( SymTagEnum, None, 0 ) ):
            enum_smbl = AsDiaSymbol( enum_smbl )
            enum_decl = self.__create_enum( enum_smbl )            
            if not enum_decl:
                continue
            self.logger.debug( '\tfound %s' % str(enum_decl) )
            name_splitter = details.get_name_splitter( enum_smbl.name )
            if not name_splitter.scope_names:
                self.global_ns.adopt_declaration( enum_decl )
                self.logger.debug( '\tenum "%s" was added to global namespace' % enum_decl.name )
            else:
                try:
                    self.logger.debug( '\tadding enum "%s" to a namespace' % enum_decl.name )
                    ns = self.__namespaces[ name_splitter.scope_names[-1] ]
                    ns.adopt_declaration( enum_decl )
                    self.logger.debug( '\tadding enum "%s" to a namespace - done' % enum_decl.name )
                except KeyError:
                    self.logger.debug( '\tadding enum "%s" to a class' % enum_decl.name )
                    klass = self.__classes[ name_splitter.scope_names[-1] ]
                    klass.adopt_declaration( enum_decl, details.guess_access_type( enum_smbl.access ) )    
                    self.logger.debug( '\tadding enum "%s" to a class - done' % enum_decl.name )                    
        self.logger.debug( 'adding enums to "%s" - done' % parent_symbol.name )
        
    def __create_nss( self ):        
        nss = self.__namespaces.keys()
        nss.sort()
        
        for ns_name in nss:
            name_splitter = details.get_name_splitter( ns_name )
            if not name_splitter.scope_names:
                parent_ns = self.global_ns
            else:
                parent_ns = self.__namespaces[ name_splitter.scope_names[-1] ]
            ns_decl = declarations.namespace_t( name_splitter.name )
            parent_ns.adopt_declaration( ns_decl )
            self.__namespaces[ ns_name ] = ns_decl
    
    def __create_class( self, dia_class ):
        name_splitter = details.get_name_splitter( dia_class.name )
        klass = declarations.class_t( name_splitter.name )
        klass.class_type = details.guess_class_type(dia_class.udtKind)        
        klass.dia_symbols = set([dia_class.symIndexId])
        return klass
        
    def __populate_scopes(self):                
        main_classes = self.__list_main_classes()
        self.__create_nss()
        
        for dia_class in main_classes:
            name_splitter = details.get_name_splitter( dia_class.name )            
            if not name_splitter.scope_names:
                parent_ns = self.global_ns
            else:
                parent_ns = self.__namespaces[ name_splitter.scope_names[-1] ]
                
            try:                
                klass = parent_ns.class_( name_splitter.name, recursive=False )
                klass.dia_symbols.add( dia_class.symIndexId )                
            except parent_ns.declaration_not_found_t:
                klass = self.__create_class( dia_class )
                parent_ns.adopt_declaration( klass )
                self.__classes[ dia_class.name ] = klass      
        
        map( self.__add_inner_classes, self.__classes.values() )

        self.__add_enums( self.dia_global_scope.symIndexId )
        for klass in self.__classes.itervalues():
            map( self.__add_enums, klass.dia_symbols )

        #declarations.print_declarations( self.global_ns )#.namespace( 'ns1' ) )
        #declarations.print_declarations( self.global_ns.namespace( 'std' ) )
        
if __name__ == '__main__':
    control_pdb = r'C:\dev\produce_pdb\Debug\produce_pdb.pdb'
    #control_pdb = r'xxx.pdb'
    reader = pdb_reader_t( control_pdb )
    reader.read()
    f = file( 'decls.cpp', 'w+' )
    declarations.print_declarations( reader.global_ns, writer=f.write )
    f.close()