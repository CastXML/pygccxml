# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import bz2

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


def test_copy_constructor2():
    # Extract the xml file from the bz2 archive
    bz2_path = os.path.join(
        autoconfig.data_directory,
        'ogre.1.7.xml.bz2')
    xml_path = os.path.join(
        autoconfig.data_directory,
        'ogre.1.7.xml')
    with open(xml_path, 'wb') as new_file:
        # bz2.BZ2File can not be used in a with statement in python 2.6
        bz2_file = bz2.BZ2File(bz2_path, 'rb')
        for data in iter(lambda: bz2_file.read(100 * 1024), b''):
            new_file.write(data)
        bz2_file.close()

    reader = parser.source_reader_t(autoconfig.cxx_parsers_cfg.config)
    global_ns = declarations.get_global_namespace(
        reader.read_xml_file(xml_path)
        )
    global_ns.init_optimizer()

    for x in global_ns.typedefs('SettingsMultiMap'):
        assert declarations.is_noncopyable(x) is False

    for x in global_ns.typedefs('SettingsIterator'):
        assert declarations.is_noncopyable(x) is False

    for x in global_ns.typedefs('SectionIterator'):
        assert declarations.is_noncopyable(x) is False

    os.remove(xml_path)
