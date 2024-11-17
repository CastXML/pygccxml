# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import utils
from pygccxml import parser
from pygccxml import declarations


def is_sub_path(root, some_path):
    root = utils.normalize_path(root)
    some_path = utils.normalize_path(some_path)
    return some_path.startswith(root)


TEST_FILES = [
    "core_ns_join_1.hpp",
    "core_ns_join_2.hpp",
    "core_ns_join_3.hpp",
    "core_membership.hpp",
    "core_class_hierarchy.hpp",
    "core_types.hpp",
    "core_diamand_hierarchy_base.hpp",
    "core_diamand_hierarchy_derived1.hpp",
    "core_diamand_hierarchy_derived2.hpp",
    "core_diamand_hierarchy_final_derived.hpp",
    "core_overloads_1.hpp",
    "core_overloads_2.hpp",
    "abstract_classes.hpp",
]


@pytest.fixture
def global_ns_fixture_all_at_once1():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    INIT_OPTIMIZER = True
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    if INIT_OPTIMIZER:
        global_ns.init_optimizer()
    return global_ns


@pytest.fixture
def global_ns_fixture_all_at_once2():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    INIT_OPTIMIZER = False
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    if INIT_OPTIMIZER:
        global_ns.init_optimizer()
    return global_ns


@pytest.fixture
def global_ns_fixture_file_by_file1():
    COMPILATION_MODE = parser.COMPILATION_MODE.FILE_BY_FILE
    INIT_OPTIMIZER = True
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    if INIT_OPTIMIZER:
        global_ns.init_optimizer()
    return global_ns


@pytest.fixture
def global_ns_fixture_file_by_file2():
    COMPILATION_MODE = parser.COMPILATION_MODE.FILE_BY_FILE
    INIT_OPTIMIZER = False
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    if INIT_OPTIMIZER:
        global_ns.init_optimizer()
    return global_ns


@pytest.fixture
def global_ns(request):
    return request.getfixturevalue(request.param)


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once1",
        "global_ns_fixture_all_at_once2",
        "global_ns_fixture_file_by_file1",
        "global_ns_fixture_file_by_file2",
    ],
    indirect=True,
)
def test_top_parent(global_ns):
    enum = global_ns.enumeration("::ns::ns32::E33")
    assert global_ns is enum.top_parent


# tests namespaces join functionality. described in gccxml.py
@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once1",
        "global_ns_fixture_all_at_once2",
        "global_ns_fixture_file_by_file1",
        "global_ns_fixture_file_by_file2",
    ],
    indirect=True,
)
def test_nss_join(global_ns):
    # list of all namespaces
    nss = ["::ns", "::ns::ns12", "::ns::ns22", "::ns::ns32"]
    # list of all namespaces that have unnamed namespace
    # unnamed_nss = nss[1:] doing nothing with this list ?
    # list of all enums [0:2] [3:5] [6:8] - has same parent
    enums = [
        "::E11",
        "::E21",
        "::E31",
        "::ns::E12",
        "::ns::E22",
        "::ns::E32",
        "::ns::ns12::E13",
        "::ns::ns22::E23",
        "::ns::ns32::E33",
    ]

    for ns in nss:
        global_ns.namespace(ns)

    for enum in enums:
        global_ns.enumeration(enum)

    ns = global_ns.namespace(nss[0])
    ns12 = global_ns.namespace(nss[1])
    ns22 = global_ns.namespace(nss[2])
    ns32 = global_ns.namespace(nss[3])
    assert ns is ns12.parent is ns22.parent is ns32.parent

    e11 = global_ns.enumeration(enums[0])
    e21 = global_ns.enumeration(enums[1])
    e31 = global_ns.enumeration(enums[2])
    assert e11.parent is e21.parent is e31.parent

    nse12 = global_ns.enumeration(enums[3])
    nse23 = global_ns.enumeration(enums[4])
    nse33 = global_ns.enumeration(enums[5])
    assert ns is nse12.parent is nse23.parent is nse33.parent


def _test_ns_membership(ns, enum_name):
    unnamed_enum = ns.enumeration(
        lambda d: d.name == ""
        and is_sub_path(autoconfig.data_directory, d.location.file_name),
        recursive=False,
    )
    assert unnamed_enum in ns.declarations

    enum = ns.enumeration(enum_name, recursive=False)
    assert enum in ns.declarations
    assert unnamed_enum.parent is ns
    assert enum.parent is ns


def _test_class_membership(class_inst, enum_name, access):
    # getting enum through get_members function
    nested_enum1 = class_inst.enumeration(
        name=enum_name, function=declarations.access_type_matcher_t(access)
    )

    # getting enum through declarations property
    nested_enum2 = class_inst.enumeration(enum_name)

    # it shoud be same object
    assert nested_enum1 is nested_enum2

    # check whether we meaning same class instance
    assert class_inst is nested_enum1.parent is nested_enum2.parent


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once1",
        "global_ns_fixture_all_at_once2",
        "global_ns_fixture_file_by_file1",
        "global_ns_fixture_file_by_file2",
    ],
    indirect=True,
)
# test gccxml_file_reader_t._update_membership algorithm
def test_membership(global_ns):
    core_membership = global_ns.namespace("membership")
    _test_ns_membership(global_ns, "EGlobal")
    _test_ns_membership(core_membership.namespace("enums_ns"), "EWithin")
    _test_ns_membership(core_membership.namespace(""), "EWithinUnnamed")
    class_nested_enums = core_membership.class_("class_for_nested_enums_t")
    _test_class_membership(
        class_nested_enums,
        "ENestedPublic",
        declarations.ACCESS_TYPES.PUBLIC
    )
    _test_class_membership(
        class_nested_enums,
        "ENestedProtected",
        declarations.ACCESS_TYPES.PROTECTED
    )
    _test_class_membership(
        class_nested_enums,
        "ENestedPrivate",
        declarations.ACCESS_TYPES.PRIVATE
    )


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once1",
        "global_ns_fixture_all_at_once2",
        "global_ns_fixture_file_by_file1",
        "global_ns_fixture_file_by_file2",
    ],
    indirect=True,
)
def test_mangled_name_namespace(global_ns):
    std = global_ns.namespace("std")
    assert std is not None
    assert std.mangled is None


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once1",
        "global_ns_fixture_all_at_once2",
        "global_ns_fixture_file_by_file1",
        "global_ns_fixture_file_by_file2",
    ],
    indirect=True,
)
def test_mangled_name_functions(global_ns):
    # This works with gccxml and castxml
    ns = global_ns.namespace("overloads")
    do_nothing = ns.calldefs("do_nothing", recursive=False)
    assert do_nothing.mangled is not None


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once1",
        "global_ns_fixture_all_at_once2",
        "global_ns_fixture_file_by_file1",
        "global_ns_fixture_file_by_file2",
    ],
    indirect=True,
)
def test_mangled_name_variable(global_ns):
    # This works with gccxml and castxml
    var_inst = global_ns.variable("array255")
    assert var_inst.mangled is not None


def _test_is_based_and_derived(base, derived, access):
    dhi_v = declarations.hierarchy_info_t(derived, access, True)
    dhi_not_v = declarations.hierarchy_info_t(derived, access, False)
    assert dhi_v in base.derived or dhi_not_v in base.derived

    bhi_v = declarations.hierarchy_info_t(base, access, True)
    bhi_not_v = declarations.hierarchy_info_t(base, access, False)

    assert bhi_v in derived.bases or bhi_not_v in derived.bases


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once1",
        "global_ns_fixture_all_at_once2",
        "global_ns_fixture_file_by_file1",
        "global_ns_fixture_file_by_file2",
    ],
    indirect=True,
)
def test_class_hierarchy(global_ns):
    class_hierarchy = global_ns.namespace("class_hierarchy")

    base = class_hierarchy.class_("base_t")
    other_base = class_hierarchy.class_("other_base_t")
    derived_public = class_hierarchy.class_("derived_public_t")
    derived_protected = class_hierarchy.class_("derived_protected_t")
    derived_private = class_hierarchy.class_("derived_private_t")
    multi_derived = class_hierarchy.class_("multi_derived_t")

    _test_is_based_and_derived(
        base,
        derived_public,
        declarations.ACCESS_TYPES.PUBLIC
    )
    _test_is_based_and_derived(
        base,
        derived_protected,
        declarations.ACCESS_TYPES.PROTECTED
    )
    _test_is_based_and_derived(
        base,
        derived_private,
        declarations.ACCESS_TYPES.PRIVATE
    )
    _test_is_based_and_derived(
        base, multi_derived,
        declarations.ACCESS_TYPES.PROTECTED
    )
    _test_is_based_and_derived(
        other_base,
        multi_derived,
        declarations.ACCESS_TYPES.PRIVATE
    )
    _test_is_based_and_derived(
        derived_private,
        multi_derived,
        declarations.ACCESS_TYPES.PRIVATE
    )


def _test_is_same_bases(derived1, derived2):
    bases1 = set(
        [id(hierarchy_info.related_class) for hierarchy_info in derived1.bases]
    )
    bases2 = set(
        [id(hierarchy_info.related_class) for hierarchy_info in derived2.bases]
    )
    assert bases1 == bases2


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once1",
        "global_ns_fixture_all_at_once2",
        "global_ns_fixture_file_by_file1",
        "global_ns_fixture_file_by_file2",
    ],
    indirect=True,
)
def test_class_join(global_ns):
    diamand_hierarchy = global_ns.namespace("diamand_hierarchy")
    base = diamand_hierarchy.class_("base_t")
    derived1 = diamand_hierarchy.class_("derived1_t")
    derived2 = diamand_hierarchy.class_("derived2_t")
    final_derived = diamand_hierarchy.class_("final_derived_t")

    _test_is_based_and_derived(
        base,
        derived1,
        declarations.ACCESS_TYPES.PUBLIC
    )
    _test_is_based_and_derived(
        base,
        derived2,
        declarations.ACCESS_TYPES.PUBLIC
    )
    _test_is_based_and_derived(
        derived1,
        final_derived,
        declarations.ACCESS_TYPES.PUBLIC
    )
    _test_is_based_and_derived(
        derived2,
        final_derived,
        declarations.ACCESS_TYPES.PUBLIC
    )
    _test_is_same_bases(derived1, derived2)


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once1",
        "global_ns_fixture_all_at_once2",
        "global_ns_fixture_file_by_file1",
        "global_ns_fixture_file_by_file2",
    ],
    indirect=True,
)
def test_fundamental_types(global_ns):
    # check whether all build in types could be constructed
    errors = []
    for (
        fundamental_type_name,
        fundamental_type,
    ) in declarations.FUNDAMENTAL_TYPES.items():
        if "complex" in fundamental_type_name:
            continue  # I check this in an other tester
        if isinstance(
            fundamental_type, (declarations.int128_t, declarations.uint128_t)
        ):
            continue  # I don't have test case for this
        if isinstance(fundamental_type, declarations.java_fundamental_t):
            continue  # I don't check this at all
        typedef_name = "typedef_" + fundamental_type_name.replace(" ", "_")
        typedef = global_ns.decl(
            decl_type=declarations.typedef_t,
            name=typedef_name
        )
        assert typedef is not None
        if typedef.decl_type.decl_string != fundamental_type.decl_string:
            errors.append(
                "there is a difference between typedef base type "
                + "name('%s') and expected one('%s')"
                % (typedef.decl_type.decl_string, fundamental_type.decl_string)
            )
    assert len(errors) == 0


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once1",
        "global_ns_fixture_all_at_once2",
        "global_ns_fixture_file_by_file1",
        "global_ns_fixture_file_by_file2",
    ],
    indirect=True,
)
def test_compound_types(global_ns, helpers):
    typedef_inst = global_ns.decl(
        decl_type=declarations.typedef_t, name="typedef_const_int"
    )
    helpers._test_type_composition(
        typedef_inst.decl_type, declarations.const_t, declarations.int_t
    )

    typedef_inst = global_ns.decl(
        decl_type=declarations.typedef_t, name="typedef_pointer_int"
    )
    helpers._test_type_composition(
        typedef_inst.decl_type, declarations.pointer_t, declarations.int_t
    )

    typedef_inst = global_ns.decl(
        decl_type=declarations.typedef_t, name="typedef_reference_int"
    )
    helpers._test_type_composition(
        typedef_inst.decl_type, declarations.reference_t, declarations.int_t
    )

    typedef_inst = global_ns.decl(
        decl_type=declarations.typedef_t,
        name="typedef_const_unsigned_int_const_pointer",
    )
    helpers._test_type_composition(
        typedef_inst.decl_type,
        declarations.const_t,
        declarations.pointer_t
    )
    helpers._test_type_composition(
        typedef_inst.decl_type.base,
        declarations.pointer_t,
        declarations.const_t
    )
    helpers._test_type_composition(
        typedef_inst.decl_type.base.base,
        declarations.const_t,
        declarations.unsigned_int_t,
    )

    typedef_inst = global_ns.decl(
        decl_type=declarations.typedef_t,
        name="typedef_volatile_int"
    )
    helpers._test_type_composition(
        typedef_inst.decl_type,
        declarations.volatile_t,
        declarations.int_t
    )

    var_inst = global_ns.variable("array255")
    helpers._test_type_composition(
        var_inst.decl_type,
        declarations.array_t,
        declarations.int_t
    )

    typedef_inst = global_ns.decl(
        decl_type=declarations.typedef_t,
        name="typedef_EFavoriteDrinks"
    )
    assert isinstance(typedef_inst.decl_type, declarations.declarated_t)
    enum_declaration = global_ns.enumeration("EFavoriteDrinks")
    assert typedef_inst.decl_type.declaration is enum_declaration


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once1",
        "global_ns_fixture_all_at_once2",
        "global_ns_fixture_file_by_file1",
        "global_ns_fixture_file_by_file2",
    ],
    indirect=True,
)
def test_free_function_type(global_ns, helpers):
    function_ptr = global_ns.decl(
        decl_type=declarations.typedef_t,
        name="function_ptr")
    helpers._test_type_composition(
        function_ptr.decl_type,
        declarations.pointer_t,
        declarations.free_function_type_t,
    )
    function_type = function_ptr.decl_type.base
    assert isinstance(function_type.return_type, declarations.int_t)
    assert len(function_type.arguments_types) == 2
    assert isinstance(function_type.arguments_types[0], declarations.int_t)
    assert isinstance(function_type.arguments_types[1], declarations.double_t)


@pytest.mark.parametrize(
        "global_ns",
        ["global_ns_fixture_all_at_once1"],
        indirect=True
    )
def test_member_function_type(global_ns, helpers):
    function_ptr = global_ns.decl(
        decl_type=declarations.typedef_t, name="member_function_ptr_t"
    )
    helpers._test_type_composition(
        function_ptr.decl_type,
        declarations.pointer_t,
        declarations.member_function_type_t,
    )

    function_type = function_ptr.decl_type.base

    members_pointers = global_ns.class_("members_pointers_t")
    assert function_type.class_inst.declaration is members_pointers

    assert isinstance(function_type.return_type, declarations.int_t)
    assert len(function_type.arguments_types) == 1
    assert isinstance(function_type.arguments_types[0], declarations.double_t)
    assert function_type.has_const is True


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once1",
        "global_ns_fixture_all_at_once2",
        "global_ns_fixture_file_by_file1",
        "global_ns_fixture_file_by_file2",
    ],
    indirect=True,
)
def test_member_variable_type(global_ns, helpers):
    mv = global_ns.decl(
        decl_type=declarations.typedef_t,
        name="member_variable_ptr_t"
    )
    helpers._test_type_composition(
        mv.decl_type,
        declarations.pointer_t,
        declarations.member_variable_type_t
    )

    members_pointers = global_ns.class_("members_pointers_t")
    assert members_pointers is not None
    helpers._test_type_composition(
        mv.decl_type.base,
        declarations.member_variable_type_t,
        declarations.declarated_t,
    )
    mv_type = mv.decl_type.base
    assert mv_type.base.declaration == members_pointers


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once1",
        "global_ns_fixture_all_at_once2",
        "global_ns_fixture_file_by_file1",
        "global_ns_fixture_file_by_file2",
    ],
    indirect=True,
)
def test_overloading(global_ns):
    ns = global_ns.namespace("overloads")

    do_nothings = ns.calldefs("do_nothing", recursive=False)
    assert 4 == len(do_nothings)
    for index, do_nothing in enumerate(do_nothings):
        others = do_nothings[:index] + do_nothings[index + 1:]
        if set(do_nothing.overloads) != set(others):
            print("\nexisting: ")
            for x in do_nothing.overloads:
                print(str(x))
            print("\nexpected: ")
            for x in others:
                print(str(x))

        assert set(do_nothing.overloads) == set(others)


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once1",
        "global_ns_fixture_all_at_once2",
        "global_ns_fixture_file_by_file1",
        "global_ns_fixture_file_by_file2",
    ],
    indirect=True,
)
def test_abstract_classes(global_ns):
    ns = global_ns.namespace("abstract_classes")
    abstract_i = ns.class_("abstract_i")
    assert abstract_i.is_abstract is True
    derived_abstract_i = ns.class_("derived_abstract_i")
    assert derived_abstract_i.is_abstract is True
    implementation = ns.class_("implementation")
    assert implementation.is_abstract is not True


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once1",
        "global_ns_fixture_all_at_once2",
        "global_ns_fixture_file_by_file1",
        "global_ns_fixture_file_by_file2",
    ],
    indirect=True,
)
def test_byte_size(global_ns):
    mptrs = global_ns.class_("members_pointers_t")
    assert mptrs.byte_size != 0


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once1",
        "global_ns_fixture_all_at_once2",
        "global_ns_fixture_file_by_file1",
        "global_ns_fixture_file_by_file2",
    ],
    indirect=True,
)
def test_byte_align(global_ns):
    mptrs = global_ns.class_("members_pointers_t")
    assert mptrs.byte_align != 0


@pytest.mark.parametrize(
    "global_ns",
    [
        "global_ns_fixture_all_at_once1",
        "global_ns_fixture_all_at_once2",
        "global_ns_fixture_file_by_file1",
        "global_ns_fixture_file_by_file2",
    ],
    indirect=True,
)
def test_byte_offset(global_ns):
    mptrs = global_ns.class_("members_pointers_t")
    assert mptrs.variable("xxx").byte_offset != 0
