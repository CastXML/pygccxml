# Copyright 2014-2016 Insight Software Consortium.
# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

from . import scanner

# keep py2exe happy
import xml.etree.ElementTree

import xml.etree.cElementTree as ElementTree


class ietree_scanner_t(scanner.scanner_t):

    def __init__(self, xml_file, decl_factory, *args):
        scanner.scanner_t.__init__(self, xml_file, decl_factory, *args)

    def read(self):
        context = ElementTree.iterparse(
            self.xml_file,
            events=("start", "end"))
        for event, elem in context:
            if event == 'start':
                self.startElement(elem.tag, elem.attrib)
            else:
                self.endElement(elem.tag)
                elem.clear()
        self.endDocument()
