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


class tester_src_t(parser_test_case.parser_test_case_t):
    # tester source reader
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'typedefs_base.hpp'
        self.declarations = None

    def setUp(self):
        if not self.declarations:
            self.declarations = parser.parse([self.header], self.config)
            self.global_ns = declarations.find_declaration(
                self.declarations,
                type=declarations.namespace_t,
                name='::')
            self.global_ns.init_optimizer()

    def test(self):
        item_cls = self.global_ns.class_(name='item_t')
        self.failUnless(item_cls, "unable to find class 'item_t'")
        self.failUnless(len(item_cls.aliases) == 1)
        self.failUnless(item_cls.aliases[0].name == 'Item')


class tester_prj_t(parser_test_case.parser_test_case_t):
    # tester source reader
    COMPILATION_MODE = parser.COMPILATION_MODE.FILE_BY_FILE

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.declarations = None

    def setUp(self):
        if not self.declarations:
            self.declarations = parser.parse(
                ['typedefs1.hpp',
                 'typedefs2.hpp'],
                self.config,
                self.COMPILATION_MODE)

    def test(self):
        item_cls = declarations.find_declaration(
            self.declarations,
            type=declarations.class_t,
            name='item_t')
        self.failUnless(item_cls, "unable to find class 'item_t'")
        self.failUnless(len(item_cls.aliases) == 3)
        expected_aliases = set(['Item', 'Item1', 'Item2'])
        real_aliases = set([typedef.name for typedef in item_cls.aliases])
        self.failUnless(real_aliases == expected_aliases)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_src_t))
    suite.addTest(unittest.makeSuite(tester_prj_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
