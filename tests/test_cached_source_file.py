# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import stat

from . import autoconfig

from pygccxml import utils
from pygccxml import parser

TEST_FILES = [
    "core_types.hpp",
]


def test_cached_source_file():

    config = autoconfig.cxx_parsers_cfg.config.clone()

    fconfig = parser.file_configuration_t(
        data=TEST_FILES[0],
        content_type=parser.CONTENT_TYPE.CACHED_SOURCE_FILE)
    try:
        prj_reader = parser.project_reader_t(config)
        prj_reader.read_files(
            [fconfig],
            compilation_mode=parser.COMPILATION_MODE.FILE_BY_FILE)
        assert os.path.exists(fconfig.cached_source_file)
        mtime1 = os.stat(fconfig.cached_source_file)[stat.ST_MTIME]
        prj_reader.read_files(
            [fconfig],
            compilation_mode=parser.COMPILATION_MODE.FILE_BY_FILE)
        mtime2 = os.stat(fconfig.cached_source_file)[stat.ST_MTIME]
        assert mtime1 == mtime2
    finally:
        utils.remove_file_no_raise(fconfig.cached_source_file, config)
