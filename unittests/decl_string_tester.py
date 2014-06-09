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
import autoconfig
import parser_test_case
from pygccxml import parser
from pygccxml import declarations


class tester_t(parser_test_case.parser_test_case_t):
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    global_ns = None

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = os.path.join(
            autoconfig.data_directory,
            'declarations_calldef.hpp')
        self.template = """
        //test generated declaration string using gcc(xml) compiler
        #include "declarations_calldef.hpp"
        void test_generated_decl_string( %s );
        """

    def setUp(self):
        if not tester_t.global_ns:
            decls = parser.parse([self.header], self.config)
            tester_t.global_ns = declarations.get_global_namespace(decls)
            tester_t.global_ns.init_optimizer()

    def test_member_function(self):
        member_inline_call = self.global_ns.mem_fun('member_inline_call')
        decls = parser.parse_string(
            self.template %
            member_inline_call.decl_string,
            self.config)
        self.failUnless(
            decls,
            "Created decl_string for member function containes mistake")

    def test_free_function(self):
        return_default_args = self.global_ns.free_fun('return_default_args')
        decls = parser.parse_string(
            self.template %
            return_default_args.decl_string,
            self.config)
        self.failUnless(
            decls,
            "Created decl_string for global function containes mistake")

    def test_all_mem_and_free_funs(self):
        ns = self.global_ns.ns('::declarations::calldef')
        for f in ns.mem_funs():
            decls = parser.parse_string(
                self.template %
                f.decl_string,
                self.config)
            self.failUnless(
                decls,
                "Created decl_string for member function containes mistake")
        for f in ns.free_funs():
            decls = parser.parse_string(
                self.template %
                f.decl_string,
                self.config)
            self.failUnless(
                decls,
                "Created decl_string for member function containes mistake")


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
