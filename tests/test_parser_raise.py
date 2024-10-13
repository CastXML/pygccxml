# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import pytest

from . import autoconfig

from pygccxml import parser


def test_raise():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    content = "abra cadabra " + os.linesep
    with pytest.raises(RuntimeError) as _:
        parser.parse_string(content, config)
