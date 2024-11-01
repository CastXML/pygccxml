# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import shutil

import pytest

from . import autoconfig

from pygccxml import parser

TEST_FILES = [
    "typedefs1.hpp"
]

CACHE_DIR = os.path.join(autoconfig.data_directory, "directory_cache_test")


def set_up():
    if os.path.isdir(CACHE_DIR):
        shutil.rmtree(CACHE_DIR)
    if os.path.isfile(CACHE_DIR):
        os.remove(CACHE_DIR)


def test_directory_cache_without_compression():
    """
    Test the directory cache without compression

    """
    config = autoconfig.cxx_parsers_cfg.config.clone()
    set_up()
    # Test with compression OFF
    cache = parser.directory_cache_t(directory=CACHE_DIR)
    # Generate a cache on first read
    parser.parse(TEST_FILES, config, cache=cache)
    # Read from the cache the second time
    parser.parse(TEST_FILES, config, cache=cache)


def test_directory_cache_with_compression():
    """
    Test the directory cache wit compression

    """
    config = autoconfig.cxx_parsers_cfg.config.clone()
    set_up()
    # Test with compression ON
    cache = parser.directory_cache_t(
        directory=CACHE_DIR, compression=True)
    # Generate a cache on first read
    parser.parse(TEST_FILES, config, cache=cache)
    # Read from the cache the second time
    parser.parse(TEST_FILES, config, cache=cache)


def test_directory_cache_twice():
    """
    Setup two caches in a row.

    The second run will reload the same cache directory.
    """
    config = autoconfig.cxx_parsers_cfg.config.clone()
    set_up()
    cache = parser.directory_cache_t(directory=CACHE_DIR)
    parser.parse(TEST_FILES, config, cache=cache)
    cache = parser.directory_cache_t(directory=CACHE_DIR)
    parser.parse(TEST_FILES, config, cache=cache)


def test_directory_existing_dir():
    """
    Setup a cache when there is already a file at the cache's location.
    """
    set_up()
    open(CACHE_DIR, "a").close()
    with pytest.raises(ValueError):
        parser.directory_cache_t(directory=CACHE_DIR)
