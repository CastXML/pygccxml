# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

TEST_FILE = "core_types.hpp"


def test_read_xml_file():
    config = autoconfig.cxx_parsers_cfg.config.clone()

    src_reader = parser.source_reader_t(config)
    src_decls = src_reader.read_file(TEST_FILE)

    xmlfile = src_reader.create_xml_file(TEST_FILE)

    conf_t = parser.file_configuration_t
    fconfig = conf_t(
        data=xmlfile,
        start_with_declarations=None,
        content_type=conf_t.CONTENT_TYPE.GCCXML_GENERATED_FILE)

    prj_reader = parser.project_reader_t(config)
    prj_decls = prj_reader.read_files(
        [fconfig],
        compilation_mode=parser.COMPILATION_MODE.FILE_BY_FILE)

    declarations.dump_declarations(
        src_decls,
        os.path.join(
            autoconfig.build_directory,
            'xmlfile_reader.src.txt'))
    declarations.dump_declarations(
        prj_decls,
        os.path.join(
            autoconfig.build_directory,
            'xmlfile_reader.prj.txt'))

    assert src_decls == prj_decls
