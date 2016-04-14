# Copyright 2014-2016 Insight Software Consortium.
# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

"""
defines class that describes C++ typedef declaration
"""

import warnings
from . import declaration
from . import dependencies


class typedef_t(declaration.declaration_t):

    """describes C++ typedef declaration"""

    def __init__(self, name='', type=None):
        """creates class that describes C++ typedef"""
        declaration.declaration_t.__init__(self, name)
        self._type = type

    def _get__cmp__items(self):
        """implementation details"""
        return [self.decl_type]

    def __eq__(self, other):
        if not declaration.declaration_t.__eq__(self, other):
            return False
        return self.decl_type == other.decl_type

    def __hash__(self):
        return super.__hash__(self)

    @property
    def type(self):
        """reference to the original :class:`type <type_t>`"""
        warnings.warn(
            "typedef_t.type is deprecated.\n" +
            "Please use typedef_t.decl_type instead.", DeprecationWarning)
        return self._type

    @type.setter
    def type(self, _type):
        warnings.warn(
            "typedef_t.type is deprecated.\n" +
            "Please use typedef_t.decl_type instead.", DeprecationWarning)
        self._type = _type

    @property
    def decl_type(self):
        """reference to the original :class:`decl_type <type_t>`"""
        return self._type

    @decl_type.setter
    def decl_type(self, decl_type):
        self._type = decl_type

    def i_depend_on_them(self, recursive=True):
        return [dependencies.dependency_info_t(self, self.decl_type)]

    @property
    def byte_size(self):
        "Size of this type in bytes @type: int"
        return self._type.byte_size

    @property
    def byte_align(self):
        "alignment of this type in bytes @type: int"
        return self._type.byte_align
