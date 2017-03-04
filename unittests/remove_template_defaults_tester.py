# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import unittest

from . import parser_test_case

from pygccxml import parser
from pygccxml import declarations
from pygccxml import utils


class Test(parser_test_case.parser_test_case_t):
    global_ns = None

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'remove_template_defaults.hpp'

    def setUp(self):
        if not Test.global_ns:
            decls = parser.parse([self.header], self.config)
            Test.global_ns = declarations.get_global_namespace(decls)
            Test.global_ns.init_optimizer()
            Test.xml_generator_from_xml_file = \
                self.config.xml_generator_from_xml_file
        self.xml_generator_from_xml_file = Test.xml_generator_from_xml_file

    def test_vector(self):
        v_int = self.global_ns.typedef('v_int')
        v_traits = declarations.vector_traits
        self.assertTrue('vector< int >' == v_traits.remove_defaults(v_int))
        v_string = self.global_ns.typedef('v_string')
        self.assertTrue(
            'vector< std::string >' == v_traits.remove_defaults(v_string))
        v_v_int = self.global_ns.typedef('v_v_int')
        self.assertTrue(
            'vector< std::vector< int > >' ==
            v_traits.remove_defaults(v_v_int))

    def test_list(self):
        l_int = self.global_ns.typedef('l_int')
        l_traits = declarations.list_traits
        self.assertTrue('list< int >' == l_traits.remove_defaults(l_int))
        l_wstring = self.global_ns.typedef('l_wstring')
        self.assertTrue(
            'list< std::wstring >' == l_traits.remove_defaults(l_wstring))

    def test_deque(self):
        d_v_int = self.global_ns.typedef('d_v_int')
        d_v_traits = declarations.deque_traits
        self.assertTrue(
            'deque< std::vector< int > >' ==
            d_v_traits.remove_defaults(d_v_int))
        d_l_string = self.global_ns.typedef('d_l_string')
        self.assertTrue(
            'deque< std::list< std::string > >' ==
            d_v_traits.remove_defaults(d_l_string))

    def test_queue(self):
        q_int = self.global_ns.typedef('q_int')
        q_traits = declarations.queue_traits
        self.assertTrue('queue< int >' == q_traits.remove_defaults(q_int))
        q_string = self.global_ns.typedef('q_string')
        self.assertTrue(
            'queue< std::string >' == q_traits.remove_defaults(q_string))

    def test_priority_queue(self):
        pq_int = self.global_ns.typedef('pq_int')
        pq_traits = declarations.priority_queue_traits
        self.assertTrue(
            'priority_queue< int >' == pq_traits.remove_defaults(pq_int))
        pq_string = self.global_ns.typedef('pq_string')
        self.assertTrue(
            'priority_queue< std::string >' ==
            pq_traits.remove_defaults(pq_string))

    def test_set(self):
        s_v_int = self.global_ns.typedef('s_v_int')
        self.assertTrue(
            'set< std::vector< int > >' ==
            declarations.set_traits.remove_defaults(s_v_int))
        s_string = self.global_ns.typedef('s_string')
        self.assertTrue(
            'set< std::string >' ==
            declarations.set_traits.remove_defaults(s_string))

    def test_multiset(self):
        ms_v_int = self.global_ns.typedef('ms_v_int')
        ms_v_traits = declarations.multiset_traits
        self.assertTrue(
            'multiset< std::vector< int > >' ==
            ms_v_traits.remove_defaults(ms_v_int))
        ms_string = self.global_ns.typedef('ms_string')
        self.assertTrue(
            'multiset< std::string >' ==
            ms_v_traits.remove_defaults(ms_string))

    def test_map(self):
        m_i2d = self.global_ns.typedef('m_i2d')
        self.assertTrue(
            'map< int, double >' ==
            declarations.map_traits.remove_defaults(m_i2d))
        m_wstr2d = self.global_ns.typedef('m_wstr2d')
        self.assertTrue(
            'map< std::wstring, double >' ==
            declarations.map_traits.remove_defaults(m_wstr2d))
        m_v_i2m_wstr2d = self.global_ns.typedef('m_v_i2m_wstr2d')
        m = 'map< const std::vector< int >, std::map< std::wstring, double > >'
        self.assertTrue(
            m == declarations.map_traits.remove_defaults(m_v_i2m_wstr2d))

    def test_multimap(self):
        mm_i2d = self.global_ns.typedef('mm_i2d')
        mm_traits = declarations.multimap_traits
        self.assertTrue(
            'multimap< int, double >' == mm_traits.remove_defaults(mm_i2d))
        mm_wstr2d = self.global_ns.typedef('mm_wstr2d')
        self.assertTrue(
            'multimap< const std::wstring, double >' ==
            mm_traits.remove_defaults(mm_wstr2d))
        mm_v_i2mm_wstr2d = self.global_ns.typedef('mm_v_i2mm_wstr2d')
        self.assertTrue(
            ('multimap< const std::vector< int >, ' +
                'const std::multimap< const std::wstring, double > >') ==
            mm_traits.remove_defaults(mm_v_i2mm_wstr2d))

    def test_hash_set(self):
        hs_v_int = self.global_ns.typedef('hs_v_int')
        if self.xml_generator_from_xml_file.is_castxml:
            hs_traits = declarations.unordered_set_traits
            name = 'unordered_set'
        else:
            hs_traits = declarations.hash_set_traits
            name = 'hash_set'
        self.assertTrue(
            (name + '< std::vector< int > >') ==
            hs_traits.remove_defaults(hs_v_int),
            hs_traits.remove_defaults(hs_v_int))
        hs_string = self.global_ns.typedef('hs_string')
        self.assertTrue(
            (name + '< std::string >') == hs_traits.remove_defaults(hs_string))

    def test_hash_multiset(self):
        mhs_v_int = self.global_ns.typedef('mhs_v_int')
        if self.xml_generator_from_xml_file.is_castxml:
            mhs_traits = declarations.unordered_multiset_traits
            name = 'unordered_multiset'
        else:
            mhs_traits = declarations.hash_multiset_traits
            name = 'hash_multiset'
        self.assertTrue(
            (name + '< std::vector< int > >') ==
            mhs_traits.remove_defaults(mhs_v_int))
        mhs_string = self.global_ns.typedef('mhs_string')
        self.assertTrue(
            (name + '< std::string >') ==
            mhs_traits.remove_defaults(mhs_string))

    def test_hash_map(self):
        hm_i2d = self.global_ns.typedef('hm_i2d')
        if self.xml_generator_from_xml_file.is_castxml:
            hm_traits = declarations.unordered_map_traits
            name = 'unordered_map'
        else:
            hm_traits = declarations.hash_map_traits
            name = 'hash_map'
        self.assertTrue(
            (name + '< int, double >') == hm_traits.remove_defaults(hm_i2d))
        hm_wstr2d = self.global_ns.typedef('hm_wstr2d')
        self.assertTrue(
            (name + '< std::wstring, double >') ==
            hm_traits.remove_defaults(hm_wstr2d))

    def test_hash_multimap(self):
        hmm_i2d = self.global_ns.typedef('hmm_i2d')
        if self.xml_generator_from_xml_file.is_castxml:
            hmm_traits = declarations.unordered_multimap_traits
            name = 'unordered_multimap'
        else:
            hmm_traits = declarations.hash_multimap_traits
            name = 'hash_multimap'
        self.assertTrue(
            (name + '< int, double >') ==
            hmm_traits.remove_defaults(hmm_i2d))
        hmm_wstr2d = self.global_ns.typedef('hmm_wstr2d')
        self.assertTrue(
            (name + '< const std::wstring, double >') ==
            hmm_traits.remove_defaults(hmm_wstr2d))

        hmm_v_i2mm_wstr2d = self.global_ns.typedef('hmm_v_i2mm_wstr2d')

        hmm_traits_value = hmm_traits.remove_defaults(hmm_v_i2mm_wstr2d)

        possible_values = (
            name + '< const std::vector< int >, ' +
            'const __gnu_cxx::' + name + '< const std::wstring, double > >',
            name + '< const std::vector< int >, ' +
            'const std::' + utils.get_tr1(hmm_traits_value) + name +
            '< const std::wstring, double > >',
            name + '< const std::vector< int >, ' +
            'const stdext::' + name + '< const std::wstring, double > >')

        self.assertTrue(hmm_traits_value in possible_values, hmm_traits_value)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
