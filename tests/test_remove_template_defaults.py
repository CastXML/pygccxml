# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import platform

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations
from pygccxml import utils

TEST_FILES = [
    'remove_template_defaults.hpp'
]


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    config = autoconfig.cxx_parsers_cfg.config.clone()
    if platform.system() == "Darwin":
        config.cflags = "-std=c++11 -Dat_quick_exit=atexit -Dquick_exit=exit"
        # https://fr.mathworks.com/matlabcentral/answers/2013982-clibgen-generatelibrarydefinition-error-the-global-scope-has-no-quick_exit-on-mac-m2#answer_1439856
        # https://github.com/jetbrains/kotlin/commit/d50f585911dedec5723213da8835707ac95e1c01
    else:
        config.cflags = "-std=c++11"
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    global_ns.init_optimizer()
    return global_ns


def test_vector(global_ns):
    v_int = global_ns.typedef('v_int')
    v_traits = declarations.vector_traits
    assert 'vector<int>' == v_traits.remove_defaults(v_int)
    v_string = global_ns.typedef('v_string')
    assert 'vector<std::string>' == \
        v_traits.remove_defaults(v_string)
    v_v_int = global_ns.typedef('v_v_int')
    assert 'vector<std::vector<int>>' == \
        v_traits.remove_defaults(v_v_int)


def test_list(global_ns):
    l_int = global_ns.typedef('l_int')
    l_traits = declarations.list_traits
    assert 'list<int>' == l_traits.remove_defaults(l_int)
    l_wstring = global_ns.typedef('l_wstring')
    assert 'list<std::wstring>' == l_traits.remove_defaults(l_wstring)


def test_deque(global_ns):
    d_v_int = global_ns.typedef('d_v_int')
    d_v_traits = declarations.deque_traits
    assert 'deque<std::vector<int>>' == \
        d_v_traits.remove_defaults(d_v_int)
    d_l_string = global_ns.typedef('d_l_string')
    assert 'deque<std::list<std::string>>' == \
        d_v_traits.remove_defaults(d_l_string)


def test_queue(global_ns):
    q_int = global_ns.typedef('q_int')
    q_traits = declarations.queue_traits
    assert 'queue<int>' == q_traits.remove_defaults(q_int)
    q_string = global_ns.typedef('q_string')
    assert 'queue<std::string>' == q_traits.remove_defaults(q_string)


def test_priority_queue(global_ns):
    pq_int = global_ns.typedef('pq_int')
    pq_traits = declarations.priority_queue_traits
    assert 'priority_queue<int>' == pq_traits.remove_defaults(pq_int)
    pq_string = global_ns.typedef('pq_string')
    assert 'priority_queue<std::string>' == \
        pq_traits.remove_defaults(pq_string)


def test_set(global_ns):
    s_v_int = global_ns.typedef('s_v_int')
    assert 'set<std::vector<int>>' == \
        declarations.set_traits.remove_defaults(s_v_int)
    s_string = global_ns.typedef('s_string')
    assert 'set<std::string>' == \
        declarations.set_traits.remove_defaults(s_string)


def test_multiset(global_ns):
    ms_v_int = global_ns.typedef('ms_v_int')
    ms_v_traits = declarations.multiset_traits
    assert 'multiset<std::vector<int>>' == \
        ms_v_traits.remove_defaults(ms_v_int)
    ms_string = global_ns.typedef('ms_string')
    assert 'multiset<std::string>' == \
        ms_v_traits.remove_defaults(ms_string)


def test_map(global_ns):
    m_i2d = global_ns.typedef('m_i2d')
    assert 'map<int, double>' == \
        declarations.map_traits.remove_defaults(m_i2d)
    m_wstr2d = global_ns.typedef('m_wstr2d')
    assert 'map<std::wstring, double>' == \
        declarations.map_traits.remove_defaults(m_wstr2d)
    m_v_i2m_wstr2d = global_ns.typedef('m_v_i2m_wstr2d')
    m = 'map<const std::vector<int>, std::map<std::wstring, double>>'
    assert m == declarations.map_traits.remove_defaults(m_v_i2m_wstr2d)


def test_multimap(global_ns):
    mm_i2d = global_ns.typedef('mm_i2d')
    mm_traits = declarations.multimap_traits
    assert 'multimap<int, double>' == mm_traits.remove_defaults(mm_i2d)
    mm_wstr2d = global_ns.typedef('mm_wstr2d')
    assert 'multimap<const std::wstring, double>' == \
        mm_traits.remove_defaults(mm_wstr2d)
    mm_v_i2mm_wstr2d = global_ns.typedef('mm_v_i2mm_wstr2d')
    assert ('multimap<const std::vector<int>, ' +
            'const std::multimap<const std::wstring, double>>') == \
        mm_traits.remove_defaults(mm_v_i2mm_wstr2d)


def test_hash_set(global_ns):
    hs_v_int = global_ns.typedef('hs_v_int')
    hs_traits = declarations.unordered_set_traits
    name = 'unordered_set'
    assert (name + '<std::vector<int>>') == \
        hs_traits.remove_defaults(hs_v_int), \
        hs_traits.remove_defaults(hs_v_int)
    hs_string = global_ns.typedef('hs_string')
    assert (name + '<std::string>') == \
        hs_traits.remove_defaults(hs_string)


def test_hash_multiset(global_ns):
    mhs_v_int = global_ns.typedef('mhs_v_int')
    mhs_traits = declarations.unordered_multiset_traits
    name = 'unordered_multiset'
    assert (name + '<std::vector<int>>') == \
        mhs_traits.remove_defaults(mhs_v_int)
    mhs_string = global_ns.typedef('mhs_string')
    assert (name + '<std::string>') == \
        mhs_traits.remove_defaults(mhs_string)


def test_hash_map(global_ns):
    hm_i2d = global_ns.typedef('hm_i2d')
    hm_traits = declarations.unordered_map_traits
    name = 'unordered_map'
    assert (name + '<int, double>') == \
        hm_traits.remove_defaults(hm_i2d)
    hm_wstr2d = global_ns.typedef('hm_wstr2d')
    assert (name + '<std::wstring, double>') == \
        hm_traits.remove_defaults(hm_wstr2d)


def test_hash_multimap(global_ns):
    hmm_i2d = global_ns.typedef('hmm_i2d')
    hmm_traits = declarations.unordered_multimap_traits
    name = 'unordered_multimap'
    assert (name + '<int, double>') == \
        hmm_traits.remove_defaults(hmm_i2d)
    hmm_wstr2d = global_ns.typedef('hmm_wstr2d')
    assert (name + '<const std::wstring, double>') == \
        hmm_traits.remove_defaults(hmm_wstr2d)

    hmm_v_i2mm_wstr2d = global_ns.typedef('hmm_v_i2mm_wstr2d')

    hmm_traits_value = hmm_traits.remove_defaults(hmm_v_i2mm_wstr2d)

    possible_values = (
        name + '<const std::vector<int>, ' +
        'const __gnu_cxx::' + name + '<const std::wstring, double>>',
        name + '<const std::vector<int>, ' +
        'const std::' + utils.get_tr1(hmm_traits_value) + name +
        '<const std::wstring, double>>',
        name + '<const std::vector<int>, ' +
        'const stdext::' + name + '<const std::wstring, double>>')

    assert hmm_traits_value in possible_values, hmm_traits_value
