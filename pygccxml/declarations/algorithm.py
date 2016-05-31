# Copyright 2014-2016 Insight Software Consortium.
# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

"""
Define few unrelated algorithms that work on declarations.

"""

import warnings
from . import declaration_utils


def make_flatten(decl_or_decls):
    """
    Converts tree representation of declarations to flatten one.

    :param decl_or_decls: reference to list of declaration's or single
        declaration
    :type decl_or_decls: :class:`declaration_t` or [ :class:`declaration_t` ]
    :rtype: [ all internal declarations ]

    """

    import pygccxml.declarations  # prevent cyclic import

    def proceed_single(decl):
        answer = [decl]
        if not isinstance(decl, pygccxml.declarations.scopedef_t):
            return answer
        for elem in decl.declarations:
            if isinstance(elem, pygccxml.declarations.scopedef_t):
                answer.extend(proceed_single(elem))
            else:
                answer.append(elem)
        return answer

    decls = []
    if isinstance(decl_or_decls, list):
        decls.extend(decl_or_decls)
    else:
        decls.append(decl_or_decls)
    answer = []
    for decl in decls:
        answer.extend(proceed_single(decl))
    return answer


def get_global_namespace(decls):
    import pygccxml.declarations
    found = [
        decl for decl in make_flatten(decls) if decl.name == '::' and
        isinstance(decl, pygccxml.declarations.namespace_t)]
    if len(found) == 1:
        return found[0]
    raise RuntimeError("Unable to find global namespace.")


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
            self, type=None, decl_type=None,
            name=None, fullname=None, parent=None):

        if type is not None:
            # Deprecated since 1.8.0. Will be removed in 1.9.0
            warnings.warn(
                "The type argument is deprecated. \n" +
                "Please use the decl_type argument instead.",
                DeprecationWarning)
            if decl_type is not None:
                raise (
                    "Please use only either the type or " +
                    "decl_type argument.")
            # Still allow to use the old type for the moment.
            decl_type = type

        self._decl_type = decl_type
        self.name = name
        self.fullname = fullname
        self.parent = parent

    def does_match_exist(self, inst):
        """
        Returns True if inst does match one of specified criteria.

        :param inst: declaration instance
        :type inst: :class:`declaration_t`

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


def find_all_declarations(
        declarations,
        type=None,
        decl_type=None,
        name=None,
        parent=None,
        recursive=True,
        fullname=None):
    """
    Returns a list of all declarations that match criteria, defined by
    developer.

    For more information about arguments see :class:`match_declaration_t`
    class.

    :rtype: [ matched declarations ]

    """
    if type is not None:
        # Deprecated since 1.8.0. Will be removed in 1.9.0
        warnings.warn(
            "The type argument is deprecated. \n" +
            "Please use the decl_type argument instead.",
            DeprecationWarning)
        if decl_type is not None:
            raise (
                "Please use only either the type or " +
                "decl_type argument.")
        # Still allow to use the old type for the moment.
        decl_type = type

    if recursive:
        decls = make_flatten(declarations)
    else:
        decls = declarations

    return list(
        filter(
            match_declaration_t(
                decl_type=decl_type,
                name=name,
                fullname=fullname,
                parent=parent),
            decls))


def find_declaration(
        declarations,
        type=None,
        decl_type=None,
        name=None,
        parent=None,
        recursive=True,
        fullname=None):
    """
    Returns single declaration that match criteria, defined by developer.
    If more the one declaration was found None will be returned.

    For more information about arguments see :class:`match_declaration_t`
    class.

    :rtype: matched declaration :class:`declaration_t` or None

    """
    if type is not None:
        # Deprecated since 1.8.0. Will be removed in 1.9.0
        warnings.warn(
            "The type argument is deprecated. \n" +
            "Please use the decl_type argument instead.",
            DeprecationWarning)
        if decl_type is not None:
            raise (
                "Please use only either the type or " +
                "decl_type argument.")
        # Still allow to use the old type for the moment.
        decl_type = type

    decl = find_all_declarations(
        declarations,
        decl_type=decl_type,
        name=name,
        parent=parent,
        recursive=recursive,
        fullname=fullname)
    if len(decl) == 1:
        return decl[0]


def find_first_declaration(
        declarations,
        type=None,
        decl_type=None,
        name=None,
        parent=None,
        recursive=True,
        fullname=None):
    """
    Returns first declaration that match criteria, defined by developer.

    For more information about arguments see :class:`match_declaration_t`
    class.

    :rtype: matched declaration :class:`declaration_t` or None

    """
    if type is not None:
        # Deprecated since 1.8.0. Will be removed in 1.9.0
        warnings.warn(
            "The type argument is deprecated. \n" +
            "Please use the decl_type argument instead.",
            DeprecationWarning)
        if decl_type is not None:
            raise (
                "Please use only either the type or " +
                "decl_type argument.")
        # Still allow to use the old type for the moment.
        decl_type = type

    matcher = match_declaration_t(
        decl_type=decl_type,
        name=name,
        fullname=fullname,
        parent=parent)
    if recursive:
        decls = make_flatten(declarations)
    else:
        decls = declarations
    for decl in decls:
        if matcher(decl):
            return decl
    return None


def declaration_files(decl_or_decls):
    """
    Returns set of files

    Every declaration is declared in some file. This function returns set, that
    contains all file names of declarations.

    :param decl_or_decls: reference to list of declaration's or single
        declaration
    :type decl_or_decls: :class:`declaration_t` or [:class:`declaration_t`]
    :rtype: set(declaration file names)

    """

    files = set()
    decls = make_flatten(decl_or_decls)
    for decl in decls:
        if decl.location:
            files.add(decl.location.file_name)
    return files


class visit_function_has_not_been_found_t(RuntimeError):
    """
    Exception that is raised, from :func:`apply_visitor`, when a visitor could
    not be applied.

    """

    def __init__(self, visitor, decl_inst):
        RuntimeError.__init__(self)
        self.__msg = (
            "Unable to find visit function. Visitor class: %s. " +
            "Declaration instance class: %s'") \
            % (visitor.__class__.__name__, decl_inst.__class__.__name__)

    def __str__(self):
        return self.__msg


def apply_visitor(visitor, decl_inst):
    """
    Applies a visitor on declaration instance.

    :param visitor: instance
    :type visitor: :class:`type_visitor_t` or :class:`decl_visitor_t`

    """

    fname = 'visit_' + \
        decl_inst.__class__.__name__[:-2]  # removing '_t' from class name
    if not hasattr(visitor, fname):
        raise visit_function_has_not_been_found_t(visitor, decl_inst)
    return getattr(visitor, fname)()
