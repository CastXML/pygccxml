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


class tester_impl_t(parser_test_case.parser_test_case_t):
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = os.path.join(
            autoconfig.data_directory,
            'declarations_enums.hpp')
        self.cache_file = os.path.join(
            autoconfig.data_directory,
            'pygccxml.cache')
        if os.path.exists(self.cache_file) and os.path.isfile(self.cache_file):
            os.remove(self.cache_file)

    def test_cache(self):
        cache = parser.file_cache_t(self.cache_file)
        reader = parser.source_reader_t(self.config, cache)
        decls1 = reader.read_file(self.header)
        cache.flush()
        cache = parser.file_cache_t(self.cache_file)
        reader = parser.source_reader_t(self.config, cache)
        decls2 = reader.read_file(self.header)

        enum_matcher = declarations.declaration_matcher_t(
            name="EColor",
            decl_type=declarations.enumeration_t)

        color1 = declarations.matcher.get_single(enum_matcher, decls1)
        color2 = declarations.matcher.get_single(enum_matcher, decls2)
        self.failUnless(color1.values == color2.values)

# there is no progress with this parser
# class synopsis_tester_t( tester_impl_t ):
#    CXX_PARSER_CFG = autoconfig.cxx_parsers_cfg.synopsis


class gccxml_tester_t(tester_impl_t):
    CXX_PARSER_CFG = autoconfig.cxx_parsers_cfg.gccxml


def create_suite():
    suite = unittest.TestSuite()
    # suite.addTest( unittest.makeSuite(synopsis_tester_t))
    suite.addTest(unittest.makeSuite(gccxml_tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
