# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

import platform

from . import autoconfig

from pygccxml import parser


def test_cpp_standards():
    """
    Test different compilation standards by setting cflags.

    """

    config = autoconfig.cxx_parsers_cfg.config.clone()

    parser.parse(["cpp_standards.hpp"], config)

    if platform.system() != 'Windows':
        config.cflags = "-std=c++98"
        parser.parse(["cpp_standards.hpp"], config)

        config.cflags = "-std=c++03"
        parser.parse(["cpp_standards.hpp"], config)

    config.cflags = "-std=c++11"

    parser.parse(["cpp_standards.hpp"], config)

    config.cflags = "-std=c++14"
    parser.parse(["cpp_standards.hpp"], config)

    config.cflags = "-std=c++1z"
    parser.parse(["cpp_standards.hpp"], config)

    # Pass down a flag that does not exist.
    # This should raise an exception.
    config.cflags = "-std=c++00"
    with pytest.raises(RuntimeError):
        parser.parse(["cpp_standards.hpp"], config)
