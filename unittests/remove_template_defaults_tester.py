# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import unittest
import parser_test_case
from pygccxml import parser
from pygccxml import declarations


class tester_t(parser_test_case.parser_test_case_t):
    global_ns = None

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.header = 'remove_template_defaults.hpp'

    def setUp(self):
        if not tester_t.global_ns:
            decls = parser.parse([self.header], self.config)
            tester_t.global_ns = declarations.get_global_namespace(decls)
            tester_t.global_ns.init_optimizer()

    def test_vector(self):
        v_int = self.global_ns.typedef('v_int')
        v_traits = declarations.vector_traits
        self.failUnless('vector< int >' == v_traits.remove_defaults(v_int))
        v_string = self.global_ns.typedef('v_string')
        self.failUnless('vector< std::string >'
                        == v_traits.remove_defaults(v_string))
        v_v_int = self.global_ns.typedef('v_v_int')
        self.failUnless('vector< std::vector< int > >'
                        == v_traits.remove_defaults(v_v_int))

    def test_list(self):
        l_int = self.global_ns.typedef('l_int')
        l_traits = declarations.list_traits
        self.failUnless('list< int >' == l_traits.remove_defaults(l_int))
        l_wstring = self.global_ns.typedef('l_wstring')
        self.failUnless('list< std::wstring >'
                        == l_traits.remove_defaults(l_wstring))

    def test_deque(self):
        d_v_int = self.global_ns.typedef('d_v_int')
        d_v_traits = declarations.deque_traits
        self.failUnless('deque< std::vector< int > >'
                        == d_v_traits.remove_defaults(d_v_int))
        d_l_string = self.global_ns.typedef('d_l_string')
        self.failUnless('deque< std::list< std::string > >'
                        == d_v_traits.remove_defaults(d_l_string))

    def test_queue(self):
        q_int = self.global_ns.typedef('q_int')
        q_traits = declarations.queue_traits
        self.failUnless('queue< int >' == q_traits.remove_defaults(q_int))
        q_string = self.global_ns.typedef('q_string')
        self.failUnless('queue< std::string >'
                        == q_traits.remove_defaults(q_string))

    def test_priority_queue(self):
        pq_int = self.global_ns.typedef('pq_int')
        pq_traits = declarations.priority_queue_traits
        self.failUnless('priority_queue< int >'
                        == pq_traits.remove_defaults(pq_int))
        pq_string = self.global_ns.typedef('pq_string')
        self.failUnless('priority_queue< std::string >'
                        == pq_traits.remove_defaults(pq_string))

    def test_set(self):
        s_v_int = self.global_ns.typedef('s_v_int')
        self.failUnless('set< std::vector< int > >'
                        == declarations.set_traits.remove_defaults(s_v_int))
        s_string = self.global_ns.typedef('s_string')
        self.failUnless('set< std::string >'
                        == declarations.set_traits.remove_defaults(s_string))

    def test_multiset(self):
        ms_v_int = self.global_ns.typedef('ms_v_int')
        ms_v_traits = declarations.multiset_traits
        self.failUnless('multiset< std::vector< int > >'
                        == ms_v_traits.remove_defaults(ms_v_int))
        ms_string = self.global_ns.typedef('ms_string')
        self.failUnless('multiset< std::string >'
                        == ms_v_traits.remove_defaults(ms_string))

    def test_map(self):
        m_i2d = self.global_ns.typedef('m_i2d')
        self.failUnless('map< int, double >'
                        == declarations.map_traits.remove_defaults(m_i2d))
        m_wstr2d = self.global_ns.typedef('m_wstr2d')
        self.failUnless('map< std::wstring, double >'
                        == declarations.map_traits.remove_defaults(m_wstr2d))
        m_v_i2m_wstr2d = self.global_ns.typedef('m_v_i2m_wstr2d')
        self.failUnless(
            'map< const std::vector< int >, std::map< std::wstring, double > >'
            == declarations.map_traits.remove_defaults(m_v_i2m_wstr2d))

    def test_multimap(self):
        mm_i2d = self.global_ns.typedef('mm_i2d')
        mm_traits = declarations.multimap_traits
        self.failUnless('multimap< int, double >'
                        == mm_traits.remove_defaults(mm_i2d))
        mm_wstr2d = self.global_ns.typedef('mm_wstr2d')
        self.failUnless('multimap< const std::wstring, double >'
                        == mm_traits.remove_defaults(mm_wstr2d))
        mm_v_i2mm_wstr2d = self.global_ns.typedef('mm_v_i2mm_wstr2d')
        self.failUnless(
            ('multimap< const std::vector< int >, ' +
                'const std::multimap< const std::wstring, double > >')
            == mm_traits.remove_defaults(mm_v_i2mm_wstr2d))

    def test_hash_set(self):
        hs_v_int = self.global_ns.typedef('hs_v_int')
        hs_traits = declarations.hash_set_traits
        self.failUnless('hash_set< std::vector< int > >'
                        == hs_traits.remove_defaults(hs_v_int),
                        hs_traits.remove_defaults(hs_v_int))
        hs_string = self.global_ns.typedef('hs_string')
        self.failUnless('hash_set< std::string >'
                        == hs_traits.remove_defaults(hs_string))

    def test_hash_multiset(self):
        mhs_v_int = self.global_ns.typedef('mhs_v_int')
        mhs_traits = declarations.hash_multiset_traits
        self.failUnless('hash_multiset< std::vector< int > >'
                        == mhs_traits.remove_defaults(mhs_v_int))
        mhs_string = self.global_ns.typedef('mhs_string')
        self.failUnless('hash_multiset< std::string >'
                        == mhs_traits.remove_defaults(mhs_string))

    def test_hash_map(self):
        hm_i2d = self.global_ns.typedef('hm_i2d')
        hm_traits = declarations.hash_map_traits
        self.failUnless('hash_map< int, double >'
                        == hm_traits.remove_defaults(hm_i2d))
        hm_wstr2d = self.global_ns.typedef('hm_wstr2d')
        self.failUnless('hash_map< std::wstring, double >'
                        == hm_traits.remove_defaults(hm_wstr2d))

    def test_hash_multimap(self):
        hmm_i2d = self.global_ns.typedef('hmm_i2d')
        hmm_traits = declarations.hash_multimap_traits
        self.failUnless('hash_multimap< int, double >'
                        == hmm_traits.remove_defaults(hmm_i2d))
        hmm_wstr2d = self.global_ns.typedef('hmm_wstr2d')
        self.failUnless('hash_multimap< const std::wstring, double >'
                        == hmm_traits.remove_defaults(hmm_wstr2d))
        hmm_v_i2mm_wstr2d = self.global_ns.typedef('hmm_v_i2mm_wstr2d')

        possible_values = (
            'hash_multimap< const std::vector< int >, ' +
            'const __gnu_cxx::hash_multimap< const std::wstring, double > >',
            'hash_multimap< const std::vector< int >, ' +
            'const std::hash_multimap< const std::wstring, double > >',
            'hash_multimap< const std::vector< int >, ' +
            'const stdext::hash_multimap< const std::wstring, double > >')

        self.failUnless(hmm_traits.remove_defaults(hmm_v_i2mm_wstr2d)
                        in possible_values)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
