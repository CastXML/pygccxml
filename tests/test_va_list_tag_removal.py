# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import platform

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


"""
Test the remove__va_list_tag option

With CastXML and clang some __va_list_tag declarations are present in the
tree. This options allows to remove them when parsing the xml file.

"""


__code = os.linesep.join(['struct a{};'])
known_typedefs = ["__int128_t", "__uint128_t", "__builtin_va_list"]
known_typedefs_llvm39 = known_typedefs + ["__builtin_ms_va_list"]
known_classes = ["a", "__va_list_tag"]
known_classes_llvm39 = known_classes + ["__NSConstantString_tag"]


def test_keep_va_list_tag():

    if platform.system() == 'Windows':
        return True

    config = autoconfig.cxx_parsers_cfg.config.clone()

    config.flags = ["f1"]
    src_reader = parser.source_reader_t(config)
    decls = declarations.make_flatten(src_reader.read_string(__code))

    classes = [
        i for i in decls if isinstance(i, declarations.class_t)]

    typedefs = [
        i for i in decls if isinstance(i, declarations.typedef_t)]

    variables = [
        i for i in decls if isinstance(i, declarations.variable_t)]

    tag = "__va_list_tag"

    assert tag in [class_.name for class_ in classes]
    assert "a" in [class_.name for class_ in classes]
    if len(classes) == 2:
        for c in known_classes:
            assert c in [cl.name for cl in classes]
    elif len(classes) == 3:
        for c in known_classes_llvm39:
            # This is for llvm 3.9
            assert c in [cl.name for cl in classes]

    assert len(typedefs) == 4 or len(typedefs) == 5
    if len(typedefs) == 5:
        # This is for llvm 3.9. The class __va_list_tag struct is still
        # there but the typedef is gone
        for t in known_typedefs_llvm39:
            assert t in [ty.name for ty in typedefs]
        assert "__NSConstantString_tag" in [class_.name for class_ in classes]
        assert "__NSConstantString" in [ty.name for ty in typedefs]
    else:
        for t in known_typedefs:
            assert t in [ty.name for ty in typedefs]

    assert tag in [var.decl_string.split("::")[1] for var in variables]

    # 4 variables in __va_list_tag, and 4 more in __NSConstantString_tag
    # for llvm 3.9
    assert len(variables) == 4 or len(variables) == 8


def test_remove_va_list_tag():

    if platform.system() == 'Windows':
        return True

    config = autoconfig.cxx_parsers_cfg.config.clone()

    config.flags = []
    src_reader = parser.source_reader_t(config)
    decls = declarations.make_flatten(src_reader.read_string(__code))

    classes = [
        i for i in decls if isinstance(i, declarations.class_t)]

    typedefs = [
        i for i in decls if isinstance(i, declarations.typedef_t)]

    variables = [
        i for i in decls if isinstance(i, declarations.variable_t)]

    tag = "__va_list_tag"

    assert tag not in [class_.name for class_ in classes]
    assert "a" in [class_.name for class_ in classes]
    assert len(classes) == 1

    assert tag not in [ty.name for ty in typedefs]
    assert len(typedefs) == 3 or len(typedefs) == 4
    if len(typedefs) == 4:
        # This is for llvm 3.9
        for t in known_typedefs_llvm39:
            assert t in [ty.name for ty in typedefs]
        assert "__NSConstantString_tag" not in \
            [class_.name for class_ in classes]
        assert "__NSConstantString" not in \
            [ty.name for ty in typedefs]
    else:
        for t in known_typedefs:
            assert t in [ty.name for ty in typedefs]

    assert tag not in [var.decl_string.split("::")[1] for var in variables]
    assert len(variables) == 0
