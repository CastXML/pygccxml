# Copyright 2014-2016 Insight Software Consortium.
# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt


class byte_info(object):

    def __init__(self):
        self._byte_size = 0
        self._byte_align = 0

    @property
    def byte_size(self):
        """Size of this class in bytes @type: int"""
        return self._byte_size

    @byte_size.setter
    def byte_size(self, new_byte_size):
        self._byte_size = new_byte_size

    @property
    def byte_align(self):
        """Alignment of this class in bytes @type: int"""
        return self._byte_align

    @byte_align.setter
    def byte_align(self, new_byte_align):
        self._byte_align = new_byte_align
