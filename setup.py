#!/usr/bin/env python
# Copyright 2004 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import sys, os, os.path
from distutils import sysconfig
from distutils.core import setup
from distutils.cmd import Command

def generate_doc():
    """Generate the epydoc reference manual.
    """
    print "Generating epydoc files..."
    options = [ '--output="%s"'%os.path.join('docs', 'apidocs'),
                '--docformat=epytext',
                '--url=http://www.language-binding.net',
                '--name=pygccxml',
#                '--verbose',
                'pygccxml']
    cmd_line = "epydoc " + ' '.join( options )
    print cmd_line
    os.system(cmd_line)
    

class doc_cmd(Command):
    """This is a new distutils command 'doc' to build the epydoc manual.
    """

    description = 'build the API reference using epydoc'
    user_options = [('no-doc', None, "don't run epydoc")]
    boolean_options = ['no-doc']

    def initialize_options (self):
        self.no_doc = 0
        
    def finalize_options (self):
        pass
    
    def run(self):
        if self.no_doc:
            return
        generate_doc()


# Generate the doc when a source distribution is created
if sys.argv[-1]=="sdist":
    generate_doc()


setup( name = "pygccxml",
       version = "0.7.2",
       description = "GCC-XML generated file reader",
       author = "Roman Yakovenko",
       author_email = "roman.yakovenko@gmail.com",
       url = 'http://www.language-binding.net/pygccxml/pygccxml.html',
       packages = [ 'pygccxml',
                    'pygccxml.declarations',
                    'pygccxml.parser',
                    'pygccxml.utils' ],
       cmdclass = {"doc" : doc_cmd}
)
