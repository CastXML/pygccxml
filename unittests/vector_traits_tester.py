# =============================================================================
#
#  Copyright 2014 Insight Software Consortium
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0.txt
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# =============================================================================

# Copyright 2004-2013 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest
import parser_test_case
from pygccxml import parser
from pygccxml import declarations


class tester_t(parser_test_case.parser_test_case_t):
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    global_ns = None

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'vector_traits.hpp'
        self.global_ns = None

    def setUp(self):
        if not tester_t.global_ns:
            decls = parser.parse([self.header], self.config)
            tester_t.global_ns = declarations.get_global_namespace(decls)
        self.global_ns = tester_t.global_ns

    def validate_yes(self, value_type, container):
        traits = declarations.vector_traits
        self.failUnless(traits.is_my_case(container))
        self.failUnless(
            declarations.is_same(
                value_type,
                traits.element_type(container)))
        self.failUnless(traits.is_sequence(container))

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
            self.failUnless(not traits.is_my_case(struct.typedef('container')))

    def test_declaration(self):
        cnt = (
            'std::vector<std::basic_string<char, std::char_traits<char>, ' +
            'std::allocator<char> >,std::allocator<std::basic_string<char, ' +
            'std::char_traits<char>, std::allocator<char> > > >' +
            '@::std::vector<std::basic_string<char, std::char_traits<char>, ' +
            'std::allocator<char> >,std::allocator<std::basic_string<char, ' +
            'std::char_traits<char>, std::allocator<char> > > >')
        traits = declarations.find_container_traits(cnt)
        self.failUnless(declarations.vector_traits is traits)

    def test_element_type(self):
        do_nothing = self.global_ns.free_fun('do_nothing')
        v = declarations.remove_reference(
            declarations.remove_declarated(
                do_nothing.arguments[0].type))
        declarations.vector_traits.element_type(v)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
