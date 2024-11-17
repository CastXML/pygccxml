# Copyright 2014-2020 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


TEST_FILES = [
    "test_comments.hpp",
]


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    INIT_OPTIMIZER = True
    config = autoconfig.cxx_parsers_cfg.config.clone()
    config.castxml_epic_version = 1
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    if INIT_OPTIMIZER:
        global_ns.init_optimizer()
    return global_ns


def _check_comment_content(list, comment_decl):
    if comment_decl.text:
        assert list == comment_decl.text
    else:
        print("No text in comment to check")


def test_comments(global_ns):
    """
    Check the comment parsing
    """
    tnamespace = global_ns.namespace("comment")

    assert "comment" in dir(tnamespace)
    _check_comment_content(
        [
            "//! Namespace Comment",
            "//! Across multiple lines"
        ],
        tnamespace.comment
    )

    tenumeration = tnamespace.enumeration("com_enum")
    assert "comment" in dir(tenumeration)
    _check_comment_content(
        ['/// Outside Class enum comment'],
        tenumeration.comment
    )

    tclass = tnamespace.class_("test")
    assert "comment" in dir(tclass)
    _check_comment_content(
        ["/** class comment */"],
        tclass.comment
    )

    tcls_enumeration = tclass.enumeration("test_enum")
    assert "comment" in dir(tcls_enumeration)
    _check_comment_content(
        ['/// inside class enum comment'],
        tcls_enumeration.comment
    )

    tmethod = tclass.member_functions()[0]

    assert "comment" in dir(tmethod)
    _check_comment_content(
        ["/// cxx comment", "/// with multiple lines"],
        tmethod.comment
    )

    tconstructor = tclass.constructors()[0]

    assert "comment" in dir(tconstructor)
    _check_comment_content(
        ["/** doc comment */"],
        tconstructor.comment
    )

    for indx, cmt in enumerate(
                [
                    '//! mutable field comment',
                    "/// bit field comment"
                ]
            ):
        tvariable = tclass.variables()[indx]
        assert "comment" in dir(tvariable)
        _check_comment_content([cmt], tvariable.comment)
