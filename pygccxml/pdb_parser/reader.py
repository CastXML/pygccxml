import os
import sys
import ctypes
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
        self.logger = utils.loggers.gccxml
        self.logger.debug( 'creating DiaSource object' )
        self.__dia_source = comtypes.client.CreateObject( msdia.DiaSource )
        self.logger.debug( 'loading pdb file: %s' % pdb_file_path )
        self.__dia_source.loadDataFromPdb(pdb_file_path)
        self.logger.debug( 'opening session' )
        self.__dia_session = self.__dia_source.openSession()
        self.__global_ns = declarations.namespace_t( '::' )
        self.__id2decl = {} #hash table unique symbol id : pygccxml declaration
        
    def read(self):
        self.__populate_scopes()

        files = iter( self.__dia_session.findFile( None, '', 0 ) )
        for f in files:
            f = ctypes.cast( f, ctypes.POINTER(msdia.IDiaSourceFile) )
            print 'File: ', f.fileName
            
    @property
    def dia_global_scope(self):
        return self.__dia_session.globalScope

    @property
    def global_ns(self):
        return self.__global_ns

    
    def __found_udt( self, name ):
        self.logger.debug( 'testing whether name( "%s" ) is UDT symbol' % name )
        flags = msdia.NameSearchOptions.nsfCaseSensitive
        found = self.dia_global_scope.findChildren( msdia.SymTagUDT, name, flags )
        if found.Count == 1:                      
            self.logger.debug( 'name( "%s" ) is UDT symbol' % name )
            return AsDiaSymbol( fount.Item[0] )
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
        
    def __populate_scopes(self):                
        classes = {} #full name to list of symbols
        dia_classes = self.dia_global_scope.findChildren( msdia.SymTagUDT, None, 0 )
        for dia_class in iter( dia_classes ):
            dia_class = AsDiaSymbol( dia_class )        
            if not classes.has_key( dia_class.name ):
                classes[ dia_class.name ] = [ dia_class ]
            else:
                classes[ dia_class.name ].append( dia_class )

        for name, class_list in classes.iteritems():    
            fname_splitter = details.full_name_splitter_t( name )
            klass = declarations.class_t(fname_splitter.name)
            klass.class_type = details.guess_class_type( dia_class.udtKind )
            klass.dia_symbols = class_list
            
            for index, scope in enumerate( fname_splitter.scope_names ):
                
            
            if not fname_splitter.scope_name:
                classes.append( klass )
            else:
                ns_ref = self.global_ns
                for i in range( len(scope_identifiers) - 1):
                    full_identifier = '::'.join( scope_identifiers[0:i+1] )
                    if not self.__is_udt( full_identifier ):
                        #we have namespace
                        try:
                            ns_ref = ns_ref.namespace( scope_identifiers[i], recursive=False) 
                        except ns_ref.declaration_not_found_t:
                            new_ns = declarations.namespace_t( scope_identifiers[i] )
                            ns_ref.adopt_declaration( new_ns )
                            ns_ref = new_ns
                    else:
                        classes.append( klass )
                        break
        #~ classes.sort( lambda klass1, klass2: cmp( klass1.name, klass2.name ) )
        #~ for i in classes:
            #~ print str(i)
        #~ declarations.print_declarations( self.global_ns )

if __name__ == '__main__':
    control_pdb = r'C:\dev\produce_pdb\Debug\produce_pdb.pdb'
    control_pdb = r'xxx.pdb'
    reader = pdb_reader_t( control_pdb )
    reader.read()
