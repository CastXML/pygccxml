# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


def test_text_reader():
    config = autoconfig.cxx_parsers_cfg.config.clone()

    fconfig = parser.file_configuration_t(
        data='int i;',
        start_with_declarations=None,
        content_type=parser.file_configuration_t.CONTENT_TYPE.TEXT)

    prj_reader = parser.project_reader_t(config)
    decls = prj_reader.read_files(
        [fconfig],
        compilation_mode=parser.COMPILATION_MODE.FILE_BY_FILE)

    var_i = declarations.find_declaration(
        decls, decl_type=declarations.variable_t, name='i')
    assert var_i is not None
