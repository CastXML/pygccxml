# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import scanner
import xml.etree.cElementTree as ElementTree
        
class etree_saxifier_t(object):
    """Produces SAX events for an element and children."""
    def __init__(self, element_or_tree, content_handler):
        try:
            element = element_or_tree.getroot()
        except AttributeError:
            element = element_or_tree
        self._element = element
        self._content_handler = content_handler        
        
    def saxify(self):
        self._content_handler.startDocument()
        self._recursive_saxify(self._element, {})
        self._content_handler.endDocument()

    def _recursive_saxify(self, element, prefixes):
        attrs = {}
        for attr in element.items():
            attrs[ attr[0] ] = attr[1]

        content_handler = self._content_handler
        content_handler.startElement( element.tag, attrs )
        
        if element.text:
            content_handler.characters(element.text)
        for child in element:
            self._recursive_saxify(child, prefixes)
        content_handler.endElement( element.tag )

        if element.tail:
            content_handler.characters(element.tail)

class etree_scanner_t( scanner.scanner_t ):
    def __init__(self, gccxml_file, decl_factory, *args ):
        scanner.scanner_t.__init__( self, gccxml_file, decl_factory, *args )
    
    def read( self ):
        tree = ElementTree.parse( self.gccxml_file )
        saxifier = etree_saxifier_t( tree, self )
        saxifier.saxify()
    
