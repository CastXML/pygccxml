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
        self.header = 'string_traits.hpp'
        self.global_ns = None

    def setUp(self):
        if not tester_t.global_ns:
            decls = parser.parse([self.header], self.config)
            tester_t.global_ns = declarations.get_global_namespace(decls)
        self.global_ns = tester_t.global_ns

    def validate_yes(self, ns, controller):
        for typedef in ns.typedefs():
            self.failUnless(controller(typedef.type))

    def validate_no(self, ns, controller):
        for typedef in ns.typedefs():
            self.failUnless(not controller(typedef.type))

    def test_string(self):
        string_traits = self.global_ns.namespace('string_traits')
        self.validate_yes(
            string_traits.namespace('yes'),
            declarations.is_std_string)
        self.validate_no(
            string_traits.namespace('no'),
            declarations.is_std_string)

    def test_wstring(self):
        wstring_traits = self.global_ns.namespace('wstring_traits')
        self.validate_yes(
            wstring_traits.namespace('yes'),
            declarations.is_std_wstring)
        self.validate_no(
            wstring_traits.namespace('no'),
            declarations.is_std_wstring)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
