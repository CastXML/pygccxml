# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pprint
import time
import unittest

from . import autoconfig


class parser_test_case_t(unittest.TestCase):

    CXX_PARSER_CFG = None
    xml_generator_from_xml_file = None

    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args)
        self.xml_generator_from_xml_file = None
        if self.CXX_PARSER_CFG:
            self.config = self.CXX_PARSER_CFG.clone()
        elif autoconfig.cxx_parsers_cfg.config:
            self.config = autoconfig.cxx_parsers_cfg.config.clone()
        else:
            pass

    def run(self, result=None):
        """
        Override the run method.

        Allows to measure the time each test needs. The result is written
        in the test_cost.log file.

        """
        with open("test_cost.log", "a") as cost_file:
            start_time = time.time()
            super(parser_test_case_t, self).run(result)
            name = super(parser_test_case_t, self).id()
            cost_file.write(
                name + " " +
                str(time.time() - start_time) + "\n")

    def _test_type_composition(self, type_, expected_compound, expected_base):
        self.assertTrue(
            isinstance(type_, expected_compound),
            "the compound type('%s') should be '%s'" %
            (type_.decl_string, expected_compound.__name__))
        self.assertTrue(
            isinstance(type_.base, expected_base),
            "base type('%s') should be '%s'" %
            (type_.decl_string, expected_base.__name__))

    def _test_calldef_return_type(self, calldef, expected_type):
        self.assertTrue(
            isinstance(calldef.return_type, expected_type),
            ("the function's '%s' expected return type is '%s' and in " +
                "reality it is different('%s')") %
            (calldef.name, expected_type.__name__,
             calldef.return_type.__class__.__name__))

    def _test_calldef_args(self, calldef, expected_args):
        self.assertTrue(
            len(calldef.arguments) == len(expected_args),
            ("the function's '%s' expected number of arguments is '%d' and " +
                "in reality it is different('%d')") %
            (calldef.name, len(expected_args), len(calldef.arguments)))

        for i, expected_arg in enumerate(expected_args):
            arg = calldef.arguments[i]
            self.assertTrue(
                arg == expected_arg,
                ("the function's '%s' expected %d's argument is '%s' and in " +
                    "reality it is different('%s')") %
                (calldef.name, i, pprint.pformat(expected_arg.__dict__),
                 pprint.pformat(arg.__dict__)))

    def _test_calldef_exceptions(self, calldef, exceptions):
        # exceptions is list of classes names
        exception_decls = []
        for name in exceptions:
            exception_decl = self.global_ns.class_(name)
            self.assertTrue(
                exception_decl,
                "unable to find exception class '%s'" %
                name)
            exception_decls.append(exception_decl)
        exception_decls.sort()
        self.assertTrue(
            len(calldef.exceptions) == len(exception_decls),
            ("the function's '%s' expected number of exceptions is '%d' and " +
                "in reality it is different('%d')") %
            (calldef.name,
             len(exception_decls),
             len(calldef.exceptions)))
        exceptions_indeed = sorted(calldef.exceptions[:])
        self.assertTrue(
            exception_decls == exceptions_indeed,
            ("the function's '%s' expected exceptions are '%s' and in " +
                "reality it is different('%s')") %
            (calldef.name,
             pprint.pformat([delc.name for delc in exception_decls]),
             pprint.pformat([delc.name for delc in exceptions_indeed])))
