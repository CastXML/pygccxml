# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

"""
Define few unrelated algorithms that work on declarations.

"""

import re

from . import declaration_utils
from . import runtime_errors


class match_declaration_t(object):
    """
    Helper class for different search algorithms.

    This class will help developer to match declaration by:
        - declaration type, for example :class:`class_t` or
            :class:`operator_t`.
        - declaration name
        - declaration full name
        - reference to parent declaration

    """

    def __init__(
            self, decl_type=None,
            name=None, fullname=None, parent=None):

        self._decl_type = decl_type
        self.name = name
        self.fullname = fullname
        self.parent = parent

    def does_match_exist(self, inst):
        """
        Returns True if inst does match one of specified criteria.

        :param inst: declaration instance
        :type inst: :class:`DeclarationD`

        :rtype: bool

        """

        answer = True
        if self._decl_type is not None:
            answer &= isinstance(inst, self._decl_type)
        if self.name is not None:
            answer &= inst.name == self.name
        if self.parent is not None:
            answer &= self.parent is inst.parent
        if self.fullname is not None:
            if inst.name:
                answer &= self.fullname == declaration_utils.full_name(inst)
            else:
                answer = False
        return answer

    def __call__(self, inst):
        """
        .. code-block:: python

           return self.does_match_exist(inst)

        """

        return self.does_match_exist(inst)


def apply_visitor(visitor, decl_inst):
    """
    Applies a visitor on declaration instance.

    :param visitor: instance
    :type visitor: :class:`type_visitor_t` or :class:`decl_visitor_t`

    """

    fname = decl_inst.__class__.__name__
    fname = re.sub("_t$", "", fname)  # removing '_t' from class name
    fname = re.sub("T$", "", fname)  # removing 'T' from class name
    fname = re.sub("D$", "", fname)  # removing 'D' from class name

    # TODO: Refactor this once the class name refactoring is done
    new_name = ""
    i = 0
    if fname[0].isupper():
        # New class syntaxt
        for char in fname:
            # For example:
            # ClassDeclarationD -> class_declaration
            # NamespaceD -> namespace
            # WCharT -> wchar
            if char.isupper() and i > 0 and fname[i-1].islower():
                new_name += "_"
            new_name += char.lower()
            i += 1
    else:
        # Legacy class syntax
        new_name = fname

    new_name = 'visit_' + new_name
    if not hasattr(visitor, new_name):
        raise runtime_errors.visit_function_has_not_been_found_t(
            visitor, decl_inst)
    return getattr(visitor, new_name)()
