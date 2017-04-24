# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest

from . import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class Test(parser_test_case.parser_test_case_t):
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    global_ns = None

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'vector_traits.hpp'
        self.global_ns = None

    def setUp(self):
        if not Test.global_ns:
            decls = parser.parse([self.header], self.config)
            Test.global_ns = declarations.get_global_namespace(decls)
        self.global_ns = Test.global_ns

    def validate_yes(self, value_type, container):
        traits = declarations.vector_traits
        self.assertTrue(traits.is_my_case(container))
        self.assertTrue(
            declarations.is_same(
                value_type,
                traits.element_type(container)))
        self.assertTrue(traits.is_sequence(container))

    def test_global_ns(self):
        value_type = self.global_ns.class_('_0_')
        container = self.global_ns.typedef('container', recursive=False)
        self.validate_yes(value_type, container)

    def test_yes(self):
        yes_ns = self.global_ns.namespace('yes')
        for struct in yes_ns.classes():
            if not struct.name.startswith('_'):
                continue
            if not struct.name.endswith('_'):
                continue
            self.validate_yes(
                struct.typedef('value_type'),
                struct.typedef('container'))

    def test_no(self):
        traits = declarations.vector_traits
        no_ns = self.global_ns.namespace('no')
        for struct in no_ns.classes():
            if not struct.name.startswith('_'):
                continue
            if not struct.name.endswith('_'):
                continue
            self.assertTrue(not traits.is_my_case(struct.typedef('container')))

    def test_declaration(self):
        cnt = (
            'std::vector<std::basic_string<char, std::char_traits<char>, ' +
            'std::allocator<char> >,std::allocator<std::basic_string<char, ' +
            'std::char_traits<char>, std::allocator<char> > > >' +
            '@::std::vector<std::basic_string<char, std::char_traits<char>, ' +
            'std::allocator<char> >,std::allocator<std::basic_string<char, ' +
            'std::char_traits<char>, std::allocator<char> > > >')
        traits = declarations.find_container_traits(cnt)
        self.assertTrue(declarations.vector_traits is traits)

    def test_element_type(self):
        do_nothing = self.global_ns.free_function('do_nothing')
        v = declarations.remove_reference(
            declarations.remove_declarated(
                do_nothing.arguments[0].decl_type))
        declarations.vector_traits.element_type(v)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
