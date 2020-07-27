# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pprint
import unittest

from . import autoconfig
from . import parser_test_case

from pygccxml import utils
from pygccxml import parser
from pygccxml import declarations


def is_sub_path(root, some_path):
    root = utils.normalize_path(root)
    some_path = utils.normalize_path(some_path)
    return some_path.startswith(root)


class Core(parser_test_case.parser_test_case_t):
    """Tests core algorithms of GCC-XML and CastXML file readers."""
    global_ns = None

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.global_ns = None

    def test_top_parent(self):
        enum = self.global_ns.enumeration('::ns::ns32::E33')
        self.assertTrue(self.global_ns is enum.top_parent)

    # tests namespaces join functionality. described in gccxml.py
    def test_nss_join(self):
        # list of all namespaces
        nss = ['::ns', '::ns::ns12', '::ns::ns22', '::ns::ns32']
        # list of all namespaces that have unnamed namespace
        # unnamed_nss = nss[1:] doing nothing with this list ?
        # list of all enums [0:2] [3:5] [6:8] - has same parent
        enums = [
            '::E11',
            '::E21',
            '::E31',
            '::ns::E12',
            '::ns::E22',
            '::ns::E32',
            '::ns::ns12::E13',
            '::ns::ns22::E23',
            '::ns::ns32::E33']

        for ns in nss:
            self.global_ns.namespace(ns)

        for enum in enums:
            self.global_ns.enumeration(enum)

        ns = self.global_ns.namespace(nss[0])
        ns12 = self.global_ns.namespace(nss[1])
        ns22 = self.global_ns.namespace(nss[2])
        ns32 = self.global_ns.namespace(nss[3])
        self.assertTrue(
            ns and (
                ns is ns12.parent is ns22.parent is ns32.parent),
            'There are 2 or more instances of ns namespace.')

        e11 = self.global_ns.enumeration(enums[0])
        e21 = self.global_ns.enumeration(enums[1])
        e31 = self.global_ns.enumeration(enums[2])
        self.assertTrue(
            e11.parent is e21.parent is e31.parent,
            'There are 2 or more instances of global namespace.')

        nse12 = self.global_ns.enumeration(enums[3])
        nse23 = self.global_ns.enumeration(enums[4])
        nse33 = self.global_ns.enumeration(enums[5])
        self.assertTrue(
            ns and (
                ns is nse12.parent is nse23.parent is nse33.parent),
            'There are 2 or more instances of ns namespace.')

    def _test_ns_membership(self, ns, enum_name):
        unnamed_enum = ns.enumeration(
            lambda d: d.name == '' and is_sub_path(
                autoconfig.data_directory,
                d.location.file_name),
            recursive=False)
        self.assertTrue(
            unnamed_enum in ns.declarations,
            "namespace '%s' does not contains unnamed enum." %
            ns.name)

        enum = ns.enumeration(enum_name, recursive=False)

        self.assertTrue(
            enum in ns.declarations,
            "namespace '%s' does not contains enum '%s'" %
            (ns.name, enum.name))

        self.assertTrue(
            unnamed_enum.parent is ns,
            ("unnamed enum belong to namespace '%s' but this namespace " +
                "is not it's parent.") % ns.name)

        self.assertTrue(
            enum.parent is ns,
            ("enum '%s' belong to namespace '%s' but this namespace" +
                " is not it's parent.") % (enum.name, ns.name))

    def _test_class_membership(self, class_inst, enum_name, access):
        # getting enum through get_members function
        nested_enum1 = class_inst.enumeration(
            name=enum_name,
            function=declarations.access_type_matcher_t(access))

        # getting enum through declarations property
        nested_enum2 = class_inst.enumeration(enum_name)

        # it shoud be same object
        self.assertTrue(
            nested_enum1 is nested_enum2,
            ("enum accessed through access definition('%s') and " +
                "through declarations('%s') are different enums " +
                "or instances.") %
            (nested_enum1.name, nested_enum2.name))

        # check whether we meaning same class instance
        self.assertTrue(
            class_inst is nested_enum1.parent is nested_enum2.parent,
            'There are 2 or more instances of ns namespace.')

    # test gccxml_file_reader_t._update_membership algorithm
    def test_membership(self):
        core_membership = self.global_ns.namespace('membership')
        self._test_ns_membership(self.global_ns, 'EGlobal')
        self._test_ns_membership(
            core_membership.namespace('enums_ns'),
            'EWithin')
        self._test_ns_membership(
            core_membership.namespace(''),
            'EWithinUnnamed')
        class_nested_enums = core_membership.class_('class_for_nested_enums_t')
        self._test_class_membership(
            class_nested_enums,
            'ENestedPublic',
            declarations.ACCESS_TYPES.PUBLIC)
        self._test_class_membership(
            class_nested_enums,
            'ENestedProtected',
            declarations.ACCESS_TYPES.PROTECTED)
        self._test_class_membership(
            class_nested_enums,
            'ENestedPrivate',
            declarations.ACCESS_TYPES.PRIVATE)

    def test_mangled_name_namespace(self):
        std = self.global_ns.namespace("std")
        self.assertTrue(std, "std namespace has not been found")
        self.assertIsNone(std.mangled)

    def test_mangled_name_functions(self):
        # This works with gccxml and castxml
        ns = self.global_ns.namespace("overloads")
        do_nothing = ns.calldefs("do_nothing", recursive=False)
        self.assertTrue(
            do_nothing.mangled,
            "Mangled name of do_nothing function should be different +"
            "from None")

    def test_mangled_name_variable(self):
        # This works with gccxml and castxml
        var_inst = self.global_ns.variable('array255')
        self.assertTrue(
            var_inst.mangled,
            "Mangled name of array255 variable should be different +"
            "from None")

    def _test_is_based_and_derived(self, base, derived, access):
        dhi_v = declarations.hierarchy_info_t(derived, access, True)
        dhi_not_v = declarations.hierarchy_info_t(derived, access, False)
        self.assertTrue(
            dhi_v in base.derived or dhi_not_v in base.derived,
            "base class '%s' doesn't has derived class '%s'" %
            (base.name, derived.name))

        bhi_v = declarations.hierarchy_info_t(base, access, True)
        bhi_not_v = declarations.hierarchy_info_t(base, access, False)

        self.assertTrue(
            bhi_v in derived.bases or bhi_not_v in derived.bases,
            "derive class '%s' doesn't has base class '%s'" %
            (derived.name, base.name))

    def test_class_hierarchy(self):
        class_hierarchy = self.global_ns.namespace('class_hierarchy')

        base = class_hierarchy.class_('base_t')
        other_base = class_hierarchy.class_('other_base_t')
        derived_public = class_hierarchy.class_('derived_public_t')
        derived_protected = class_hierarchy.class_('derived_protected_t')
        derived_private = class_hierarchy.class_('derived_private_t')
        multi_derived = class_hierarchy.class_('multi_derived_t')

        self._test_is_based_and_derived(
            base,
            derived_public,
            declarations.ACCESS_TYPES.PUBLIC)
        self._test_is_based_and_derived(
            base,
            derived_protected,
            declarations.ACCESS_TYPES.PROTECTED)
        self._test_is_based_and_derived(
            base,
            derived_private,
            declarations.ACCESS_TYPES.PRIVATE)
        self._test_is_based_and_derived(
            base,
            multi_derived,
            declarations.ACCESS_TYPES.PROTECTED)
        self._test_is_based_and_derived(
            other_base,
            multi_derived,
            declarations.ACCESS_TYPES.PRIVATE)
        self._test_is_based_and_derived(
            derived_private,
            multi_derived,
            declarations.ACCESS_TYPES.PRIVATE)

    def _test_is_same_bases(self, derived1, derived2):
        bases1 = set([id(hierarchy_info.related_class)
                      for hierarchy_info in derived1.bases])
        bases2 = set([id(hierarchy_info.related_class)
                      for hierarchy_info in derived2.bases])
        self.assertTrue(
            bases1 == bases2,
            ("derived class '%s' and derived class '%s' has references to " +
                "different instance of base classes ") %
            (derived1.name, derived2.name))

    def test_class_join(self):
        diamand_hierarchy = self.global_ns.namespace('diamand_hierarchy')
        base = diamand_hierarchy.class_('base_t')
        derived1 = diamand_hierarchy.class_('derived1_t')
        derived2 = diamand_hierarchy.class_('derived2_t')
        final_derived = diamand_hierarchy.class_('final_derived_t')

        self._test_is_based_and_derived(
            base,
            derived1,
            declarations.ACCESS_TYPES.PUBLIC)
        self._test_is_based_and_derived(
            base,
            derived2,
            declarations.ACCESS_TYPES.PUBLIC)
        self._test_is_based_and_derived(
            derived1,
            final_derived,
            declarations.ACCESS_TYPES.PUBLIC)
        self._test_is_based_and_derived(
            derived2,
            final_derived,
            declarations.ACCESS_TYPES.PUBLIC)
        self._test_is_same_bases(derived1, derived2)

    def test_fundamental_types(self):
        # check whether all build in types could be constructed
        errors = []
        for fundamental_type_name, fundamental_type in \
                declarations.FUNDAMENTAL_TYPES.items():
            if 'complex' in fundamental_type_name:
                continue  # I check this in an other tester
            if isinstance(
                fundamental_type,
                    (declarations.int128_t, declarations.uint128_t)):
                continue  # I don't have test case for this
            if isinstance(fundamental_type, declarations.java_fundamental_t):
                continue  # I don't check this at all
            typedef_name = 'typedef_' + fundamental_type_name.replace(' ', '_')
            typedef = self.global_ns.decl(
                decl_type=declarations.typedef_t,
                name=typedef_name)
            self.assertTrue(
                typedef,
                "unable to find typedef to build-in type '%s'" %
                fundamental_type_name)
            if typedef.decl_type.decl_string != fundamental_type.decl_string:
                errors.append(
                    "there is a difference between typedef base type " +
                    "name('%s') and expected one('%s')" %
                    (typedef.decl_type.decl_string,
                     fundamental_type.decl_string))
        self.assertFalse(errors, pprint.pformat(errors))

    def test_compound_types(self):
        typedef_inst = self.global_ns.decl(
            decl_type=declarations.typedef_t,
            name='typedef_const_int')
        self._test_type_composition(
            typedef_inst.decl_type,
            declarations.const_t,
            declarations.int_t)

        typedef_inst = self.global_ns.decl(
            decl_type=declarations.typedef_t,
            name='typedef_pointer_int')
        self._test_type_composition(
            typedef_inst.decl_type,
            declarations.pointer_t,
            declarations.int_t)

        typedef_inst = self.global_ns.decl(
            decl_type=declarations.typedef_t,
            name='typedef_reference_int')
        self._test_type_composition(
            typedef_inst.decl_type,
            declarations.reference_t,
            declarations.int_t)

        typedef_inst = self.global_ns.decl(
            decl_type=declarations.typedef_t,
            name='typedef_const_unsigned_int_const_pointer')
        self._test_type_composition(
            typedef_inst.decl_type,
            declarations.const_t,
            declarations.pointer_t)
        self._test_type_composition(
            typedef_inst.decl_type.base,
            declarations.pointer_t,
            declarations.const_t)
        self._test_type_composition(
            typedef_inst.decl_type.base.base,
            declarations.const_t,
            declarations.unsigned_int_t)

        typedef_inst = self.global_ns.decl(
            decl_type=declarations.typedef_t,
            name='typedef_volatile_int')
        self._test_type_composition(
            typedef_inst.decl_type,
            declarations.volatile_t,
            declarations.int_t)

        var_inst = self.global_ns.variable('array255')
        self._test_type_composition(
            var_inst.decl_type,
            declarations.array_t,
            declarations.int_t)

        typedef_inst = self.global_ns.decl(
            decl_type=declarations.typedef_t,
            name='typedef_EFavoriteDrinks')
        self.assertTrue(
            isinstance(
                typedef_inst.decl_type,
                declarations.declarated_t),
            " typedef to enum should be 'declarated_t' instead of '%s'" %
            typedef_inst.decl_type.__class__.__name__)
        enum_declaration = self.global_ns.enumeration('EFavoriteDrinks')
        self.assertTrue(
            typedef_inst.decl_type.declaration is enum_declaration,
            "instance of declaration_t has reference to '%s' instead of '%s'" %
            (typedef_inst.decl_type.declaration.name,
             enum_declaration.name))

    def test_free_function_type(self):
        function_ptr = self.global_ns.decl(
            decl_type=declarations.typedef_t,
            name='function_ptr')
        self._test_type_composition(
            function_ptr.decl_type,
            declarations.pointer_t,
            declarations.free_function_type_t)
        function_type = function_ptr.decl_type.base
        self.assertTrue(
            isinstance(
                function_type.return_type,
                declarations.int_t),
            "return function type of typedef 'function_ptr' should be " +
            "'%s' instead of '%s' " %
            ('int_t', function_type.return_type.__class__.__name__))
        self.assertTrue(
            len(function_type.arguments_types) == 2,
            "number of arguments of function of typedef 'function_ptr' " +
            "should be 2 instead of '%d' " %
            len(function_type.arguments_types))
        self.assertTrue(
            isinstance(
                function_type.arguments_types[0],
                declarations.int_t),
            "first argument of function of typedef 'function_ptr' should be " +
            "'%s' instead of '%s' " %
            ('int_t', function_type.arguments_types[0].__class__.__name__))
        self.assertTrue(
            isinstance(
                function_type.arguments_types[1],
                declarations.double_t),
            "first argument of function of typedef 'function_ptr' should be " +
            "'%s' instead of '%s' " %
            ('double_t', function_type.arguments_types[0].__class__.__name__))

    def test_member_function_type(self):
        function_ptr = self.global_ns.decl(
            decl_type=declarations.typedef_t,
            name='member_function_ptr_t')
        self._test_type_composition(
            function_ptr.decl_type,
            declarations.pointer_t,
            declarations.member_function_type_t)

        function_type = function_ptr.decl_type.base

        members_pointers = self.global_ns.class_('members_pointers_t')
        self.assertTrue(
            function_type.class_inst.declaration is members_pointers,
            "member function type class should be '%s' instead of '%s'" %
            (members_pointers.decl_string,
             function_type.class_inst.decl_string))

        self.assertTrue(
            isinstance(
                function_type.return_type,
                declarations.int_t),
            "return function type of typedef 'member_function_ptr_t' should " +
            "be '%s' instead of '%s' " %
            ('int_t', function_type.return_type.__class__.__name__))
        self.assertTrue(
            len(
                function_type.arguments_types) == 1,
            "number of arguments of function of typedef " +
            "'member_function_ptr_t' should be 1 instead of '%d' " % len(
                function_type.arguments_types))
        self.assertTrue(
            isinstance(
                function_type.arguments_types[0],
                declarations.double_t),
            "first argument of function of typedef 'member_function_ptr_t' " +
            "should be '%s' instead of '%s' " %
            ('double_t', function_type.arguments_types[0].__class__.__name__))

        self.assertTrue(
            function_type.has_const,
            " 'member_function_ptr_t' should be const function.")

    def test_member_variable_type(self):
        mv = self.global_ns.decl(
            decl_type=declarations.typedef_t,
            name='member_variable_ptr_t')
        self._test_type_composition(
            mv.decl_type,
            declarations.pointer_t,
            declarations.member_variable_type_t)

        members_pointers = self.global_ns.class_('members_pointers_t')
        self.assertTrue(
            members_pointers,
            "unable to find class('%s')" %
            'members_pointers_t')
        self._test_type_composition(
            mv.decl_type.base,
            declarations.member_variable_type_t,
            declarations.declarated_t)
        mv_type = mv.decl_type.base
        self.assertTrue(
            mv_type.base.declaration is members_pointers,
            "member function type class should be '%s' instead of '%s'" %
            (members_pointers.decl_string,
             mv_type.base.decl_string))

    def test_overloading(self):
        ns = self.global_ns.namespace('overloads')

        do_nothings = ns.calldefs('do_nothing', recursive=False)
        self.assertTrue(
            4 == len(do_nothings),
            ("expected number of overloaded 'do_nothing' functions is %d " +
                "and existing(%d) is different") %
            (4, len(do_nothings)))
        for index, do_nothing in enumerate(do_nothings):
            others = do_nothings[:index] + do_nothings[index + 1:]
            if set(do_nothing.overloads) != set(others):
                print('\nexisting: ')
                for x in do_nothing.overloads:
                    print(str(x))
                print('\nexpected: ')
                for x in others:
                    print(str(x))

            self.assertTrue(set(do_nothing.overloads) == set(
                others), "there is a difference between expected function " +
                "overloads and existing ones.")

    def test_abstract_classes(self):
        ns = self.global_ns.namespace('abstract_classes')
        abstract_i = ns.class_('abstract_i')
        self.assertTrue(
            abstract_i.is_abstract,
            "class 'abstract_i' should be abstract")
        derived_abstract_i = ns.class_('derived_abstract_i')
        self.assertTrue(
            derived_abstract_i.is_abstract,
            "class 'derived_abstract_i' should be abstract")
        implementation = ns.class_('implementation')
        self.assertTrue(
            not implementation.is_abstract,
            "class 'implementation' should not be abstract")

    def test_byte_size(self):
        mptrs = self.global_ns.class_('members_pointers_t')
        self.assertTrue(mptrs.byte_size != 0)

    def test_byte_align(self):
        mptrs = self.global_ns.class_('members_pointers_t')
        self.assertTrue(mptrs.byte_align != 0)

    def test_byte_offset(self):
        mptrs = self.global_ns.class_('members_pointers_t')
        self.assertTrue(mptrs.variable('xxx').byte_offset != 0)


class CoreXMLGenerator(Core):
    """Tests core algorithms of GCC-XML and CastXML file readers."""
    global_ns = None
    COMPILATION_MODE = None
    INIT_OPTIMIZER = None

    def __init__(self, *args):
        Core.__init__(self, *args)
        self.test_files = [
            'core_ns_join_1.hpp',
            'core_ns_join_2.hpp',
            'core_ns_join_3.hpp',
            'core_membership.hpp',
            'core_class_hierarchy.hpp',
            'core_types.hpp',
            'core_diamand_hierarchy_base.hpp',
            'core_diamand_hierarchy_derived1.hpp',
            'core_diamand_hierarchy_derived2.hpp',
            'core_diamand_hierarchy_final_derived.hpp',
            'core_overloads_1.hpp',
            'core_overloads_2.hpp',
            'abstract_classes.hpp']
        self.global_ns = None

    def setUp(self):
        if not Core.global_ns:
            decls = parser.parse(
                self.test_files,
                self.config,
                self.COMPILATION_MODE)
            Core.global_ns = declarations.get_global_namespace(
                decls)
            if self.INIT_OPTIMIZER:
                Core.global_ns.init_optimizer()
            Core.xml_generator_from_xml_file = \
                self.config.xml_generator_from_xml_file
        self.global_ns = Core.global_ns
        self.xml_generator_from_xml_file = Core.xml_generator_from_xml_file


class core_all_at_once_t(CoreXMLGenerator):
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    INIT_OPTIMIZER = True

    def __init__(self, *args):
        CoreXMLGenerator.__init__(self, *args)


class core_all_at_once_no_opt_t(CoreXMLGenerator):
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    INIT_OPTIMIZER = False

    def __init__(self, *args):
        CoreXMLGenerator.__init__(self, *args)


class core_file_by_file_t(CoreXMLGenerator):
    COMPILATION_MODE = parser.COMPILATION_MODE.FILE_BY_FILE
    INIT_OPTIMIZER = True

    def __init__(self, *args):
        CoreXMLGenerator.__init__(self, *args)


class core_file_by_file_no_opt_t(CoreXMLGenerator):
    COMPILATION_MODE = parser.COMPILATION_MODE.FILE_BY_FILE
    INIT_OPTIMIZER = False

    def __init__(self, *args):
        CoreXMLGenerator.__init__(self, *args)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(core_all_at_once_t))
    suite.addTest(unittest.makeSuite(core_all_at_once_no_opt_t))
    suite.addTest(unittest.makeSuite(core_file_by_file_t))
    suite.addTest(unittest.makeSuite(core_file_by_file_no_opt_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
