# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt


from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


def test_source_reader_enums():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    reader = parser.source_reader_t(config)
    decls = reader.read_file("unnamed_enums_bug1.hpp")
    global_ns = declarations.get_global_namespace(decls)
    global_ns.init_optimizer()
    names = []
    enums = global_ns.enumerations()
    for enum in enums:
        names.extend(list(enum.get_name2value_dict().keys()))
    assert len(names) == 4
    assert 'x1' in names
    assert 'x2' in names
    assert 'y1' in names
    assert 'y2' in names


def test_project_reader_enums():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(["unnamed_enums_bug1.hpp"], config)
    global_ns = declarations.get_global_namespace(decls)
    global_ns.init_optimizer()

    names = []
    for enum in global_ns.enumerations():
        names.extend(list(enum.get_name2value_dict().keys()))
    assert len(names) == 4
    assert 'x1' in names
    assert 'x2' in names
    assert 'y1' in names
    assert 'y2' in names


def test_multiple_files_enums():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse(
        [
            'unnamed_enums_bug1.hpp',
            'unnamed_enums_bug2.hpp',
            'unnamed_enums_bug1.hpp'
        ], config
    )
    global_ns = declarations.get_global_namespace(decls)
    global_ns.init_optimizer()
    names = []
    enums = global_ns.enumerations()
    list(map(
        lambda enum: names.extend(list(enum.get_name2value_dict().keys())),
        enums))
    assert len(names) == 6
    assert 'x1' in names
    assert 'x2' in names
    assert 'y1' in names
    assert 'y2' in names
    assert 'z1' in names
    assert 'z2' in names
