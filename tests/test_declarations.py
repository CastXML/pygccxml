# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

TEST_FILES = [
    "declarations_enums.hpp",
    "declarations_variables.hpp",
    "declarations_calldef.hpp",
]


@pytest.fixture
def global_ns_fixture_all_at_once():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    return global_ns


@pytest.fixture
def global_ns_fixture_file_by_file():
    COMPILATION_MODE = parser.COMPILATION_MODE.FILE_BY_FILE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    return global_ns


@pytest.fixture
def global_ns(request):
    return request.getfixturevalue(request.param)


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once",
        "global_ns_fixture_file_by_file",
    ],
    indirect=True,
)
def test_enumeration_t(global_ns):
    enum = global_ns.enumeration("ENumbers")
    expected_values = list(
        zip(
            ["e%d" % index for index in range(10)],
            [index for index in range(10)]
        )
    )
    assert expected_values == enum.values


def test_namespace():
    pass  # tested in core_tester


def test_types():
    pass  # tested in core_tester


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once",
        "global_ns_fixture_file_by_file",
    ],
    indirect=True,
)
def test_variables(global_ns, helpers):
    global_ns.namespace("variables")
    initialized = global_ns.variable(name="initialized")

    expected_value = "10122004"
    assert initialized.value == expected_value
    helpers._test_type_composition(
        initialized.decl_type,
        declarations.const_t,
        declarations.long_unsigned_int_t
    )

    m_mutable = global_ns.variable(name="m_mutable")
    assert m_mutable.type_qualifiers.has_static is False
    assert m_mutable.type_qualifiers.has_mutable is True

    # External static variable
    extern_var = global_ns.variable(name="extern_var")
    assert extern_var.type_qualifiers.has_extern is True
    assert extern_var.type_qualifiers.has_static is False
    assert extern_var.type_qualifiers.has_mutable is False

    # Static variable
    static_var = global_ns.variable(name="static_var")
    assert static_var.type_qualifiers.has_static is True
    assert static_var.type_qualifiers.has_extern is False
    assert static_var.type_qualifiers.has_mutable is False

    ssv_static_var = global_ns.variable(name="ssv_static_var")
    assert ssv_static_var.type_qualifiers.has_static is True
    assert ssv_static_var.type_qualifiers.has_extern is False
    assert ssv_static_var.type_qualifiers.has_mutable is False

    ssv_static_var_value = global_ns.variable(name="ssv_static_var_value")
    assert ssv_static_var_value.type_qualifiers.has_static is True
    assert ssv_static_var_value.type_qualifiers.has_extern is False
    assert ssv_static_var_value.type_qualifiers.has_mutable is False


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once",
        "global_ns_fixture_file_by_file",
    ],
    indirect=True,
)
def test_calldef_free_functions(global_ns, helpers):
    ns = global_ns.namespace("calldef")

    no_return_no_args = ns.free_function("no_return_no_args")

    helpers._test_calldef_return_type(no_return_no_args, declarations.void_t)
    assert no_return_no_args.has_extern is False

    # Static_call is explicetely defined as extern, this works with gccxml
    # and castxml.
    static_call = ns.free_function("static_call")
    assert static_call is not None

    return_no_args = ns.free_function("return_no_args")
    helpers._test_calldef_return_type(return_no_args, declarations.int_t)
    # from now there is no need to check return type.
    no_return_1_arg = ns.free_function(name="no_return_1_arg")
    assert no_return_1_arg is not None
    assert no_return_1_arg.arguments[0].name in ["arg", "arg0"]
    helpers._test_calldef_args(
        no_return_1_arg,
        [
            declarations.argument_t(
                name=no_return_1_arg.arguments[0].name,
                decl_type=declarations.int_t()
            )
        ],
    )

    return_default_args = ns.free_function("return_default_args")
    assert return_default_args.arguments[0].name in ["arg", "arg0"]
    assert return_default_args.arguments[1].name in ["arg1", "flag"]
    helpers._test_calldef_args(
        return_default_args,
        [
            declarations.argument_t(
                name=return_default_args.arguments[0].name,
                decl_type=declarations.int_t(),
                default_value="1",
            ),
            declarations.argument_t(
                name=return_default_args.arguments[1].name,
                decl_type=declarations.bool_t(),
                default_value="false",
            ),
        ],
    )
    helpers._test_calldef_exceptions(global_ns, return_default_args, [])


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once",
        "global_ns_fixture_file_by_file",
    ],
    indirect=True,
)
def test_calldef_member_functions(global_ns, helpers):
    struct_calldefs = global_ns.class_("calldefs_t")

    member_inline_call = struct_calldefs.member_function("member_inline_call")
    helpers._test_calldef_args(
        member_inline_call,
        [declarations.argument_t(name="i", decl_type=declarations.int_t())],
    )

    member_const_call = struct_calldefs.member_function("member_const_call")
    assert member_const_call.has_const
    assert member_const_call.virtuality == \
        declarations.VIRTUALITY_TYPES.NOT_VIRTUAL

    member_virtual_call = struct_calldefs.member_function(
        name="member_virtual_call"
        )
    assert member_virtual_call.virtuality == \
        declarations.VIRTUALITY_TYPES.VIRTUAL

    member_pure_virtual_call = struct_calldefs.member_function(
        "member_pure_virtual_call"
    )
    assert (
        member_pure_virtual_call.virtuality
        == declarations.VIRTUALITY_TYPES.PURE_VIRTUAL
    )

    static_call = struct_calldefs.member_function("static_call")
    assert static_call.has_static is True


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once",
        "global_ns_fixture_file_by_file",
    ],
    indirect=True,
)
def test_constructors_destructors(global_ns, helpers):
    struct_calldefs = global_ns.class_("calldefs_t")

    destructor = struct_calldefs.calldef("~calldefs_t")
    helpers._test_calldef_args(destructor, [])
    helpers._test_calldef_return_type(destructor, None.__class__)

    # well, now we have a few functions ( constructors ) with the same
    # name, there is no easy way to find the desired one. Well in my case
    # I have only 4 constructors
    # 1. from char
    # 2. from (int,double)
    # 3. default
    # 4. copy constructor
    constructor_found = struct_calldefs.constructors("calldefs_t")
    assert len(constructor_found) == 5
    assert (
        len(
            [
                constructor
                for constructor in constructor_found
                if declarations.is_copy_constructor(constructor)
            ]
        )
        == 1
    )
    # there is nothing to check about constructors - I know the
    # implementation of parser.
    # In this case it doesn't different from any other function

    c = struct_calldefs.constructor("calldefs_t", arg_types=["char"])
    assert c.explicit is True

    arg_type = declarations.declarated_t(global_ns.class_("some_exception_t"))
    c = struct_calldefs.constructor("calldefs_t", arg_types=[arg_type])
    assert c.explicit is False


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once",
        "global_ns_fixture_file_by_file",
    ],
    indirect=True,
)
def test_operator_symbol(global_ns):
    calldefs_operators = ["=", "=="]
    calldefs_cast_operators = ["char *", "double"]
    struct_calldefs = global_ns.class_("calldefs_t")
    assert struct_calldefs is not None
    for decl in struct_calldefs.declarations:
        if not isinstance(decl, declarations.operator_t):
            continue
        if not isinstance(decl, declarations.casting_operator_t):
            assert decl.symbol in calldefs_operators
        else:
            assert decl.return_type.decl_string in calldefs_cast_operators


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once",
        "global_ns_fixture_file_by_file",
    ],
    indirect=True,
)
def test_ellipsis(global_ns):
    ns = global_ns.namespace("ellipsis_tester")
    do_smth = ns.member_function("do_smth")
    assert do_smth.has_ellipsis is True
    do_smth_else = ns.free_function("do_smth_else")
    assert do_smth_else.has_ellipsis is True
