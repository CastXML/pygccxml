# Copyright 2014-2016 Insight Software Consortium.
# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import sys
from platform import system
import unittest
import autoconfig
import parser_test_case
import subprocess
from pygccxml import binary_parsers
from pygccxml import utils
from pygccxml import parser
from pygccxml import declarations


class tester_t(parser_test_case.parser_test_case_t):

    global_ns = None

    @property
    def known_issues(self):
        if 'nt' == os.name:
            issues = set([
                # array as function argument: 'int FA10_i_i(int * const)'
                # pointer to function: 'void myclass_t::set_do_smth(void
                # (**)(std::auto_ptr<number_t> &))'
                # pointer to functions: 'void (**
                # myclass_t::get_do_smth(void))(std::auto_ptr<number_t> &)'
                '?FA10_i_i@@YAHQAH@Z',
                ('?set_do_smth@myclass_t@@QAEXPAP6AXAAV?' +
                    '$auto_ptr@Vnumber_t@@@std@@@Z@Z'),
                ('?get_do_smth@myclass_t@@QAEPAP6AXAAV?' +
                    '$auto_ptr@Vnumber_t@@@std@@@ZXZ')
            ])
            if 'msvc71' == utils.native_compiler.get_gccxml_compiler():
                # missing reference in argument - compiler issue
                # ('std::auto_ptr<number_t> &
                # std::auto_ptr<number_t>::operator=' +
                # '(std::auto_ptr_ref<number_t>)')
                issues.add((
                    '??4?$auto_ptr@Vnumber_t@@@std@@QAEAAV01@U?' +
                    '$auto_ptr_ref@Vnumber_t@@@1@@Z'))
            return issues
        else:
            return set([
                # even c++filt fails
                # typeinfo name for number_t
                # it seems that gccxml doesn't report this one
                # the following are some global symbols
                '_ZNSt8auto_ptrI8number_tEcvSt12auto_ptr_refIT_EIS0_EEv',
                '_ZTI8number_t', '_ZTV8number_t', '_ZTS8number_t',
                '_ZNSt12auto_ptr_refI8number_tEC1EPS0_', '_init', '_edata',
                '_fini', '_end'])

    def __init__(self, *args):
        parser_test_case.parser_test_case_t.__init__(self, *args)
        self.binary_parsers_dir = os.path.join(
            autoconfig.data_directory,
            'binary_parsers')
        self.header = os.path.join(self.binary_parsers_dir, r'mydll.h')
        self.map_file = os.path.join(
            self.binary_parsers_dir,
            'binaries',
            'mydll.map')
        self.dll_file = os.path.join(
            self.binary_parsers_dir,
            'binaries',
            'mydll.dll')
        system_name = system()
        if system_name == 'Darwin':
            ext = '.dylib'
        elif system_name == 'Windows':
            ext = '.dll'
        else:
            ext = '.so'
        self.so_file = os.path.join(
            self.binary_parsers_dir,
            'binaries',
            'libmydll%s' %
            ext)

    def setUp(self):
        if not tester_t.global_ns:
            decls = parser.parse([self.header], self.config)
            tester_t.global_ns = declarations.get_global_namespace(decls)
            tester_t.global_ns.init_optimizer()

            process = subprocess.Popen(
                args='scons msvc_compiler=%s' %
                autoconfig.cxx_parsers_cfg.gccxml.compiler,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=self.binary_parsers_dir)
            process.stdin.close()

            while process.poll() is None:
                line = process.stdout.readline()
                print(line.rstrip())
            for line in process.stdout.readlines():
                print(line.rstrip())
            if process.returncode:
                raise RuntimeError(
                    ("unable to compile binary parser module. " +
                        "See output for the errors."))

    def is_included(self, decl):
        if not isinstance(
                decl, (declarations.calldef_t, declarations.variable_t)):
            return False
        for suffix in [self.header, 'memory']:
            if decl.location.file_name.endswith(suffix):
                return True
        else:
            return False

    def __tester_impl(self, fname, expected_symbols):
        symbols, parser = binary_parsers.merge_information(
            self.global_ns, fname, runs_under_unittest=True)
        # this doesn't work reliably
        # self.assertTrue(
        #    len(symbols) == expected_symbols,
        # "The expected symbols number(%d),
        # is different from the actual one(%d)"
        # % ( expected_symbols, len(symbols) ) )
        self.assertTrue('identity' in symbols)

        msg = []
        blob_names = set()
        for blob in parser.loaded_symbols:
            if isinstance(blob, tuple):
                blob = blob[0]
            if 'nt' == os.name:
                # TODO: find out where undecorate function is exposed on linux
                undname = binary_parsers.undecorate_blob(blob)
                if "`" in undname:
                    continue
            blob_names.add(blob)

        decl_blob_names = set(symbols.keys())

        issuperset = decl_blob_names.issuperset(blob_names)
        if not issuperset:
            common = decl_blob_names.intersection(blob_names)

            decl_blob_names.difference_update(common)
            blob_names.difference_update(common)
            if not self.known_issues.issubset(blob_names):
                blob_names.difference_update(self.known_issues)
                if sys.version_info[0] == 2 and sys.version_info[1] == 5:
                    if 0 == len(decl_blob_names) and 0 == len(blob_names):
                        return
                msg.append("decl_blob_names :")
                for i in decl_blob_names:
                    msg.append('\t==>%s<==' % i)
                msg.append("blob_names :")
                for i in blob_names:
                    msg.append('\t==>%s<==' % i)

                self.fail(os.linesep.join(msg))

    def test_map_file(self):
        if 'nt' == os.name:
            self.__tester_impl(self.map_file, 71)

    def test_dll_file(self):
        if 'nt' == os.name:
            self.__tester_impl(self.dll_file, 71)

    def test_z_compare_parsers(self):
        if 'nt' != os.name:
            return
        dsymbols, dparser = binary_parsers.merge_information(
            self.global_ns, self.dll_file, runs_under_unittest=True)
        msymbols, mparser = binary_parsers.merge_information(
            self.global_ns, self.map_file, runs_under_unittest=True)

        self.assertTrue(
            len(dparser.loaded_symbols) == len(mparser.loaded_symbols))

        was_error = False
        for blob, decl in dsymbols.items():
            if blob not in msymbols:
                was_error = True
                print(
                    '\n%s could not be found in .map file' %
                    binary_parsers.undecorate_blob(blob))
                # self.assertTrue( blob in msymbols,
                # binary_parsers.undecorate_blob( blob ) )
            else:
                mdecl = msymbols[blob]
                self.assertTrue(mdecl is decl)
        self.assertTrue(was_error is False)

    def test_so_file(self):
        if 'posix' in os.name:
            self.__tester_impl(self.so_file, 64)

    def dont_test_print(self):
        """primary used for debugging"""
        symbols, parser = binary_parsers.merge_information(
            self.global_ns, self.so_file, runs_under_unittest=True)
        for f in self.global_ns.calldefs(allow_empty=True, recursive=True):
            print(binary_parsers.format_decl(f, 'nm'))

        for v in self.global_ns.variables(allow_empty=True, recursive=True):
            print(binary_parsers.format_decl(v, 'nm'))


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
