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

import os
import unittest
import parser_test_case
from pygccxml import parser
from pygccxml import declarations


class tester_1_t(parser_test_case.parser_test_case_t):
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    declarations = None

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'bit_fields.hpp'
        self.declarations = None

    def setUp(self):
        if not self.declarations:
            self.declarations = parser.parse([self.header], self.config)

    def test(self):
        criteria = declarations.variable_matcher_t(
            name='x',
            type='unsigned int')
        x = declarations.matcher.get_single(criteria, self.declarations)

        comp_str = (
            '(decl type==variable_t) and (name==x) and ' +
            '(value type==unsigned int)')
        self.failUnless(str(criteria) == comp_str)

        criteria = declarations.variable_matcher_t(
            name='::bit_fields::fields_t::x',
            type=declarations.unsigned_int_t(),
            header_dir=os.path.dirname(
                x.location.file_name),
            header_file=x.location.file_name)

        x = declarations.matcher.get_single(criteria, self.declarations)
        self.failUnless(x, "Variable was not found.")

        self.failUnless('public' == x.access_type)


class tester_2_t(parser_test_case.parser_test_case_t):
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    global_ns = None

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'vector_traits.hpp'
        self.global_ns = None

    def setUp(self):
        if not self.global_ns:
            self.global_ns = declarations.get_global_namespace(
                parser.parse([self.header], self.config))

    def test_no_defaults(self):
        self.global_ns.decls(lambda decl: 'vector<' in decl.name)
        self.global_ns.decl('vector< _0_ >')
        self.global_ns.class_('vector< std::vector< int > >')
        self.global_ns.class_('vector< std::string >')
        self.global_ns.decl('vector< const int >')


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_1_t))
    suite.addTest(unittest.makeSuite(tester_2_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
