# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


TEST_FILES = [
    "type_traits.hpp",
]


@pytest.fixture
def decls():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    return decls


def __test_type_category(decls, ns_name, controller):
    ns_control = declarations.find_declaration(
        decls,
        decl_type=declarations.namespace_t,
        name=ns_name)
    assert ns_control is not None
    ns_yes = declarations.find_declaration(
        ns_control,
        decl_type=declarations.namespace_t,
        name='yes')
    assert ns_yes is not None
    ns_no = declarations.find_declaration(
        ns_control,
        decl_type=declarations.namespace_t,
        name='no')
    assert ns_no is not None
    for decl in ns_yes.declarations:
        if isinstance(decl, declarations.variable_t):
            assert controller(decl.decl_type) is not None
        elif isinstance(decl, declarations.calldef_t) and \
                decl.name.startswith('test_'):
            continue
        else:
            assert controller(decl) is not None
    for decl in ns_no.declarations:
        if isinstance(decl, declarations.calldef_t) and \
                decl.name.startswith('test_'):
            continue
        val = controller(decl)
        # TODO: This looks bad and should be improved?
        # Why a boolean or None?
        assert val is False or val is None


def __test_type_transformation(decls, ns_name, transformer):
    ns_control = declarations.find_declaration(
        decls,
        decl_type=declarations.namespace_t,
        name=ns_name)
    assert ns_control is not None
    ns_before = declarations.find_declaration(
        ns_control,
        decl_type=declarations.namespace_t,
        name='before')
    assert ns_before is not None
    ns_after = declarations.find_declaration(
        ns_control,
        decl_type=declarations.namespace_t,
        name='after')
    assert ns_after is not None

    for tbefore in ns_before.declarations:
        tafter = declarations.find_declaration(
            ns_after,
            name=tbefore.name)
        assert tafter is not None
        transformed = transformer(tbefore)
        assert declarations.is_same(
                transformed,
                tafter) is True


def test_is_enum(decls):
    __test_type_category(decls, 'is_enum', declarations.is_enum)


def test_is_void(decls):
    __test_type_category(decls, 'is_void', declarations.is_void)


def test_is_bool(decls):
    __test_type_category(decls, 'is_bool', declarations.is_bool)


def test_is_integral(decls):
    __test_type_category(decls, 'is_integral', declarations.is_integral)


def test_is_pointer(decls):
    __test_type_category(decls, 'is_pointer', declarations.is_pointer)


def test_is_void_pointer(decls):
    __test_type_category(
        decls, 'is_void_pointer', declarations.is_void_pointer)


def test_is_const(decls):
    __test_type_category(decls, 'is_const', declarations.is_const)


def test_is_volatile(decls):
    __test_type_category(decls, 'is_volatile', declarations.is_volatile)


def test_is_reference(decls):
    __test_type_category(decls, 'is_reference', declarations.is_reference)


def test_is_floating_point(decls):
    __test_type_category(
        decls,
        'is_floating_point',
        declarations.is_floating_point)


def test_is_array(decls):
    __test_type_category(decls, 'is_array', declarations.is_array)


def test_is_fundamental(decls):
    __test_type_category(
        decls,
        'is_fundamental',
        declarations.is_fundamental)


def test_is_noncopyable(decls):
    __test_type_category(
        decls,
        'is_noncopyable',
        declarations.is_noncopyable)


def test_is_std_ostream(decls):
    __test_type_category(
        decls,
        'is_std_ostream',
        declarations.is_std_ostream)


def test_is_std_wostream(decls):
    __test_type_category(
        decls,
        'is_std_wostream',
        declarations.is_std_wostream)


def test_is_calldef_pointer(decls):
    __test_type_category(
        decls,
        'is_calldef_pointer',
        declarations.is_calldef_pointer)


def test_has_trivial_constructor(decls):
    __test_type_category(
        decls,
        'has_trivial_constructor',
        declarations.has_trivial_constructor)


def test_has_public_constructor(decls):
    __test_type_category(
        decls,
        'has_public_constructor',
        declarations.has_public_constructor)


def test_has_public_destructor(decls):
    __test_type_category(
        decls,
        'has_public_destructor',
        declarations.has_public_destructor)


def test_has_any_non_copyconstructor(decls):
    __test_type_category(
        decls,
        'has_any_non_copyconstructor',
        declarations.has_any_non_copyconstructor)


def test_has_copy_constructor(decls):
    __test_type_category(
        decls,
        'has_copy_constructor',
        declarations.has_copy_constructor)


def test_is_base_and_derived(decls):
    ns = declarations.find_declaration(
        decls,
        decl_type=declarations.namespace_t,
        name='is_base_and_derived')
    assert ns is not None
    base = declarations.find_declaration(
        ns.declarations,
        decl_type=declarations.class_t,
        name='base')
    derived = declarations.find_declaration(
        ns.declarations,
        decl_type=declarations.class_t,
        name='derived')
    assert base is not None
    assert derived is not None
    assert declarations.is_base_and_derived(base, derived) is True
    assert declarations.is_base_and_derived(base, (derived, derived)) is True

    unrelated1 = declarations.find_declaration(
        ns.declarations,
        decl_type=declarations.class_t,
        name='unrelated1')

    unrelated2 = declarations.find_declaration(
        ns.declarations,
        decl_type=declarations.class_t,
        name='unrelated2')
    assert base is not None
    assert derived is not None
    assert declarations.is_base_and_derived(unrelated1, unrelated2) is False


def test_is_same():
    assert declarations.is_same(
        declarations.int_t,
        declarations.int_t) is True
    assert declarations.is_same(
        declarations.int_t,
        declarations.float_t) is False


def test_remove_const(decls):
    __test_type_transformation(
        decls,
        'remove_const',
        declarations.remove_const)


def test_remove_reference(decls):
    __test_type_transformation(
        decls,
        'remove_reference',
        declarations.remove_reference)


def test_remove_volatile(decls):
    __test_type_transformation(
        decls,
        'remove_volatile',
        declarations.remove_volatile)


def test_remove_cv(decls):
    __test_type_transformation(
        decls, 'remove_cv', declarations.remove_cv
    )


def test_remove_pointer(decls):
    __test_type_transformation(
        decls,
        'remove_pointer',
        declarations.remove_pointer)


def test_is_unary_binary_operator(decls):
    operator_not = declarations.find_declaration(
        decls,
        decl_type=declarations.operator_t,
        fullname='::is_unary_operator::dummy::operator!')
    assert operator_not is not None
    assert declarations.is_unary_operator(operator_not) is True
    assert declarations.is_binary_operator(operator_not) is False

    operator_class_p = declarations.find_declaration(
        decls,
        decl_type=declarations.operator_t,
        fullname='::is_unary_operator::dummy::operator+')
    assert operator_class_p is not None
    assert declarations.is_unary_operator(operator_class_p) is False
    assert declarations.is_binary_operator(operator_class_p) is True

    operator_class_pp = declarations.find_declaration(
        decls,
        decl_type=declarations.operator_t,
        fullname='::is_unary_operator::dummy::operator++')
    assert operator_class_pp is not None
    assert declarations.is_unary_operator(operator_class_pp) is True
    assert declarations.is_binary_operator(operator_class_pp) is False

    operator_pp = declarations.find_declaration(
        decls,
        decl_type=declarations.operator_t,
        fullname='::is_unary_operator::operator++')
    assert operator_pp is not None
    assert declarations.is_unary_operator(operator_pp) is True
    assert declarations.is_binary_operator(operator_pp) is False

    operator_mm = declarations.find_declaration(
        decls,
        decl_type=declarations.operator_t,
        fullname='::is_unary_operator::operator*')
    assert operator_mm is not None
    assert declarations.is_unary_operator(operator_mm) is False
    assert declarations.is_binary_operator(operator_mm) is True

    operator_pe = declarations.find_declaration(
        decls,
        decl_type=declarations.operator_t,
        fullname='::is_unary_operator::operator+=')
    assert operator_pe is not None
    assert declarations.is_unary_operator(operator_pe) is False
    assert declarations.is_binary_operator(operator_pe) is True


def __is_convertible_impl(decl):
    defs = decl.bases[0].related_class.declarations
    source_type = declarations.find_declaration(defs, name='source_type')
    target_type = declarations.find_declaration(defs, name='target_type')
    expected_type = declarations.find_declaration(
        defs,
        name='expected',
        decl_type=declarations.enumeration_t)
    expected_value = bool(expected_type.get_name2value_dict()['value'])
    assert expected_value == declarations.is_convertible(
        source_type,
        target_type
    )


def test_is_convertible(decls):
    ns_is_convertible = declarations.find_declaration(
        decls,
        decl_type=declarations.namespace_t,
        name="is_convertible")

    assert ns_is_convertible is not None
    for tester in [
        decl for decl in ns_is_convertible.declarations if
            decl.name.startswith('x')]:
        __is_convertible_impl(tester)


def test_missing_decls():
    config = autoconfig.cxx_parsers_cfg.config
    code = "struct const_item{ const int values[10]; };"
    global_ns = parser.parse_string(code, config)[0]
    ci = global_ns.class_('const_item')
    assert len(ci.declarations) == 3


def test_get_declaration():
    code = """
        namespace A{
        struct B{
            int c;
        };

        template <class T>
        struct C: public T{
            int d;
        };

        template <class T>
        struct D{
            int dD;
        };

        typedef C<B> easy;
        typedef D<easy> Deasy;

        inline void instantiate(){
            int val = sizeof(easy);
        }

        }
    """

    global_ns = parser.parse_string(
        code,
        autoconfig.cxx_parsers_cfg.config)
    global_ns = declarations.get_global_namespace(global_ns)
    easy = global_ns.typedef('easy')
    declarations.class_traits.get_declaration(easy)
    deasy = global_ns.typedef('Deasy')
    d_a = declarations.class_traits.get_declaration(deasy)
    assert isinstance(d_a, declarations.class_types)
