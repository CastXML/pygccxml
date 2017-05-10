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
        self.headers = ['remove_template_defaults.hpp', 'indexing_suites2.hpp']

    def setUp(self):
        if not Test.global_ns:
            decls = parser.parse(self.headers, self.config)
            Test.global_ns = declarations.get_global_namespace(decls)
            Test.global_ns.init_optimizer()
            Test.xml_generator_from_xml_file = \
                self.config.xml_generator_from_xml_file
        self.xml_generator_from_xml_file = Test.xml_generator_from_xml_file
        self.global_ns = Test.global_ns

    def __cmp_traits(self, typedef, expected, partial_name, key_type=None):
        if utils.is_str(typedef):
            typedef = self.global_ns.typedef(typedef)
        traits = declarations.find_container_traits(typedef)
        self.assertTrue(
            traits,
            'container traits for "%s" not found' %
            str(typedef))
        self.assertTrue(
            traits is expected,
            'container "%s", expected %s_traits, got %s_traits' %
            (str(typedef),
             expected.name(),
             traits.name()))
        cls = declarations.remove_declarated(typedef)
        self.assertTrue(declarations.find_container_traits(cls) is expected)
        self.assertTrue(cls.partial_name == partial_name)
        cls = traits.class_declaration(cls)

        self.assertTrue(traits.element_type(typedef))
        self.assertTrue(
            cls.cache.container_element_type,
            "For some reason cache was not updated")

        if key_type:
            self.assertTrue(traits.is_mapping(typedef))
            real_key_type = traits.key_type(typedef)
            self.assertTrue(
                real_key_type.decl_string == key_type,
                'Error extracting key type.  Expected type "%s", got "%s"' %
                (key_type,
                 real_key_type.decl_string))
            self.assertTrue(
                cls.cache.container_key_type,
                "For some reason cache was not updated")
        else:
            self.assertTrue(traits.is_sequence(typedef))

    def test_find_traits(self):
        self.__cmp_traits('v_int', declarations.vector_traits, "vector< int >")
        self.__cmp_traits('l_int', declarations.list_traits, "list< int >")
        self.__cmp_traits(
            'd_v_int',
            declarations.deque_traits,
            "deque< std::vector< int > >")
        self.__cmp_traits('q_int', declarations.queue_traits, "queue< int >")
        self.__cmp_traits(
            'pq_int',
            declarations.priority_queue_traits,
            "priority_queue< int >")
        self.__cmp_traits(
            's_v_int',
            declarations.set_traits,
            "set< std::vector< int > >")
        self.__cmp_traits(
            'ms_v_int',
            declarations.multiset_traits,
            "multiset< std::vector< int > >")
        self.__cmp_traits(
            'm_i2d',
            declarations.map_traits,
            "map< int, double >",
            'int')
        self.__cmp_traits(
            'mm_i2d',
            declarations.multimap_traits,
            "multimap< int, double >",
            'int')

        if self.xml_generator_from_xml_file.is_castxml:
            self.__cmp_traits(
                'hs_v_int',
                declarations.unordered_set_traits,
                "unordered_set< std::vector< int > >")
        else:
            self.__cmp_traits(
                'hs_v_int',
                declarations.hash_set_traits,
                "hash_set< std::vector< int > >")

        if self.xml_generator_from_xml_file.is_castxml:
            self.__cmp_traits(
                'mhs_v_int',
                declarations.unordered_multiset_traits,
                "unordered_multiset< std::vector< int > >")
        else:
            self.__cmp_traits(
                'mhs_v_int',
                declarations.hash_multiset_traits,
                "hash_multiset< std::vector< int > >")

        if self.xml_generator_from_xml_file.is_castxml:
            self.__cmp_traits(
                'hm_i2d',
                declarations.unordered_map_traits,
                "unordered_map< int, double >",
                'int')
        else:
            self.__cmp_traits(
                'hm_i2d',
                declarations.hash_map_traits,
                "hash_map< int, double >",
                'int')

        if self.xml_generator_from_xml_file.is_castxml:
            self.__cmp_traits(
                'hmm_i2d',
                declarations.unordered_multimap_traits,
                "unordered_multimap< int, double >",
                'int')
        else:
            self.__cmp_traits(
                'hmm_i2d',
                declarations.hash_multimap_traits,
                "hash_multimap< int, double >",
                'int')

    def test_multimap(self):
        m = self.global_ns.class_(
            lambda decl: decl.name.startswith('multimap'))
        declarations.find_container_traits(m)
        self.assertTrue(m.partial_name == 'multimap< int, int >')

    def test_recursive_partial_name(self):
        f1 = self.global_ns.free_function('f1')
        t1 = declarations.class_traits.get_declaration(
            f1.arguments[0].decl_type)
        self.assertTrue(
            'type< std::set< std::vector< int > > >' == t1.partial_name)

    def test_remove_defaults_partial_name_namespace(self):
        f2 = self.global_ns.free_function('f2')
        type_info = f2.return_type
        traits = declarations.find_container_traits(type_info)
        cls = traits.class_declaration(type_info)
        # traits.remove_defaults(type_info)
        decl_string = cls.partial_decl_string
        key_type_string = traits.key_type(type_info).partial_decl_string
        self.assertTrue(
            decl_string.startswith('::std::'),
            "declaration string %r doesn't start with 'std::'" %
            decl_string)
        self.assertTrue(
            key_type_string.startswith('::std::'),
            "key type string %r doesn't start with 'std::'" %
            key_type_string)

    @staticmethod
    def test_from_ogre():
        x = (
            'map<std::string, bool (*)(std::string&, ' +
            'Ogre::MaterialScriptContext&), std::less<std::string>, ' +
            'std::allocator<std::pair<std::string const, bool (*)' +
            '(std::string&, Ogre::MaterialScriptContext&)> > >')
        ct = declarations.find_container_traits(x)
        ct.remove_defaults(x)

    def test_infinite_loop(self):
        rt = self.global_ns.free_function('test_infinite_loop').return_type
        map_traits = declarations.find_container_traits(rt)
        self.assertTrue(map_traits is declarations.map_traits)
        elem = map_traits.element_type(rt)
        self.assertTrue(elem.decl_string == 'int')


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())


if __name__ == "__main__":
    run_suite()
