# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os

from . import autoconfig

from pygccxml import parser

TEST_FILE = os.path.join(autoconfig.data_directory, 'core_cache.hpp')
cache_file = os.path.join(
            autoconfig.data_directory,
            'pygccxml.cache')


def reset_cache():
    if os.path.exists(cache_file) and os.path.isfile(cache_file):
        os.remove(cache_file)


def touch():
    # Need to change file.
    with open(TEST_FILE, "a+") as header:
        header.write("//touch")


def test_update_cache():
    reset_cache()
    config = autoconfig.cxx_parsers_cfg.config.clone()

    # Save the content of the header file for later
    with open(TEST_FILE, "r") as old_header:
        content = old_header.read()

    declarations = parser.parse([TEST_FILE], config)
    cache = parser.file_cache_t(cache_file)
    cache.update(
        source_file=TEST_FILE,
        configuration=config,
        declarations=declarations,
        included_files=[])
    assert declarations == cache.cached_value(
            TEST_FILE,
            config)
    touch()
    assert cache.cached_value(TEST_FILE, config) is None

    # We wrote a //touch in the header file. Just replace the file with the
    # original content. The touched file would be sometimes commited by
    # error as it was modified.
    with open(TEST_FILE, "w") as new_header:
        new_header.write(content)


def test_cache_from_file():
    reset_cache()
    config = autoconfig.cxx_parsers_cfg.config.clone()
    declarations = parser.parse([TEST_FILE], config)
    cache = parser.file_cache_t(cache_file)
    cache.update(
        source_file=TEST_FILE,
        configuration=config,
        declarations=declarations,
        included_files=[])
    assert declarations == cache.cached_value(
            TEST_FILE,
            config)
    cache.flush()
    cache = parser.file_cache_t(cache_file)
    assert declarations == cache.cached_value(
            TEST_FILE,
            config)
