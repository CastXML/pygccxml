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


@pytest.fixture
def helpers():
    return Helpers
