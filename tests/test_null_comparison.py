# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

TEST_FILES = [
    "null_comparison.hpp",
]


def test_argument_null_comparison():
    """
    Test for None comparisons with default arguments
    """

    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(TEST_FILES, config)
    global_ns = declarations.get_global_namespace(decls)

    ns = global_ns.namespace("ns")

    func = ns.free_function(name="TestFunction1")
    assert (func.arguments[0] > func.arguments[1]) is False

    func = ns.free_function(name="TestFunction2")
    assert (func.arguments[0] > func.arguments[1]) is False
