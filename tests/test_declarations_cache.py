# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import os.path

from . import autoconfig

from pygccxml.parser.config import xml_generator_configuration_t
from pygccxml.parser import declarations_cache


def test_file_signature():
    file1 = os.path.join(autoconfig.data_directory, 'decl_cache_file1.txt')
    file1_dup = os.path.join(
        autoconfig.data_directory,
        'decl_cache_file1_duplicate.txt')
    file2 = os.path.join(autoconfig.data_directory, 'decl_cache_file2.txt')
    sig1 = declarations_cache.file_signature(file1)
    sig1_dup = declarations_cache.file_signature(file1_dup)
    sig2 = declarations_cache.file_signature(file2)
    assert sig1 == sig1_dup
    assert sig1 != sig2


def test_config_signature():
    diff_cfg_list = build_differing_cfg_list()
    def_cfg = diff_cfg_list[0]
    def_sig = declarations_cache.configuration_signature(def_cfg)

    # Test changes that should cause sig changes
    for cfg in diff_cfg_list[1:]:
        assert declarations_cache.configuration_signature(cfg) != def_sig

    # Test changes that should not cause sig changes
    no_changes = def_cfg.clone()
    assert declarations_cache.configuration_signature(no_changes) == def_sig

    ignore_changed = def_cfg.clone()
    ignore_changed.ignore_gccxml_output = True
    assert (
        declarations_cache.configuration_signature(ignore_changed) == def_sig
        )


def test_cache_interface():
    cache_file = os.path.join(
        autoconfig.build_directory,
        'decl_cache_test.test_cache_read.cache')
    file1 = os.path.join(autoconfig.data_directory, 'decl_cache_file1.txt')
    file1_dup = os.path.join(
        autoconfig.data_directory,
        'decl_cache_file1_duplicate.txt')
    file2 = os.path.join(autoconfig.data_directory, 'decl_cache_file2.txt')
    diff_cfg_list = build_differing_cfg_list()
    def_cfg = diff_cfg_list[0]

    if os.path.exists(cache_file):
        os.remove(cache_file)

    cache = declarations_cache.file_cache_t(cache_file)
    assert len(cache._file_cache_t__cache) == 0

    # test creating new entries for differing files
    cache.update(file1, def_cfg, 1, [])
    assert len(cache._file_cache_t__cache) == 1
    cache.update(file1_dup, def_cfg, 2, [])
    assert len(cache._file_cache_t__cache) == 1
    cache.update(file2, def_cfg, 3, [])
    assert len(cache._file_cache_t__cache) == 2

    assert cache.cached_value(file1, def_cfg) == 2
    assert cache.cached_value(file2, def_cfg) == 3

    # Test reading again
    cache.flush()
    cache = declarations_cache.file_cache_t(cache_file)
    assert len(cache._file_cache_t__cache) == 2
    assert cache.cached_value(file1, def_cfg) == 2
    assert cache.cached_value(file2, def_cfg) == 3

    # Test flushing doesn't happen if we don't touch the cache
    cache = declarations_cache.file_cache_t(cache_file)
    assert cache.cached_value(file1, def_cfg) == 2  # Read from cache
    cache.flush()    # should not actually flush
    cache = declarations_cache.file_cache_t(cache_file)
    assert len(cache._file_cache_t__cache) == 2

    # Test flush culling
    cache = declarations_cache.file_cache_t(cache_file)
    cache.update(file1_dup, def_cfg, 4, [])    # Modify cache
    cache.flush()    # should cull off one entry
    cache = declarations_cache.file_cache_t(cache_file)
    assert len(cache._file_cache_t__cache) == 1


def build_differing_cfg_list():
    """ Return a list of configurations that all differ. """
    cfg_list = []
    def_cfg = xml_generator_configuration_t(
        "xml_generator_path",
        '.', ['tmp'], ['sym'], ['unsym'], None, False, "")
    cfg_list.append(def_cfg)

    # Test changes that should cause sig changes
    gccxml_changed = def_cfg.clone()
    gccxml_changed.xml_generator_path = "other_path"
    cfg_list.append(gccxml_changed)

    wd_changed = def_cfg.clone()
    wd_changed.working_directory = "other_dir"
    cfg_list.append(wd_changed)

    # inc_changed = def_cfg.clone()
    # inc_changed.include_paths = ["/var/tmp"]
    # assert configuration_signature(inc_changed) != def_sig)
    inc_changed = xml_generator_configuration_t(
        "xml_generator_path", '.', ['/var/tmp'], ['sym'], ['unsym'],
        None, False, "")
    cfg_list.append(inc_changed)

    # def_changed = def_cfg.clone()
    # def_changed.define_symbols = ["symbol"]
    # assert configuration_signature(def_changed) != def_sig)
    def_changed = xml_generator_configuration_t(
        "xml_generator_path", '.', ['/var/tmp'], ['new-sym'], ['unsym'],
        None, False, "")
    cfg_list.append(def_changed)

    # undef_changed = def_cfg.clone()
    # undef_changed.undefine_symbols = ["symbol"]
    # assert configuration_signature(undef_changed) != def_sig)
    undef_changed = xml_generator_configuration_t(
        "xml_generator_path", '.', ['/var/tmp'], ['sym'], ['new-unsym'],
        None, False, "")
    cfg_list.append(undef_changed)

    cflags_changed = def_cfg.clone()
    cflags_changed.cflags = "new flags"
    cfg_list.append(cflags_changed)

    return cfg_list
