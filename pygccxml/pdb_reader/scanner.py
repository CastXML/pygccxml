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


class scanner_t(object):
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
        
        self.__enums = {}
        self.__classes = {}
        self.__typedefs = {}
        self.__namespaces = {'': self.__global_ns}

        
    def read(self):
        self.__populate_scopes()
        
    @property
    def dia_global_scope(self):
        return self.__dia_session.globalScope

    @property
    def global_ns(self):
        return self.__global_ns
    
    def __are_symbols_equivalent( self, smbl1_id, smbl2_id ):
        smbl1 = self.__dia_session.symbolById(smbl1_id)
        smbl2 = self.__dia_session.symbolById(smbl2_id)
        result = self.__dia_session.symsAreEquiv( smbl1, smbl2 )
        if result:
            msg = 'Symbols "%s(%d)" and  "%s(%d)" are equivalent.' 
        else:
            msg = 'Symbols "%s(%d)" and  "%s(%d)" are NOT equivalent.' 
        self.logger.debug( msg, smbl1.name, smbl1_id, smbl2.name, smbl2_id )
        return result
    
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
        enum_decl.dia_symbols = [ enum_smbl.symIndexId ]
        enum_decl.byte_size = enum_smbl.length
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

    def __load_enums( self, parent_symbol_id ):
        parent_symbol = self.__dia_session.symbolById( parent_symbol_id )
        self.logger.debug( 'loading enums to "%s" ' % parent_symbol.name )
        for enum_smbl in iter( parent_symbol.findChildren( SymTagEnum, None, 0 ) ):
            enum_smbl = AsDiaSymbol( enum_smbl )
            enum_decl = self.__create_enum( enum_smbl )            
            if enum_decl:
                try:
                    for enum_discovered in self.__enums[ enum_smbl.name ]:
                        if self.__are_symbols_equivalent( enum_smbl.symIndexId, enum_discovered.dia_symbols[0] ):
                            continue
                    else:
                        self.__enums[ enum_smbl.name ].append( enum_decl )
                except KeyError:
                    self.__enums[ enum_smbl.name ] = [ enum_decl ]
                self.logger.debug( '\tfound %s %s' % ( enum_smbl.name, str(enum_decl) ) )
        self.logger.debug( 'loading enums to "%s" - done' % parent_symbol.name )
    
    def __create_typedef( self, typedef_smbl ):
        name_splitter = details.get_name_splitter( typedef_smbl.name )
        typedef_decl = declarations.typedef_t( name_splitter.name )
        typedef_decl.dia_symbols = [ typedef_smbl.symIndexId ]
        return typedef_decl
    
    def __load_typedefs( self, parent_symbol_id ):
        parent_symbol = self.__dia_session.symbolById( parent_symbol_id )
        self.logger.debug( 'loading typedefs to "%s" ' % parent_symbol.name )
        for typedef_smbl in iter( parent_symbol.findChildren( SymTagEnum, None, 0 ) ):
            typedef_smbl = AsDiaSymbol( typedef_smbl )
            typedef_decl = self.__create_typedef( typedef_smbl )            
            try:
                for typedef_discovered in self.__typedefs[ typedef_smbl.name ]:
                    if self.__are_symbols_equivalent( typedef_smbl.symIndexId, typedef_discovered.dia_symbols[0] ):
                        continue
                else:
                    self.__typedefs[ typedef_smbl.name ].append( typedef_decl )
            except KeyError:
                self.__typedefs[ typedef_smbl.name ] = [ typedef_decl ]
            self.logger.debug( '\tfound %s %s' % ( typedef_smbl.name, str(typedef_decl) ) )
        self.logger.debug( 'loading typedefs to "%s" - done' % parent_symbol.name )
    
    def __load_classes( self, parent_symbol_id ):
        parent_symbol = self.__dia_session.symbolById( parent_symbol_id )
        self.logger.debug( 'loading classes to "%s" ' % parent_symbol.name )
        for class_smbl in iter( parent_symbol.findChildren( msdia.SymTagUDT, None, 0 ) ):
            class_smbl = AsDiaSymbol( class_smbl )
            class_decl = self.__create_class( class_smbl )            
            try:
                equivalent_found = False
                for class_discovered in self.__classes[ class_smbl.name ]:
                    for smbl_discovered in class_discovered.dia_symbols:
                        equivalent_found = self.__are_symbols_equivalent( smbl_discovered, class_smbl.symIndexId )
                        if equivalent_found:
                            class_discovered.dia_symbols.add( class_smbl.symIndexId )
                            break
                    if equivalent_found:
                        break
                if not equivalent_found:
                    self.__classes[ class_smbl.name ].append( class_decl )
            except KeyError:
                self.__classes[ class_smbl.name ] = [ class_decl ]
            self.logger.debug( '\tfound %s' % str(class_decl) )
        self.logger.debug( 'loading classes to "%s" - done' % parent_symbol.name )
    
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
    
    def __create_class( self, class_smbl ):
        name_splitter = details.get_name_splitter( class_smbl.name )
        class_decl = declarations.class_t( name_splitter.name )
        class_decl.class_type = details.guess_class_type(class_smbl.udtKind)        
        class_decl.dia_symbols = set([class_smbl.symIndexId])
        class_decl.byte_size = class_smbl.length
        return class_decl
        
    def __populate_scopes(self):                
        self.__load_enums( self.dia_global_scope.symIndexId )
        self.__load_classes( self.dia_global_scope.symIndexId )
        self.__load_typedefs( self.dia_global_scope.symIndexId )
        #~ main_classes = self.__list_main_classes()
        #~ self.__create_nss()
        
        #~ for dia_class in main_classes:
            #~ name_splitter = details.get_name_splitter( dia_class.name )            
            #~ if not name_splitter.scope_names:
                #~ parent_ns = self.global_ns
            #~ else:
                #~ parent_ns = self.__namespaces[ name_splitter.scope_names[-1] ]
                
            #~ try:                
                #~ klass = parent_ns.class_( name_splitter.name, recursive=False )
                #~ klass.dia_symbols.add( dia_class.symIndexId )                
            #~ except parent_ns.declaration_not_found_t:
                #~ klass = self.__create_class( dia_class )
                #~ parent_ns.adopt_declaration( klass )
                #~ self.__classes[ dia_class.name ] = klass      
        
        #~ map( self.__add_inner_classes, self.__classes.values() )

        #~ self.__add_enums( self.dia_global_scope.symIndexId )
        #~ for klass in self.__classes.itervalues():
            #~ map( self.__add_enums, klass.dia_symbols )

        #declarations.print_declarations( self.global_ns )#.namespace( 'ns1' ) )
        #declarations.print_declarations( self.global_ns.namespace( 'std' ) )
        
if __name__ == '__main__':
    control_pdb = r'C:\dev\produce_pdb\Debug\produce_pdb.pdb'
    control_pdb = r'xxx.pdb'
    reader = scanner_t( control_pdb )
    reader.read()
    f = file( 'decls.cpp', 'w+' )
    declarations.print_declarations( reader.global_ns, writer=f.write )
    f.close()
