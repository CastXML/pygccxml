import os
import sys
import ctypes
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

def print_enums( smb ):
    enums = smb.findChildren( SymTagEnum, None, 0 )
    for enum in iter( enums ):
        enum = AsDiaSymbol( enum )
        print 'name: ', enum.name
        if enum.container:
            print 'container: ', enum.container.name
        if enum.classParent:
            print 'parent: ', enum.classParent.name
        if enum.lexicalParent:
            print 'lexical parent: ', enum.lexicalParent.Name

        values = enum.findChildren( msdia.SymTagData, None, 0 )
        for v in iter(values):
            v = AsDiaSymbol(v)
            if v.classParent.symIndexId !=  enum.symIndexId:
                continue
            print '  value %s(%d): ' % ( v.name, v.value )

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
        self.__global_ns = declarations.namespace_t( '::' )
        
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
            return False
    
    def __list_main_classes( self ):
        #in this context main classes, are classes that was defined within a namespace
        #as opposite to classes defined in other classes
        classes = []
        dia_classes = self.dia_global_scope.findChildren( msdia.SymTagUDT, None, 0 )
        for dia_class in iter( dia_classes ):
            dia_class = AsDiaSymbol( dia_class )        
            name_splitter = details.get_name_splitter( dia_class.name )            
            for scope in name_splitter.scope_names:
                udt = self.__find_udt( scope )
                if udt:
                    classes.append( udt )
                    break
            else:
                classes.append( dia_class )
        return classes
    
    def __add_inner_classes( self ):
        for klass in self.global_ns.classes(recursive=True):
            for dia_symbol in klass.dia_symbols:
                flags = msdia.NameSearchOptions.nsCaseInRegularExpression
                inner_name = dia_symbol.name + '::.*'
                found = dia_symbol.findChildren( msdia.SymTagUDT, None, flags )
                for inner_dia_class in iter(found):
                    inner_dia_class = AsDiaSymbol( inner_dia_class )
                    inner_name_splitter = details.get_name_splitter( inner_dia_class.name )
                    try:
                        inner_klass = klass.class_( inner_name_splitter.name, recursive=False )
                        inner_klass.dia_symbols.append( inner_dia_class )
                    except klass.declaration_not_found_t:
                        klass.adopt_declaration( self.__create_class( inner_dia_class )
                                                 , details.guess_access_type( inner_dia_class.access ) )

    def __create_parent_ns( self, ns_full_name ):        
        name_splitter = details.get_name_splitter( ns_full_name )
        ns_ref = self.global_ns
        for ns_name in name_splitter.identifiers:
            try:
                ns_ref = ns_ref.ns( ns_name, recursive=False )
            except ns_ref.declaration_not_found_t:
                ns = declarations.namespace_t( ns_name )
                ns_ref.adopt_declaration( ns )
                ns_ref = ns
    
    def __create_class( self, dia_class ):
        name_splitter = details.get_name_splitter( dia_class.name )
        klass = declarations.class_t( name_splitter.name )
        klass.class_type = details.guess_class_type(dia_class.udtKind)        
        klass.dia_symbols = [ dia_class ]
        return klass
        
    def __populate_scopes(self):                
        main_classes = self.__list_main_classes()
        for dia_class in main_classes:
            name_splitter = details.get_name_splitter( dia_class.name )
            map( self.__create_parent_ns, name_splitter.scope_names )
        for dia_class in main_classes:
            name_splitter = details.get_name_splitter( dia_class.name )            
            ns_ref = self.global_ns
            if 1 < len(name_splitter.identifiers):
                ns_ref = self.global_ns.ns( '::' + name_splitter.scope_names[-1] )
            try:
                klass = ns_ref.class_( name_splitter.name, recursive=False )
                klass.dia_symbols.append( dia_class )
            except ns_ref.declaration_not_found_t:
                ns_ref.adopt_declaration( self.__create_class( dia_class ) )
        
        self.__add_inner_classes()
        
        declarations.print_declarations( self.global_ns )
        
if __name__ == '__main__':
    control_pdb = r'C:\dev\produce_pdb\Debug\produce_pdb.pdb'
    #control_pdb = r'xxx.pdb'
    reader = pdb_reader_t( control_pdb )
    reader.read()
