import os
import sys
import ctypes
import pprint
import logging
import comtypes
import itertools
import comtypes.client

from . import enums
from . import impl_details

from ... import utils
from ... import declarations
from .. import config as msvc_cfg

msdia = comtypes.client.GetModule( msvc_cfg.msdia_path )

SymTagEnum = 12
msdia.SymTagEnum = 12

def as_symbol( x ):
    return ctypes.cast( x, ctypes.POINTER( msdia.IDiaSymbol ) )

def as_table( x ):
    return ctypes.cast( x, ctypes.POINTER( msdia.IDiaTable ) )

def as_enum_symbols( x ):
    return ctypes.cast( x, ctypes.POINTER( msdia.IDiaEnumSymbols ) )

def as_enum_variant( x ):
    return ctypes.cast( x, ctypes.POINTER( comtypes.automation.IEnumVARIANT ) )

def print_files( session ):
    files = iter( session.findFile( None, '', 0 ) )
    for f in files:
        f = ctypes.cast( f, ctypes.POINTER(msdia.IDiaSourceFile) )
        print 'File: ', f.fileName

class decl_loader_t(object):
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

    def __find_table(self, name):
        valid_names = ( 'Symbols', 'SourceFiles', 'Sections'
                        , 'SegmentMap', 'InjectedSource', 'FrameData' )
        tables = self.__dia_session.getEnumTables()
        for table in itertools.imap(as_table, tables):
            if name == table.name:
                return table
        else:
            return None

    @utils.cached
    def symbols_table(self):
        return self.__find_table( "Symbols" )

    @utils.cached
    def symbols(self):
        smbls = {}
        for smbl in itertools.imap( as_symbol, as_enum_variant( self.symbols_table._NewEnum ) ):
            smbls[ smbl.symIndexId ] = smbl
        return smbls

    def __load_nss(self):
        def ns_filter( smbl ):
            tags = ( msdia.SymTagFunction
                     , msdia.SymTagBlock
                     #I should skipp data, because it requier different treatment
                     #, msdia.SymTagData
                     , msdia.SymTagAnnotation
                     , msdia.SymTagPublicSymbol
                     , msdia.SymTagUDT
                     , msdia.SymTagEnum
                     , msdia.SymTagFunctionType
                     , msdia.SymTagPointerType
                     , msdia.SymTagArrayType
                     , msdia.SymTagBaseType
                     , msdia.SymTagTypedef
                     , msdia.SymTagBaseClass
                     , msdia.SymTagFriend
                     , msdia.SymTagFunctionArgType
                     , msdia.SymTagUsingNamespace )
            if smbl.symTag not in tags:
                return False
            elif not smbl.name:
                return False
            elif smbl.classParent:
                if smbl.classParent.name:
                    return False
                parent_smbl = smbl.classParent
                while parent_smbl:
                    if parent_smbl.symTag == msdia.SymTagUDT:
                        return False
                    else:
                        parent_smbl = parent_smbl.classParent
            elif smbl.name.endswith( '__unnamed' ):
                return False
            return True

        self.logger.debug( 'scanning symbols table' )

        self.logger.debug( 'looking for scopes' )
        names = set()
        for index, smbl in enumerate( itertools.ifilter( ns_filter, self.symbols.itervalues() ) ):
            if index and ( index % 10000 == 0 ):
                self.logger.debug( '%d symbols scanned', index )
            if '_Facetptr<std::ctype<char> >' in smbl.name:
                i = 0
            name_splitter = impl_details.get_name_splitter( smbl.name )
            names.update( name_splitter.scope_names )
        names = list( names )
        names.sort()
        self.logger.debug( 'looking for scopes - done' )

        nss = {'': self.__global_ns}

        self.logger.debug( 'building namespace objects' )
        for ns_name in itertools.ifilterfalse( self.__find_udt, names ):
            name_splitter = impl_details.get_name_splitter( ns_name )
            if not name_splitter.scope_names:
                parent_ns = self.global_ns
            else:
                parent_ns = nss[ name_splitter.scope_names[-1] ]
            ns_decl = declarations.namespace_t( name_splitter.name )
            parent_ns.adopt_declaration( ns_decl )
            nss[ ns_name ] = ns_decl
        self.logger.debug( 'building namespace objects - done' )

        self.logger.debug( 'scanning symbols table - done' )

    def __load_classes( self ):
        classes = {}#unique symbold id : class decl
        is_udt = lambda smbl: smbl.symTag == msdia.SymTagUDT
        self.logger.info( 'building udt objects' )
        for udt_smbl in itertools.ifilter( is_udt, self.symbols.itervalues() ):
            classes[udt_smbl.symIndexId] = self.__create_class(udt_smbl)
        self.logger.info( 'building udt objects(%d) - done', len(classes) )

        does_parent_exist = lambda cls_decl: not classes.has_key( cls_decl.dia_symbols[0].classParentId )
        self.logger.info( 'integrating udt objects with namespaces' )
        while classes:
            self.logger.info( 'there are %d classes to go', len( classes ) )
            to_be_deleted = filter( does_parent_exist, classes.itervalues() )
            for ns_class in to_be_deleted:
                udt_smbl = ns_class.dia_symbols[0]
                name_splitter = impl_details.get_name_splitter( udt_smbl.name )
                if not name_splitter.scope_names:
                    self.global_ns.adopt_declaration( ns_class )
                else:
                    parent_name = '::' + name_splitter.scope_names[-1]
                    parent = self.global_ns.decls( parent_name, allow_empty=True )
                    if not parent:
                        self.logger.debug( 'unable to find parent for class %s', udt_smbl.name )
                        continue
                    if isinstance( parent[0], declarations.namespace_t ):
                        parent.adopt_declaration( ns_class )
                    else:
                        parent[0].adopt_declaration( ns_class, declarations.ACCESS_TYPES.PUBLIC )
                del classes[ ns_class.dia_symbols[0].symIndexId ]
        self.logger.info( 'integrating udt objects with namespaces - done' )

    def read(self):
        self.__load_nss()
        self.__load_classes()

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
        flags = enums.NameSearchOptions.nsfCaseSensitive
        found = self.dia_global_scope.findChildren( msdia.SymTagUDT, name, flags )
        if found.Count == 1:
            self.logger.debug( 'name( "%s" ) is UDT symbol' % name )
            return as_symbol( found.Item(0) )
        elif 1 < found.Count:
            raise RuntimeError( "duplicated UDTs with name '%s', were found" % name )
            #~ self.logger.debug( 'name( "%s" ) is UDT symbol' % name )
            #~ return [as_symbol( s ) for s in  iter(found)]
            #~ for s in iter(found):
                #~ s =
                #~ print s.name
                #~ print impl_details.guess_class_type(s.udtKind)
        else:
            self.logger.debug( 'name( "%s" ) is **NOT** UDT symbol' % name )
            return None


    def __create_enum( self, enum_smbl ):
        name_splitter = impl_details.get_name_splitter( enum_smbl.name )
        enum_decl = declarations.enumeration_t( name_splitter.name )
        enum_decl.dia_symbols = [ enum_smbl.symIndexId ]
        enum_decl.byte_size = enum_smbl.length
        values = enum_smbl.findChildren( msdia.SymTagData, None, 0 )
        for v in itertools.imap(as_symbol, values):
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


    def __create_typedef( self, typedef_smbl ):
        name_splitter = impl_details.get_name_splitter( typedef_smbl.name )
        typedef_decl = declarations.typedef_t( name_splitter.name )
        typedef_decl.dia_symbols = [ typedef_smbl.symIndexId ]
        return typedef_decl

    def __create_class( self, class_smbl ):
        name_splitter = impl_details.get_name_splitter( class_smbl.name )
        class_decl = declarations.class_t( name_splitter.name )
        class_decl.class_type = impl_details.guess_class_type(class_smbl.udtKind)
        class_decl.dia_symbols = [class_smbl]
        class_decl.byte_size = class_smbl.length
        return class_decl
