# Copyright 2014-2016 Insight Software Consortium.
# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

from . import typedef
from . import cpptypes


def __remove_alias(type_):
    """implementation details"""
    if isinstance(type_, typedef.typedef_t):
        return __remove_alias(type_.decl_type)
    if isinstance(type_, cpptypes.declarated_t) and \
            isinstance(type_.declaration, typedef.typedef_t):
        return __remove_alias(type_.declaration.decl_type)
    if isinstance(type_, cpptypes.compound_t):
        type_.base = __remove_alias(type_.base)
        return type_
    return type_


def remove_alias(type_):
    """returns type without typedefs"""
    type_ref = None
    if isinstance(type_, cpptypes.type_t):
        type_ref = type_
    elif isinstance(type_, typedef.typedef_t):
        type_ref = type_.decl_type
    else:
        pass  # not a valid input, just return it
    if not type_ref:
        return type_
    if type_ref.cache.remove_alias:
        return type_ref.cache.remove_alias
    no_alias = __remove_alias(type_ref.clone())
    type_ref.cache.remove_alias = no_alias
    return no_alias
