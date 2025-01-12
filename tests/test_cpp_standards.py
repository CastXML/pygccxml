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

    cflags_common = ""

    if platform.system() == "Darwin":
        cflags_common = " -Dat_quick_exit=atexit -Dquick_exit=exit"
        # https://fr.mathworks.com/matlabcentral/answers/2013982-clibgen-generatelibrarydefinition-error-the-global-scope-has-no-quick_exit-on-mac-m2#answer_1439856
        # https://github.com/jetbrains/kotlin/commit/d50f585911dedec5723213da8835707ac95e1c01

    parser.parse(["cpp_standards.hpp"], config)

    if platform.system() != 'Windows':
        config.cflags = "-std=c++98" + cflags_common
        parser.parse(["cpp_standards.hpp"], config)

        config.cflags = "-std=c++03" + cflags_common
        parser.parse(["cpp_standards.hpp"], config)

    config.cflags = "-std=c++11" + cflags_common

    parser.parse(["cpp_standards.hpp"], config)

    config.cflags = "-std=c++14" + cflags_common
    parser.parse(["cpp_standards.hpp"], config)

    config.cflags = "-std=c++1z" + cflags_common
    parser.parse(["cpp_standards.hpp"], config)

    # Pass down a flag that does not exist.
    # This should raise an exception.
    config.cflags = "-std=c++00" + cflags_common
    with pytest.raises(RuntimeError):
        parser.parse(["cpp_standards.hpp"], config)
