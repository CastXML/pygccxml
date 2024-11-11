# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import inspect

from pygccxml import declarations


def test_types_hashes():
    """
    Test if all the type_t instances implement a hash method.

    The hash is part of the public API, as there are multiple tools
    that rely on it to compare type_t instances.

    The best way to test this is to instanciate dummy type_t objects
    for each class that subclasses type_t, and check that the hash of
    these objects is not None.

    """

    members = inspect.getmembers(declarations, inspect.isclass)
    for member in members:
        member_type = member[1]
        is_type_t_subclass = issubclass(member_type, declarations.type_t)
        is_not_type_t = member_type != declarations.type_t
        if is_type_t_subclass and is_not_type_t:
            type_mockup = _create_type_t_mockup(member_type)
            assert hash(type_mockup) is not None


def test_declarations_hashes():
    """
    Test if all the declaration_t instances implement a hash method.

    The hash is part of the public API, as there are multiple tools
    that rely on it to compare declaration_t instances.

    The best way to test this is to instanciate dummy declaration_t objects
    for each class that subclasses declaration_t, and check that the hash
    of these objects is not None.

    """
    members = inspect.getmembers(declarations, inspect.isclass)
    for member in members:
        member_type = member[1]
        if issubclass(member_type, declarations.declaration_t):
            assert hash(member_type()) is not None


def test_type_qualifiers_t_hash():
    """
    Test if the type_qualifiers_t instance implements a hash method.

    The hash is part of the public API, as there are multiple tools
    that rely on it to compare type_qualifiers_t instances.

    """
    assert hash(declarations.type_qualifiers_t()) is not None


def _create_type_t_mockup(member_type):
    nbr_parameters = len(inspect.signature(member_type).parameters)
    if nbr_parameters == 0:
        m = member_type()
    else:
        if member_type == declarations.array_t:
            m = member_type(_base_mockup(), size=1)
        else:
            m = member_type(_base_mockup())
    m.cache.decl_string = ""
    return m


class _base_mockup(declarations.type_t):

    def __init__(self):
        declarations.type_t.__init__(self)
        self.cache.decl_string = ""
        self._decl_string = ""
        self.variable_type = declarations.type_t()

    def build_decl_string(self, with_defaults=False):
        return self._decl_string
