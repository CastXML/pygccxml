# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import platform
import unittest

from . import parser_test_case

from pygccxml import parser
from pygccxml import declarations


class Test(parser_test_case.parser_test_case_t):

    """
    Test the remove__va_list_tag option

    With CastXML and clang some __va_list_tag declarations are present in the
    tree. This options allows to remove them when parsing the xml file.

    """

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.__code = os.linesep.join(['struct a{};'])
        self.known_typedefs = [
            "__int128_t", "__uint128_t", "__builtin_va_list"]
        self.known_typedefs_llvm39 = \
            self.known_typedefs + ["__builtin_ms_va_list"]
        self.known_classes = ["a", "__va_list_tag"]
        self.known_classes_llvm39 = \
            self.known_classes + ["__NSConstantString_tag"]

    def test_keep_va_list_tag(self):

        if "gccxml" in self.config.xml_generator or \
                platform.system() == 'Windows':
            return True

        self.config.flags = ["f1"]
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
        if len(classes) == 2:
            for c in self.known_classes:
                self.assertTrue(c in [cl.name for cl in classes])
        elif len(classes) == 3:
            for c in self.known_classes_llvm39:
                # This is for llvm 3.9
                self.assertTrue(c in [cl.name for cl in classes])

        self.assertTrue(len(typedefs) == 4 or len(typedefs) == 5)
        if len(typedefs) == 5:
            # This is for llvm 3.9. The class __va_list_tag struct is still
            # there but the typedef is gone
            for t in self.known_typedefs_llvm39:
                self.assertTrue(t in [ty.name for ty in typedefs])
            self.assertTrue(
                "__NSConstantString_tag" in
                [class_.name for class_ in classes])
            self.assertTrue(
                "__NSConstantString" in [ty.name for ty in typedefs])
        else:
            for t in self.known_typedefs:
                self.assertTrue(t in [ty.name for ty in typedefs])

        self.assertTrue(
            tag in [var.decl_string.split("::")[1] for var in variables])

        # 4 variables in __va_list_tag, and 4 more in __NSConstantString_tag
        # for llvm 3.9
        self.assertTrue(len(variables) == 4 or len(variables) == 8)

    def test_remove_va_list_tag(self):

        if "gccxml" in self.config.xml_generator or \
                platform.system() == 'Windows':
            return True

        self.config.flags = []
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
        self.assertTrue(len(typedefs) == 3 or len(typedefs) == 4)
        if len(typedefs) == 4:
            # This is for llvm 3.9
            for t in self.known_typedefs_llvm39:
                self.assertTrue(t in [ty.name for ty in typedefs])
            self.assertFalse(
                "__NSConstantString_tag"
                in [class_.name for class_ in classes])
            self.assertFalse(
                "__NSConstantString" in [ty.name for ty in typedefs])
        else:
            for t in self.known_typedefs:
                self.assertTrue(t in [ty.name for ty in typedefs])

        self.assertFalse(
            tag in [var.decl_string.split("::")[1] for var in variables])
        self.assertTrue(len(variables) == 0)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
