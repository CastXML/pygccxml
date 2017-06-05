# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest
import warnings

from . import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class Test(parser_test_case.parser_test_case_t):
    global_ns = None

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'include_all.hpp'
        self.global_ns = None

    def setUp(self):
        if not Test.global_ns:
            decls = parser.parse([self.header], self.config)
            Test.xml_generator_from_xml_file = \
                self.config.xml_generator_from_xml_file
            Test.global_ns = declarations.get_global_namespace(decls)
            Test.global_ns.init_optimizer()
        self.xml_generator_from_xml_file = Test.xml_generator_from_xml_file
        self.global_ns = Test.global_ns

    def test_variable(self):
        ns_vars = self.global_ns.namespace('::declarations::variables')
        static_var = ns_vars.variable('static_var')

        # Legacy way of fetching dependencies. Is still valid but deprecated
        warnings.simplefilter("ignore", Warning)
        dependencies_old = static_var.i_depend_on_them()
        warnings.simplefilter("error", Warning)
        self.assertTrue(len(dependencies_old) == 1)
        self.assertTrue(dependencies_old[0].declaration is static_var)
        self.assertTrue(dependencies_old[0].depend_on_it.decl_string == 'int')

        dependencies_new = declarations.get_dependencies_from_decl(static_var)
        self.assertTrue(len(dependencies_new) == 1)
        self.assertTrue(dependencies_new[0].declaration is static_var)
        self.assertTrue(dependencies_new[0].depend_on_it.decl_string == 'int')

        m_mutable = ns_vars.variable('m_mutable')

        # Legacy way of fetching dependencies. Is still valid but deprecated
        warnings.simplefilter("ignore", Warning)
        dependencies_old = m_mutable.i_depend_on_them()
        warnings.simplefilter("error", Warning)
        self.assertTrue(len(dependencies_old) == 1)
        self.assertTrue(dependencies_old[0].declaration is m_mutable)
        self.assertTrue(dependencies_old[0].depend_on_it.decl_string == 'int')

        dependencies_new = declarations.get_dependencies_from_decl(m_mutable)
        self.assertTrue(len(dependencies_new) == 1)
        self.assertTrue(dependencies_new[0].declaration is m_mutable)
        self.assertTrue(dependencies_new[0].depend_on_it.decl_string == 'int')

    def test_class(self):
        ns_vars = self.global_ns.namespace('::declarations::variables')

        cls = ns_vars.class_('struct_variables_t')

        # Legacy way of fetching dependencies. Is still valid but deprecated
        warnings.simplefilter("ignore", Warning)
        dependencies_old = cls.i_depend_on_them()
        warnings.simplefilter("error", Warning)
        dependencies_old = [
            d for d in dependencies_old if not d.declaration.is_artificial]
        self.assertTrue(len(dependencies_old) == 1)

        dependencies_new = declarations.get_dependencies_from_decl(cls)
        dependencies_new = [
            d for d in dependencies_new if not d.declaration.is_artificial]
        self.assertTrue(len(dependencies_new) == 1)

        m_mutable = ns_vars.variable('m_mutable')

        # Legacy way of fetching dependencies. Is still valid but deprecated
        dependencies_old = [
            dependency for dependency in dependencies_old if
            dependency.declaration is m_mutable]
        self.assertTrue(len(dependencies_old) == 1)
        self.assertTrue(dependencies_old[0].depend_on_it.decl_string == 'int')
        self.assertTrue(dependencies_old[0].access_type == 'public')

        dependencies_new = [
            dependency for dependency in dependencies_new if
            dependency.declaration is m_mutable]
        self.assertTrue(len(dependencies_new) == 1)
        self.assertTrue(dependencies_new[0].depend_on_it.decl_string == 'int')
        self.assertTrue(dependencies_new[0].access_type == 'public')

        ns_dh = self.global_ns.namespace('::core::diamand_hierarchy')
        fd_cls = ns_dh.class_('final_derived_t')
        derived1_cls = ns_dh.class_('derived1_t')

        # Legacy way of fetching dependencies. Is still valid but deprecated
        warnings.simplefilter("ignore", Warning)
        dependencies_old = declarations.get_dependencies_from_decl(fd_cls)
        warnings.simplefilter("error", Warning)
        dependencies_old = [
            dependency for dependency in dependencies_old if
            dependency.depend_on_it is derived1_cls]
        self.assertTrue(len(dependencies_old) == 1)
        self.assertTrue(dependencies_old[0].depend_on_it is derived1_cls)
        self.assertTrue(dependencies_old[0].access_type == 'public')

        dependencies_new = declarations.get_dependencies_from_decl(fd_cls)
        dependencies_new = [
            dependency for dependency in dependencies_new if
            dependency.depend_on_it is derived1_cls]
        self.assertTrue(len(dependencies_new) == 1)
        self.assertTrue(dependencies_new[0].depend_on_it is derived1_cls)
        self.assertTrue(dependencies_new[0].access_type == 'public')

    def test_calldefs(self):
        ns = self.global_ns.namespace('::declarations::calldef')
        return_default_args = ns.calldef('return_default_args')

        # Legacy way of fetching dependencies. Is still valid but deprecated
        warnings.simplefilter("ignore", Warning)
        dependencies_old = return_default_args.i_depend_on_them()
        warnings.simplefilter("error", Warning)
        self.assertTrue(len(dependencies_old) == 3)
        used_types = [
            dependency.depend_on_it.decl_string
            for dependency in dependencies_old]
        self.assertTrue(used_types == ['int', 'int', 'bool'])

        dependencies_new = declarations.get_dependencies_from_decl(
            return_default_args)
        self.assertTrue(len(dependencies_new) == 3)
        used_types = [
            dependency.depend_on_it.decl_string
            for dependency in dependencies_new]
        self.assertTrue(used_types == ['int', 'int', 'bool'])

        some_exception = ns.class_('some_exception_t')
        other_exception = ns.class_('other_exception_t')
        calldef_with_throw = ns.calldef('calldef_with_throw')

        # Legacy way of fetching dependencies. Is still valid but deprecated
        warnings.simplefilter("ignore", Warning)
        dependencies_old = calldef_with_throw.i_depend_on_them()
        warnings.simplefilter("error", Warning)
        self.assertTrue(len(dependencies_old) == 3)
        dependencies_old = [
            dependency for dependency in dependencies_old if
            dependency.depend_on_it in (some_exception, other_exception)]
        self.assertTrue(len(dependencies_old) == 2)

        dependencies_new = declarations.get_dependencies_from_decl(
            calldef_with_throw)
        self.assertTrue(len(dependencies_new) == 3)
        dependencies_new = [
            dependency for dependency in dependencies_new if
            dependency.depend_on_it in (some_exception, other_exception)]
        self.assertTrue(len(dependencies_new) == 2)

    def test_coverage(self):
        declarations.get_dependencies_from_decl(self.global_ns)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
