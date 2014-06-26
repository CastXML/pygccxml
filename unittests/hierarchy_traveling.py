# =============================================================================
#
#  Copyright Insight Software Consortium
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

# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import unittest
import parser_test_case
from pygccxml import parser
from pygccxml import declarations


class tester_t(parser_test_case.parser_test_case_t):

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.__code = os.linesep.join(['struct a{};',
                                       'struct b{};',
                                       'struct c{};',
                                       'struct d : public a{};',
                                       'struct e : public a, public b{};',
                                       'struct f{};',
                                       'struct g : public d, public f{};',
                                       'struct h : public f{};',
                                       'struct i : public h, public g{};'])

        self.__recursive_bases = {'a': set(),
                                  'b': set(),
                                  'c': set(),
                                  'd': set(['a']),
                                  'e': set(['a', 'b']),
                                  'f': set(),
                                  'g': set(['d', 'f', 'a']),
                                  'h': set(['f']),
                                  'i': set(['h', 'g', 'd', 'f', 'a'])}

        self.__recursive_derived = {
            'a': set(['d', 'e', 'g', 'i']),
            'b': set(['e']),
            'c': set(),
            'd': set(['g', 'i']),
            'e': set(),
            'f': set(['g', 'h', 'i']),
            'g': set(['i']),
            'h': set(['i']),
            'i': set()}

    def test_recursive_bases(self):
        src_reader = parser.source_reader_t(self.config)
        decls = declarations.make_flatten(src_reader.read_string(self.__code))
        classes = [
            inst for inst in decls if isinstance(inst, declarations.class_t)]
        for class_ in classes:
            self.failUnless(class_.name in self.__recursive_bases)
            all_bases = class_.recursive_bases
            control_bases = self.__recursive_bases[class_.name]
            self.failUnless(len(control_bases) == len(all_bases))
            all_bases_names = [hi.related_class.name for hi in all_bases]
            self.failUnless(set(all_bases_names) == control_bases)

    def test_recursive_derived(self):
        src_reader = parser.source_reader_t(self.config)
        decls = declarations.make_flatten(src_reader.read_string(self.__code))
        classes = [
            inst for inst in decls if isinstance(
                inst,
                declarations.class_t)]
        for class_ in classes:
            self.failUnless(class_.name in self.__recursive_derived)
            all_derived = class_.recursive_derived
            control_derived = self.__recursive_derived[class_.name]
            self.failUnless(len(control_derived) == len(all_derived))
            all_derived_names = [hi.related_class.name for hi in all_derived]
            self.failUnless(set(all_derived_names) == control_derived)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
