# =============================================================================
#
#  Copyright Insight Software Consortium
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0.txt
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# =============================================================================

# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pprint
import unittest
import autoconfig


class parser_test_case_t(unittest.TestCase):

    CXX_PARSER_CFG = None

    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args)
        if self.CXX_PARSER_CFG:
            self.config = self.CXX_PARSER_CFG.clone()
        elif autoconfig.cxx_parsers_cfg.gccxml:
            self.config = autoconfig.cxx_parsers_cfg.gccxml.clone()
        else:
            pass

    def _test_type_composition(self, type, expected_compound, expected_base):
        self.failUnless(
            isinstance(type, expected_compound),
            "the compound type('%s') should be '%s'" %
            (type.decl_string, expected_compound.__name__))
        self.failUnless(
            isinstance(type.base, expected_base),
            "base type('%s') should be '%s'" %
            (type.decl_string,
             expected_base.__name__))

    def _test_calldef_return_type(self, calldef, expected_type):
        self.failUnless(
            isinstance(calldef.return_type, expected_type),
            ("the function's '%s' expected return type is '%s' and in " +
                "reality it is different('%s')") %
            (calldef.name, expected_type.__name__,
             calldef.return_type.__class__.__name__))

    def _test_calldef_args(self, calldef, expected_args):
        self.failUnless(
            len(calldef.arguments) == len(expected_args),
            ("the function's '%s' expected number of arguments is '%d' and " +
                "in reality it is different('%d')") %
            (calldef.name,
             len(expected_args),
             len(calldef.arguments)))
        for ordinal in range(len(expected_args)):
            arg = calldef.arguments[ordinal]
            expected_arg = expected_args[ordinal]
            self.failUnless(
                arg == expected_arg,
                ("the function's '%s' expected %d's argument is '%s' and in " +
                    "reality it is different('%s')") %
                (calldef.name,
                 ordinal, pprint.pformat(expected_arg.__dict__),
                 pprint.pformat(arg.__dict__)))

    def _test_calldef_exceptions(self, calldef, exceptions):
        # exceptions is list of classes names
        exception_decls = []
        for name in exceptions:
            exception_decl = self.global_ns.class_(name)
            self.failUnless(
                exception_decl,
                "unable to find exception class '%s'" %
                name)
            exception_decls.append(exception_decl)
        exception_decls.sort()
        self.failUnless(
            len(calldef.exceptions) == len(exception_decls),
            ("the function's '%s' expected number of exceptions is '%d' and " +
                "in reality it is different('%d')") %
            (calldef.name,
             len(exception_decls),
             len(calldef.exceptions)))
        exceptions_indeed = sorted(calldef.exceptions[:])
        self.failUnless(
            exception_decls == exceptions_indeed,
            ("the function's '%s' expected exceptions are '%s' and in " +
                "reality it is different('%s')") %
            (calldef.name,
             pprint.pformat([delc.name for delc in exception_decls]),
             pprint.pformat([delc.name for delc in exceptions_indeed])))
