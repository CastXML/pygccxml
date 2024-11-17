# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


TEST_FILES = [
    "declarations_enums.hpp",
]


def test_cache():
    cache_file = os.path.join(autoconfig.data_directory, 'pygccxml.cache')
    if os.path.exists(cache_file) and os.path.isfile(cache_file):
        os.remove(cache_file)

    config = autoconfig.cxx_parsers_cfg.config.clone()

    cache = parser.file_cache_t(cache_file)
    reader = parser.source_reader_t(config, cache)
    decls1 = reader.read_file(TEST_FILES[0])
    cache.flush()
    cache = parser.file_cache_t(cache_file)
    reader = parser.source_reader_t(config, cache)
    decls2 = reader.read_file(TEST_FILES[0])

    enum_matcher = declarations.declaration_matcher_t(
        name="EColor",
        decl_type=declarations.enumeration_t
    )

    color1 = declarations.matcher.get_single(enum_matcher, decls1)
    color2 = declarations.matcher.get_single(enum_matcher, decls2)
    assert color1.values == color2.values
