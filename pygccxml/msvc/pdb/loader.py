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
from .. import common_utils as msvc_utils

msdia = comtypes.client.GetModule( msvc_cfg.msdia_path )

SymTagEnum = 12
msdia.SymTagEnum = 12

def iif( condition, true_value, false_value ):
    if condition:
        return true_value
    else:
        return false_value

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
    COMPILER = 'MSVC PDB'
    def __init__(self, pdb_file_path ):
        self.logger = utils.loggers.pdb_reader
        self.logger.setLevel(logging.INFO)
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

    def create_type( self, smbl ):
        if msdia.SymTagBaseType == smbl.symTag:
            if enums.BasicType.btNoType == smbl.baseType:
                return declarations.unknown_t()
            elif enums.BasicType.btVoid == smbl.baseType:
                return declarations.void_t()
            elif enums.BasicType.btChar == smbl.baseType:
                return declarations.char_t()
            elif enums.BasicType.btWChar == smbl.baseType:
                return declarations.wchar_t()
            elif enums.BasicType.btInt == smbl.baseType:
                return declarations.int_t()
            elif enums.BasicType.btUInt == smbl.baseType:
                return declarations.unsigned_int_t()
            elif enums.BasicType.btFloat == smbl.baseType:
                return declarations.float_t()
            elif enums.BasicType.btBCD == smbl.baseType:
                return declarations.unknown_t()
            elif enums.BasicType.btBool == smbl.baseType:
                return declarations.bool_t()
            elif enums.BasicType.btLong == smbl.baseType:
                return declarations.long_int_t()
            elif enums.BasicType.btULong == smbl.baseType:
                return declarations.long_unsigned_int_t()
            elif enums.BasicType.btCurrency == smbl.baseType:
                return declarations.unknown_t()
            elif enums.BasicType.btDate == smbl.baseType:
                return declarations.unknown_t()
            elif enums.BasicType.btVariant == smbl.baseType:
                return declarations.unknown_t()
            elif enums.BasicType.btComplex == smbl.baseType:
                return declarations.complex_double_t()
            elif enums.BasicType.btBit == smbl.baseType:
                return declarations.unknown_t()
            elif enums.BasicType.btBSTR == smbl.baseType:
                return declarations.unknown_t()
            elif enums.BasicType.btHresult == smbl.baseType:
                return declarations.unknown_t()
            else:
                return declarations.unknown_t()
        else:
            return declarations.unknown_t()

    @utils.cached
    def symbols_table(self):
        return self.__find_table( "Symbols" )

    @utils.cached
    def symbols(self):
        smbls = {}
        for smbl in itertools.imap( as_symbol, as_enum_variant( self.symbols_table._NewEnum ) ):
            smbl.uname = msvc_utils.undecorate_name( smbl.name, msvc_utils.UNDECORATE_NAME_OPTIONS.UNDNAME_SCOPES_ONLY )
            def smbl_undecorate_name( options = None ):
                return msvc_utils.undecorate_name( smbl.name, options )
            smbl.undecorate_name = smbl_undecorate_name
            smbls[ smbl.symIndexId ] = smbl
        return smbls

    def __load_nss(self):
        def ns_filter( smbl ):
            self.logger.debug( '__load_ns.ns_filter, %s', smbl.uname )
            tags = ( msdia.SymTagFunction
                     , msdia.SymTagBlock
                     , msdia.SymTagData
                     #~ , msdia.SymTagAnnotation
                     #~ , msdia.SymTagPublicSymbol
                     , msdia.SymTagUDT
                     , msdia.SymTagEnum
                     #~ , msdia.SymTagFunctionType
                     #~ , msdia.SymTagPointerType
                     , msdia.SymTagArrayType
                     , msdia.SymTagBaseType
                     , msdia.SymTagTypedef
                     , msdia.SymTagBaseClass
                     , msdia.SymTagFriend
                     #~ , msdia.SymTagFunctionArgType
                     #~ , msdia.SymTagUsingNamespace
                    )
            if smbl.symTag not in tags:
                self.logger.debug( 'smbl.symTag not in tags, %s', smbl.uname )
                return False
            elif smbl.symTag == msdia.SymTagData and not self.__is_my_var( smbl ):
                return False
            elif not smbl.name:
                self.logger.debug( 'not smbl.name, %s', smbl.uname )
                return False
            #~ elif '-' in smbl.name:
                #~ self.logger.debug( '"-" in smbl.name, %s', smbl.uname )
                #~ return False
            elif smbl.classParent:
                parent_smbl = self.symbols[ smbl.classParentId ]
                while parent_smbl:
                    if parent_smbl.symTag == msdia.SymTagUDT:
                        if parent_smbl.uname in smbl.uname:
                            #for some reason std::map is reported as parent of std::_Tree, in source code
                            #std::map derives from std::_Tree. In logical sense parent name is a subset of the child name
                            self.logger.debug( 'parent_smbl.symTag == msdia.SymTagUDT, %s', parent_smbl.uname )
                            return False
                        else:
                            return True
                    else:
                        parent_smbl = self.symbols[ parent_smbl.classParentId ]
            else:
                return True

        self.logger.debug( 'scanning symbols table' )

        self.logger.debug( 'looking for scopes' )
        names = set()
        for index, smbl in enumerate( itertools.ifilter( ns_filter, self.symbols.itervalues() ) ):
            if index and ( index % 10000 == 0 ):
                self.logger.debug( '%d symbols scanned', index )
            name_splitter = impl_details.get_name_splitter( smbl.uname )
            for sn in name_splitter.scope_names:
                if '<' in sn:
                    break
                else:
                    names.add( sn )
        names = list( names )
        names.sort()
        self.logger.debug( 'looking for scopes - done' )

        nss = {'': self.__global_ns}

        self.logger.debug( 'building namespace objects' )
        for ns_name in itertools.ifilterfalse( self.__find_udt, names ):
            self.logger.debug( 'inserting ns "%s" into declarations tree', ns_name )
            name_splitter = impl_details.get_name_splitter( ns_name )
            if not name_splitter.scope_names:
                parent_ns = self.global_ns
            else:
                parent_ns = nss.get( name_splitter.scope_names[-1], None )
                if not parent_ns:
                    continue #in this case the parent scope is UDT
            ns_decl = declarations.namespace_t( name_splitter.name )
            parent_ns.adopt_declaration( ns_decl )
            nss[ ns_name ] = ns_decl
            self.logger.debug( 'inserting ns "%s" into declarations tree - done', ns_name )
        self.logger.debug( 'building namespace objects - done' )

        self.logger.debug( 'scanning symbols table - done' )

    def __update_decls_tree( self, decl ):
        smbl = decl.dia_symbols[0]
        name_splitter = impl_details.get_name_splitter( smbl.uname )
        if not name_splitter.scope_names:
            self.__adopt_declaration( self.global_ns, decl )
        else:
            parent_name = '::' + name_splitter.scope_names[-1]
            try:
                parent = self.global_ns.decl( parent_name )
            except:
                declarations.print_declarations( self.global_ns )
                print 'identifiers:'
                for index, identifier in enumerate(name_splitter.identifiers):
                    print index, ':', identifier
                raise
            self.__adopt_declaration( parent, decl )

    def __adopt_declaration( self, parent, decl ):
        smbl = decl.dia_symbols[0]
        already_added = parent.decls( decl.name, decl_type=decl.__class__, recursive=False, allow_empty=True )
        if not already_added:
            if isinstance( parent, declarations.namespace_t ):
                parent.adopt_declaration( decl )
            else:
                parent.adopt_declaration( decl, self.__guess_access_type( smbl ) )
        else:
            for other_decl in already_added:
                for other_smbl in other_decl.dia_symbols:
                    if self.__are_symbols_equivalent( other_smbl, smbl ):
                        other_decl.dia_symbols.append( smbl )
                        return
            else:
                if isinstance( parent, declarations.namespace_t ):
                    parent.adopt_declaration( decl )
                else:
                    parent.adopt_declaration( decl, self.__guess_access_type( smbl )  )

    def __guess_access_type( self, smbl ):
        if enums.CV_access_e.CV_private == smbl.access:
            return declarations.ACCESS_TYPES.PRIVATE
        elif enums.CV_access_e.CV_protected == smbl.access:
            return declarations.ACCESS_TYPES.PROTECTED
        else:
            fully_undecorated_name = smbl.undecorate_name()
            if fully_undecorated_name.startswith( 'private:' ):
                declarations.ACCESS_TYPES.PRIVATE
            elif fully_undecorated_name.startswith( 'protected:' ):
                declarations.ACCESS_TYPES.PROTECTED
            else:
                return declarations.ACCESS_TYPES.PUBLIC

    def __load_classes( self ):
        classes = {}#unique symbol id : class decl
        is_udt = lambda smbl: smbl.symTag == msdia.SymTagUDT
        self.logger.info( 'building udt objects' )
        for udt_smbl in itertools.ifilter( is_udt, self.symbols.itervalues() ):
            classes[udt_smbl.symIndexId] = self.__create_class(udt_smbl)
        self.logger.info( 'building udt objects(%d) - done', len(classes) )

        def does_parent_exist_in_decls_tree( class_decl ):
            class_smbl = class_decl.dia_symbols[0]
            if classes.has_key( class_smbl.classParentId ):
                return False
            name_splitter = impl_details.get_name_splitter( class_smbl.uname )
            if not name_splitter.scope_names:
                return True #global namespace
            else:
                parent_name = '::' + name_splitter.scope_names[-1]
                found = self.global_ns.decls( parent_name
                                              , decl_type=declarations.scopedef_t
                                              , allow_empty=True
                                              , recursive=True )
                return bool( found )
        self.logger.info( 'integrating udt objects with namespaces' )
        while classes:
            to_be_integrated = len( classes )
            self.logger.info( 'there are %d classes to go', len( classes ) )
            to_be_deleted = filter( does_parent_exist_in_decls_tree, classes.itervalues() )
            map( self.__update_decls_tree, to_be_deleted )
            map( lambda decl: classes.pop( decl.dia_symbols[0].symIndexId )
                 , to_be_deleted )
            if not ( to_be_integrated - len( classes ) ):
                for cls in classes.itervalues():
                    self.logger.warning( 'unable to integrate class "%s" into declarations tree', cls.dia_symbols[0].uname )
                break
        self.logger.info( 'integrating udt objects with namespaces - done' )

    def read(self):
        self.__load_nss()
        self.__load_classes()
        self.__load_enums()
        self.__load_vars()

    @property
    def dia_global_scope(self):
        return self.__dia_session.globalScope

    @property
    def global_ns(self):
        return self.__global_ns

    def __are_symbols_equivalent( self, smbl1, smbl2 ):
        result = smbl1.symTag == smbl2.symTag and smbl1.uname == smbl2.uname
        if not result:
            result = self.__dia_session.symsAreEquiv( smbl1, smbl2 )
        if result:
            msg = 'Symbols "%s(%d)" and  "%s(%d)" are equivalent.'
        else:
            msg = 'Symbols "%s(%d)" and  "%s(%d)" are NOT equivalent.'
        self.logger.debug( msg, smbl1.uname, smbl1.symIndexId, smbl2.uname, smbl2.symIndexId )
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

    def __update_decl( self, decl, smbl ):
        decl.dia_symbols = [smbl]
        decl.compiler = self.COMPILER
        decl.byte_size = smbl.length
        decl.mangled = iif( smbl.name, smbl.name, '' )
        decl.demangled = iif( smbl.uname, smbl.uname, '' )

    def __load_enums( self ):
        is_enum = lambda smbl: smbl.symTag == msdia.SymTagEnum
        self.logger.info( 'building enum objects' )
        enums_count = 0
        for enum_smbl in itertools.ifilter( is_enum, self.symbols.itervalues() ):
            enum_decl = self.__create_enum(enum_smbl)
            if not enum_decl:
                continue
            enums_count += 1
            self.__update_decls_tree( enum_decl )
        self.logger.info( 'building enum objects(%d) - done', enums_count )

    def __create_enum( self, enum_smbl ):
        name_splitter = impl_details.get_name_splitter( enum_smbl.uname )
        self.logger.debug( 'working on enum %s', enum_smbl.uname )
        enum_decl = declarations.enumeration_t( name_splitter.name )
        self.__update_decl( enum_decl, enum_smbl )

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

    def __create_class( self, class_smbl ):
        name_splitter = impl_details.get_name_splitter( class_smbl.uname )
        class_decl = declarations.class_t( name_splitter.name )
        self.__update_decl( class_decl, class_smbl )
        class_decl.class_type = impl_details.guess_class_type(class_smbl.udtKind)
        return class_decl

    def __is_my_var( self, smbl ):
        #I am only interested in global and class variables
        if smbl.symTag != msdia.SymTagData:
            return False
        if smbl.classParentId not in self.symbols:
            return True #global scope
        parent_smbl = self.symbols[ smbl.classParentId ]
        return bool( parent_smbl.symTag == msdia.SymTagUDT )

    def __load_vars( self ):
        self.logger.info( 'building variable objects' )
        vars_count = 0
        for var_smbl in itertools.ifilter( self.__is_my_var, self.symbols.itervalues() ):
            var_decl = self.__create_var(var_smbl)
            if not var_decl:
                continue
            vars_count += 1
            self.__update_decls_tree( var_decl )
        self.logger.info( 'building variable objects(%d) - done', vars_count )

    def __create_var( self, var_smbl ):
        self.logger.debug( 'creating variable "%s"', var_smbl.uname )
        name_splitter = impl_details.get_name_splitter( var_smbl.uname )
        if not name_splitter.name:
            return None
        var_decl = declarations.variable_t( name_splitter.name )
        self.__update_decl( var_decl, var_smbl )

        var_decl.type = self.create_type( var_smbl.type )
        self.logger.debug( 'creating variable "%s" - done', var_smbl.uname )
        return var_decl



