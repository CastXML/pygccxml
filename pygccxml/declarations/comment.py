# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

"""
Describe a C++ comment declaration.

"""


from . import declaration


class comment_t(declaration.declaration_t):

    def __init__(self, name='', declarations=None):
        """
        Creates an object that describes a C++ comment declaration.

        Args:

        """
        declaration.declaration_t.__init__(self, name)
        self.location = {}
        self._start_line = 0
        self._end_line = 0
        self._text = ""

    @property
    def start_line(self):
        return self._start_line

    @start_line.setter
    def start_line(self, start_line):
        self._start_line = int(start_line)

    @property
    def end_line(self):
        return self._end_line

    @end_line.setter
    def end_line(self, end_line):
        self._end_line = int(end_line)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
