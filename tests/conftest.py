# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest


class Helpers:
    @staticmethod
    def _test_type_composition(type_, expected_compound, expected_base):
        assert isinstance(type_, expected_compound)
        assert isinstance(type_.base, expected_base)

    @staticmethod
    def _test_calldef_args(calldef, expected_args):
        assert len(calldef.arguments) == len(expected_args)

        for i, expected_arg in enumerate(expected_args):
            arg = calldef.arguments[i]
            assert arg == expected_arg

    @staticmethod
    def _test_calldef_return_type(calldef, expected_type):
        assert isinstance(calldef.return_type, expected_type)

    @staticmethod
    def _test_calldef_exceptions(global_ns, calldef, exceptions):
        # exceptions is list of classes names
        exception_decls = []
        for name in exceptions:
            exception_decl = global_ns.class_(name)
            assert exception_decl is not None
            exception_decls.append(exception_decl)
        exception_decls.sort()
        assert len(calldef.exceptions) == len(exception_decls)
        exceptions_indeed = sorted(calldef.exceptions[:])
        assert exception_decls == exceptions_indeed


@pytest.fixture
def helpers():
    return Helpers
