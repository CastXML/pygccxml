# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest

from . import parser_test_case

from pygccxml import parser
from pygccxml import declarations
from pygccxml.declarations import type_traits


class Test(parser_test_case.parser_test_case_t):

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'unnamed_classes.hpp'
        self.global_ns = None

    def setUp(self):
        if not self.global_ns:
            decls = parser.parse([self.header], self.config)
            self.global_ns = declarations.get_global_namespace(decls)
            self.global_ns.init_optimizer()

    def validate_bitfields(self, parent, bitfields):
        for key in bitfields:
            var = parent.variable(key)
            self.assertEqual(var.bits, bitfields[key])

    def do_union_test(self, union_name, bitfields):
        s2 = self.global_ns.class_('S2')
        self.assertFalse(declarations.is_union(s2))
        self.assertTrue(declarations.is_struct(s2))
        self.assertEqual(s2.parent.name, 'S1')
        self.assertFalse(declarations.is_union(s2.parent))

        union = s2.variable(union_name)
        self.assertTrue(declarations.is_union(union.decl_type))
        self.assertFalse(declarations.is_struct(union.decl_type))

        union_type = type_traits.remove_declarated(union.decl_type)
        self.validate_bitfields(union_type, bitfields)
        self.assertIsNotNone(union_type.variable('raw'))

    def test_union_Flags(self):
        flags_bitfields = {
            'hasItemIdList': 1,
            'pointsToFileOrDir': 1,
            'hasDescription': 1,
            'hasRelativePath': 1,
            'hasWorkingDir': 1,
            'hasCmdLineArgs': 1,
            'hasCustomIcon': 1,
            'useWorkingDir': 1,
            'unused': 24,
        }
        self.do_union_test('flags', flags_bitfields)

    def test_unnamed_unions(self):
        fileattribs_bitfields = {
            'isReadOnly': 1,
            'isHidden': 1,
            'isSystem': 1,
            'isVolumeLabel': 1,
            'isDir': 1,
            'isModified': 1,
            'isEncrypted': 1,
            'isNormal': 1,
            'isTemporary': 1,
            'isSparse': 1,
            'hasReparsePoint': 1,
            'isCompressed': 1,
            'isOffline': 1,
            'unused': 19,
        }
        self.do_union_test('fileattribs', fileattribs_bitfields)

    def test_anonymous_unions(self):
        s3 = self.global_ns.class_('S3')
        self.assertEqual(s3.parent.name, 'S1')

        s3_vars = ['anon_mem_c', 'anon_mem_i', 's3_mem', 's2']
        for var in s3_vars:
            self.assertFalse(declarations.is_union(s3.variable(var).decl_type))


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
