# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

TEST_FILES = ["remove_template_defaults.hpp", "indexing_suites2.hpp"]


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    global_ns.init_optimizer()
    return global_ns


def __cmp_traits(global_ns, typedef, expected, partial_name, key_type=None):
    if isinstance(typedef, str):
        typedef = global_ns.typedef(typedef)
    traits = declarations.find_container_traits(typedef)
    assert traits is not None
    assert traits == expected
    cls = declarations.remove_declarated(typedef)
    assert declarations.find_container_traits(cls) == expected
    assert cls.partial_name == partial_name
    cls = traits.class_declaration(cls)
    assert traits.element_type(typedef) is not None
    assert cls.cache.container_element_type is not None

    if key_type:
        assert traits.is_mapping(typedef) is not None
        real_key_type = traits.key_type(typedef)
        assert real_key_type.decl_string == key_type
        assert cls.cache.container_key_type is not None
    else:
        assert traits.is_sequence(typedef)


def test_find_traits(global_ns):
    __cmp_traits(
        global_ns,
        "v_int",
        declarations.vector_traits,
        "vector<int>"
    )
    __cmp_traits(
        global_ns,
        "l_int",
        declarations.list_traits,
        "list<int>"
    )
    __cmp_traits(
        global_ns,
        "d_v_int",
        declarations.deque_traits,
        "deque<std::vector<int>>"
    )
    __cmp_traits(
        global_ns, "q_int",
        declarations.queue_traits,
        "queue<int>"
    )
    __cmp_traits(
        global_ns, "pq_int",
        declarations.priority_queue_traits,
        "priority_queue<int>"
    )
    __cmp_traits(
        global_ns, "s_v_int",
        declarations.set_traits,
        "set<std::vector<int>>"
    )
    __cmp_traits(
        global_ns,
        "ms_v_int",
        declarations.multiset_traits,
        "multiset<std::vector<int>>",
    )
    __cmp_traits(
        global_ns, "m_i2d",
        declarations.map_traits,
        "map<int, double>",
        "int"
    )
    __cmp_traits(
        global_ns,
        "mm_i2d",
        declarations.multimap_traits,
        "multimap<int, double>",
        "int",
    )
    __cmp_traits(
        global_ns,
        "hs_v_int",
        declarations.unordered_set_traits,
        "unordered_set<std::vector<int>>",
    )
    __cmp_traits(
        global_ns,
        "mhs_v_int",
        declarations.unordered_multiset_traits,
        "unordered_multiset<std::vector<int>>",
    )
    __cmp_traits(
        global_ns,
        "hm_i2d",
        declarations.unordered_map_traits,
        "unordered_map<int, double>",
        "int",
    )
    __cmp_traits(
        global_ns,
        "hmm_i2d",
        declarations.unordered_multimap_traits,
        "unordered_multimap<int, double>",
        "int",
    )


def test_multimap(global_ns):
    m = global_ns.class_(lambda decl: decl.name.startswith("multimap"))
    declarations.find_container_traits(m)
    assert m.partial_name == "multimap<int, int>"


def test_recursive_partial_name(global_ns):
    f1 = global_ns.free_function("f1")
    t1 = declarations.class_traits.get_declaration(f1.arguments[0].decl_type)
    assert "type<std::set<std::vector<int>>>" == t1.partial_name


def test_remove_defaults_partial_name_namespace(global_ns):
    f2 = global_ns.free_function("f2")
    type_info = f2.return_type
    traits = declarations.find_container_traits(type_info)
    cls = traits.class_declaration(type_info)
    decl_string = cls.partial_decl_string
    key_type_string = traits.key_type(type_info).partial_decl_string
    assert decl_string.startswith("::std::")
    assert key_type_string.startswith("::std::")


def test_from_ogre():
    x = (
        "map<std::string, bool (*)(std::string&, "
        + "Ogre::MaterialScriptContext&), std::less<std::string>, "
        + "std::allocator<std::pair<std::string const, bool (*)"
        + "(std::string&, Ogre::MaterialScriptContext&)>>>"
    )
    ct = declarations.find_container_traits(x)
    ct.remove_defaults(x)


def test_infinite_loop(global_ns):
    rt = global_ns.free_function("test_infinite_loop").return_type
    map_traits = declarations.find_container_traits(rt)
    assert map_traits == declarations.map_traits
    elem = map_traits.element_type(rt)
    assert elem.decl_string == "int"
