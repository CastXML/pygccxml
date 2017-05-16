# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pprint
import unittest

from . import autoconfig
from . import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class declarations_t(parser_test_case.parser_test_case_t):

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.global_ns = None

    def test_enumeration_t(self):
        enum = self.global_ns.enumeration('ENumbers')
        expected_values = list(
            zip(['e%d' % index for index in range(10)],
                [index for index in range(10)]))
        self.assertTrue(
            expected_values == enum.values,
            ("expected enum values ( '%s' ) and existings ( '%s' ) are " +
                "different") %
            (pprint.pformat(expected_values), pprint.pformat(enum.values)))

    def test_namespace(self):
        pass  # tested in core_tester

    def test_types(self):
        pass  # tested in core_tester

    def test_variables(self):
        self.global_ns.namespace('variables')
        initialized = self.global_ns.variable(name='initialized')

        expected_value = '10122004'
        self.assertTrue(
            initialized.value == expected_value,
            ("there is a difference between expected value( %s ) and real " +
                "value(%s) of 'initialized' variable") %
            (expected_value, initialized.value))
        self._test_type_composition(
            initialized.decl_type,
            declarations.const_t,
            declarations.long_unsigned_int_t)

        m_mutable = self.global_ns.variable(name="m_mutable")
        self.assertFalse(
            m_mutable.type_qualifiers.has_static,
            "m_mutable must not have static type qualifier")

        self.assertTrue(
            m_mutable.type_qualifiers.has_mutable,
            "m_mutable must have mutable type qualifier")

        # External static variable
        extern_var = self.global_ns.variable(name="extern_var")
        self.assertTrue(
            extern_var.type_qualifiers.has_extern,
            "extern_var must have extern type qualifier")
        self.assertFalse(
            extern_var.type_qualifiers.has_static,
            "extern_var must not have a static type qualifier")
        self.assertFalse(
            extern_var.type_qualifiers.has_mutable,
            "static_var must not have mutable type qualifier")

        # Static variable
        static_var = self.global_ns.variable(name="static_var")
        self.assertTrue(
            static_var.type_qualifiers.has_static,
            "static_var must have static type qualifier")
        self.assertFalse(
            static_var.type_qualifiers.has_extern,
            "static_var must not have an extern type qualifier")
        self.assertFalse(
            static_var.type_qualifiers.has_mutable,
            "static_var must not have mutable type qualifier")

        ssv_static_var = self.global_ns.variable(name="ssv_static_var")
        self.assertTrue(
            ssv_static_var.type_qualifiers.has_static,
            "ssv_static_var must have static type qualifier")
        self.assertFalse(
            ssv_static_var.type_qualifiers.has_extern,
            "ssv_static_var must not have an extern type qualifier")
        self.assertFalse(
            ssv_static_var.type_qualifiers.has_mutable,
            "ssv_static_var must not have mutable type qualifier")

        ssv_static_var_value = self.global_ns.variable(
            name="ssv_static_var_value")
        self.assertTrue(
            ssv_static_var_value.type_qualifiers.has_static,
            "ssv_static_var_value must have static type qualifier")
        self.assertFalse(
            ssv_static_var_value.type_qualifiers.has_extern,
            "ssv_static_var_value must not have an extern type qualifier")
        self.assertFalse(
            ssv_static_var_value.type_qualifiers.has_mutable,
            "ssv_static_var_value must not have mutable type qualifier")

    def test_calldef_free_functions(self):
        ns = self.global_ns.namespace('calldef')

        no_return_no_args = ns.free_function('no_return_no_args')

        self._test_calldef_return_type(no_return_no_args, declarations.void_t)
        self.assertTrue(
            not no_return_no_args.has_extern,
            "function 'no_return_no_args' should have an extern qualifier")

        # Static_call is explicetely defined as extern, this works with gccxml
        # and castxml.
        static_call = ns.free_function('static_call')
        self.assertTrue(
            static_call,
            "function 'no_return_no_args' should have an extern qualifier")

        return_no_args = ns.free_function('return_no_args')
        self._test_calldef_return_type(return_no_args, declarations.int_t)
        # from now there is no need to check return type.
        no_return_1_arg = ns.free_function(name='no_return_1_arg')
        self.assertTrue(
            no_return_1_arg,
            "unable to find 'no_return_1_arg' function")
        self.assertTrue(no_return_1_arg.arguments[0].name in ['arg', 'arg0'])
        self._test_calldef_args(
            no_return_1_arg,
            [declarations.argument_t(
                name=no_return_1_arg.arguments[0].name,
                decl_type=declarations.int_t())])

        return_default_args = ns.free_function('return_default_args')
        self.assertTrue(
            return_default_args.arguments[0].name in ['arg', 'arg0'])
        self.assertTrue(
            return_default_args.arguments[1].name in ['arg1', 'flag'])
        self._test_calldef_args(
            return_default_args,
            [declarations.argument_t(
                name=return_default_args.arguments[0].name,
                decl_type=declarations.int_t(),
                default_value='1'),
                declarations.argument_t(
                    name=return_default_args.arguments[1].name,
                    decl_type=declarations.bool_t(),
                    default_value='false')])
        self._test_calldef_exceptions(return_default_args, [])

        calldef_with_throw = ns.free_function('calldef_with_throw')
        self.assertTrue(
            calldef_with_throw,
            "unable to find 'calldef_with_throw' function")
        self._test_calldef_exceptions(
            calldef_with_throw, [
                'some_exception_t', 'other_exception_t'])
        # from now there is no need to check exception specification

    def test_calldef_member_functions(self):
        struct_calldefs = self.global_ns.class_('calldefs_t')

        member_inline_call = struct_calldefs.member_function(
            'member_inline_call')
        self._test_calldef_args(
            member_inline_call, [
                declarations.argument_t(
                    name='i', decl_type=declarations.int_t())])

        member_const_call = struct_calldefs.member_function(
            'member_const_call')
        self.assertTrue(
            member_const_call.has_const,
            "function 'member_const_call' should have const qualifier")
        self.assertTrue(
            member_const_call.virtuality ==
            declarations.VIRTUALITY_TYPES.NOT_VIRTUAL,
            "function 'member_const_call' should be non virtual function")

        member_virtual_call = struct_calldefs.member_function(
            name='member_virtual_call')
        self.assertTrue(
            member_virtual_call.virtuality ==
            declarations.VIRTUALITY_TYPES.VIRTUAL,
            "function 'member_virtual_call' should be virtual function")

        member_pure_virtual_call = struct_calldefs.member_function(
            'member_pure_virtual_call')
        self.assertTrue(
            member_pure_virtual_call.virtuality ==
            declarations.VIRTUALITY_TYPES.PURE_VIRTUAL,
            ("function 'member_pure_virtual_call' should be pure virtual " +
                "function"))

        static_call = struct_calldefs.member_function('static_call')
        self.assertTrue(
            static_call.has_static,
            "function 'static_call' should have static qualifier")
        # from now we there is no need to check static qualifier

    def test_constructors_destructors(self):
        struct_calldefs = self.global_ns.class_('calldefs_t')

        destructor = struct_calldefs.calldef('~calldefs_t')
        self._test_calldef_args(destructor, [])
        self._test_calldef_return_type(destructor, None.__class__)

        # well, now we have a few functions ( constructors ) with the same
        # name, there is no easy way to find the desired one. Well in my case
        # I have only 4 constructors
        # 1. from char
        # 2. from (int,double)
        # 3. default
        # 4. copy constructor
        constructor_found = struct_calldefs.constructors('calldefs_t')
        self.assertTrue(
            len(constructor_found) == 5,
            ("struct 'calldefs_t' has 5 constructors, pygccxml parser " +
                "reports only about %d.") %
            len(constructor_found))
        error_text = "copy constructor has not been found"
        self.assertTrue(1 == len(
            [constructor for constructor in constructor_found if
                declarations.is_copy_constructor(constructor)]), error_text)
        # there is nothing to check about constructors - I know the
        # implementation of parser.
        # In this case it doesn't different from any other function

        c = struct_calldefs.constructor('calldefs_t', arg_types=['char'])
        self.assertTrue(
            c.explicit,
            ("calldef_t constructor defined with 'explicit' keyword, " +
                "for some reason the value is False "))

        arg_type = declarations.declarated_t(
            self.global_ns.class_('some_exception_t'))
        c = struct_calldefs.constructor('calldefs_t', arg_types=[arg_type])
        self.assertTrue(
            c.explicit is False,
            ("calldef_t constructor defined without 'explicit' keyword, " +
                "for some reason the value is True "))

    def test_operator_symbol(self):
        calldefs_operators = ['=', '==']
        calldefs_cast_operators = ['char *', 'double']
        struct_calldefs = self.global_ns.class_('calldefs_t')
        self.assertTrue(struct_calldefs, "unable to find struct 'calldefs_t'")
        for decl in struct_calldefs.declarations:
            if not isinstance(decl, declarations.operator_t):
                continue
            if not isinstance(decl, declarations.casting_operator_t):
                self.assertTrue(
                    decl.symbol in calldefs_operators,
                    "unable to find operator symbol for operator '%s'" %
                    decl.decl_string)
            else:
                self.assertTrue(
                    decl.return_type.decl_string in calldefs_cast_operators,
                    "unable to find operator symbol for operator '%s'" %
                    decl.decl_string)

    def test_ellipsis(self):
        ns = self.global_ns.namespace('ellipsis_tester')
        do_smth = ns.member_function('do_smth')
        self.assertTrue(do_smth.has_ellipsis)
        do_smth_else = ns.free_function('do_smth_else')
        self.assertTrue(do_smth_else.has_ellipsis)


class gccxml_declarations_t(declarations_t):
    global_ns = None

    def __init__(self, *args):
        declarations_t.__init__(self, *args)
        self.test_files = [
            'declarations_enums.hpp',
            'declarations_variables.hpp',
            'declarations_calldef.hpp']
        self.global_ns = None

    def setUp(self):
        if not gccxml_declarations_t.global_ns:
            decls = parser.parse(
                self.test_files,
                self.config,
                self.COMPILATION_MODE)
            gccxml_declarations_t.global_ns = \
                declarations.get_global_namespace(decls)
            gccxml_declarations_t.xml_generator_from_xml_file = \
                self.config.xml_generator_from_xml_file
        if not self.global_ns:
            self.xml_generator_from_xml_file = \
                gccxml_declarations_t.xml_generator_from_xml_file
            self.global_ns = gccxml_declarations_t.global_ns


class all_at_once_tester_t(gccxml_declarations_t):
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE

    def __init__(self, *args):
        gccxml_declarations_t.__init__(self, *args)


class file_by_file_tester_t(gccxml_declarations_t):
    COMPILATION_MODE = parser.COMPILATION_MODE.FILE_BY_FILE

    def __init__(self, *args):
        gccxml_declarations_t.__init__(self, *args)


class pdb_based_tester_t(declarations_t):

    def __init__(self, *args):
        declarations_t.__init__(self, *args)
        self.global_ns = autoconfig.get_pdb_global_ns()


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(file_by_file_tester_t))
    suite.addTest(unittest.makeSuite(all_at_once_tester_t))
    # if os.name == 'nt' and autoconfig.get_pdb_global_ns():
    # suite.addTest( unittest.makeSuite(pdb_based_tester_t))

    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
