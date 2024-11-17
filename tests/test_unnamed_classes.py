# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations
from pygccxml.declarations import type_traits


TEST_FILES = [
    "unnamed_classes.hpp",
]


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    global_ns.init_optimizer()
    return global_ns


def validate_bitfields(parent, bitfields):
    for key in bitfields:
        var = parent.variable(key)
        assert var.bits == bitfields[key]


def do_union_test(global_ns, union_name, bitfields):
    s2 = global_ns.class_('S2')
    assert declarations.is_union(s2) is False
    assert declarations.is_struct(s2) is True
    assert s2.parent.name == 'S1'
    assert declarations.is_union(s2.parent) is False

    union = s2.variable(union_name)
    assert declarations.is_union(union.decl_type) is True
    assert declarations.is_struct(union.decl_type) is False

    union_type = type_traits.remove_declarated(union.decl_type)
    validate_bitfields(union_type, bitfields)
    assert union_type.variable('raw') is not None


def test_union_Flags(global_ns):
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
    do_union_test(global_ns, 'flags', flags_bitfields)


def test_unnamed_unions(global_ns):
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
    do_union_test(global_ns, 'fileattribs', fileattribs_bitfields)


def test_anonymous_unions(global_ns):
    s3 = global_ns.class_('S3')
    assert s3.parent.name == 'S1'

    s3_vars = ['anon_mem_c', 'anon_mem_i', 's3_mem', 's2']
    for var in s3_vars:
        assert declarations.is_union(s3.variable(var).decl_type) is False
