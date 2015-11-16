# Copyright 2014-2015 Insight Software Consortium.
# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import unittest
import parser_test_case

from pygccxml import parser
from pygccxml import declarations
from pygccxml import utils


class tester_t(parser_test_case.parser_test_case_t):

    """
    Test the remove__va_list_tag option

    With CastXML and clang some __va_list_tag declarations are present in the
    tree. This options allows to remove them when parsing the xml file.

    """

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.__code = os.linesep.join(['struct a{};'])

    def test_keep_va_list_tag(self):
        utils.remove__va_list_tag = False
        src_reader = parser.source_reader_t(self.config)
        decls = declarations.make_flatten(src_reader.read_string(self.__code))

        classes = [
            i for i in decls if isinstance(i, declarations.class_t)]

        typedefs = [
            i for i in decls if isinstance(i, declarations.typedef_t)]

        variables = [
            i for i in decls if isinstance(i, declarations.variable_t)]

        tag = "__va_list_tag"

        self.assertTrue(tag in [class_.name for class_ in classes])
        self.assertTrue("a" in [class_.name for class_ in classes])
        self.assertTrue(len(classes) == 2)

        self.assertTrue(tag in [ty.name for ty in typedefs])
        self.assertTrue(len(typedefs) == 4)

        self.assertTrue(
            tag in [var.decl_string.split("::")[1] for var in variables])
        self.assertTrue(len(variables) == 4)

    def test_remove_va_list_tag(self):
        utils.remove__va_list_tag = True
        src_reader = parser.source_reader_t(self.config)
        decls = declarations.make_flatten(src_reader.read_string(self.__code))

        classes = [
            i for i in decls if isinstance(i, declarations.class_t)]

        typedefs = [
            i for i in decls if isinstance(i, declarations.typedef_t)]

        variables = [
            i for i in decls if isinstance(i, declarations.variable_t)]

        tag = "__va_list_tag"

        self.assertFalse(tag in [class_.name for class_ in classes])
        self.assertTrue("a" in [class_.name for class_ in classes])
        self.assertTrue(len(classes) == 1)

        self.assertFalse(tag in [ty.name for ty in typedefs])
        self.assertTrue(len(typedefs) == 3)

        self.assertFalse(
            tag in [var.decl_string.split("::")[1] for var in variables])
        self.assertTrue(len(variables) == 0)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
