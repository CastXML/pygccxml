# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest
import warnings

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

TEST_FILES = [
    "include_all.hpp",
]


@pytest.fixture
def global_ns():
    COMPILATION_MODE = parser.COMPILATION_MODE.ALL_AT_ONCE
    INIT_OPTIMIZER = True
    config = autoconfig.cxx_parsers_cfg.config.clone()
    config.castxml_epic_version = 1
    decls = parser.parse(TEST_FILES, config, COMPILATION_MODE)
    global_ns = declarations.get_global_namespace(decls)
    if INIT_OPTIMIZER:
        global_ns.init_optimizer()
    return global_ns


def test_variable(global_ns):
    ns_vars = global_ns.namespace('::declarations::variables')
    static_var = ns_vars.variable('static_var')

    # Legacy way of fetching dependencies. Is still valid but deprecated
    warnings.simplefilter("ignore", Warning)
    dependencies_old = static_var.i_depend_on_them()
    warnings.simplefilter("error", Warning)
    assert len(dependencies_old) == 1
    assert dependencies_old[0].declaration is static_var
    assert dependencies_old[0].depend_on_it.decl_string == 'int'

    dependencies_new = declarations.get_dependencies_from_decl(static_var)
    assert len(dependencies_new) == 1
    assert dependencies_new[0].declaration is static_var
    assert dependencies_new[0].depend_on_it.decl_string == 'int'

    m_mutable = ns_vars.variable('m_mutable')

    # Legacy way of fetching dependencies. Is still valid but deprecated
    warnings.simplefilter("ignore", Warning)
    dependencies_old = m_mutable.i_depend_on_them()
    warnings.simplefilter("error", Warning)
    assert len(dependencies_old) == 1
    assert dependencies_old[0].declaration is m_mutable
    assert dependencies_old[0].depend_on_it.decl_string == 'int'

    dependencies_new = declarations.get_dependencies_from_decl(m_mutable)
    assert len(dependencies_new) == 1
    assert dependencies_new[0].declaration is m_mutable
    assert dependencies_new[0].depend_on_it.decl_string == 'int'


def test_class(global_ns):
    ns_vars = global_ns.namespace('::declarations::variables')

    cls = ns_vars.class_('struct_variables_t')

    # Legacy way of fetching dependencies. Is still valid but deprecated
    warnings.simplefilter("ignore", Warning)
    dependencies_old = cls.i_depend_on_them()
    warnings.simplefilter("error", Warning)
    dependencies_old = [
        d for d in dependencies_old if not d.declaration.is_artificial]
    assert len(dependencies_old) == 1

    dependencies_new = declarations.get_dependencies_from_decl(cls)
    dependencies_new = [
        d for d in dependencies_new if not d.declaration.is_artificial]
    assert len(dependencies_new) == 1

    m_mutable = ns_vars.variable('m_mutable')

    # Legacy way of fetching dependencies. Is still valid but deprecated
    dependencies_old = [
        dependency for dependency in dependencies_old if
        dependency.declaration is m_mutable]
    assert len(dependencies_old) == 1
    assert dependencies_old[0].depend_on_it.decl_string == 'int'
    assert dependencies_old[0].access_type == 'public'

    dependencies_new = [
        dependency for dependency in dependencies_new if
        dependency.declaration is m_mutable]
    assert len(dependencies_new) == 1
    assert dependencies_new[0].depend_on_it.decl_string == 'int'
    assert dependencies_new[0].access_type == 'public'

    ns_dh = global_ns.namespace('::core::diamand_hierarchy')
    fd_cls = ns_dh.class_('final_derived_t')
    derived1_cls = ns_dh.class_('derived1_t')

    # Legacy way of fetching dependencies. Is still valid but deprecated
    warnings.simplefilter("ignore", Warning)
    dependencies_old = declarations.get_dependencies_from_decl(fd_cls)
    warnings.simplefilter("error", Warning)
    dependencies_old = [
        dependency for dependency in dependencies_old if
        dependency.depend_on_it is derived1_cls]
    assert len(dependencies_old) == 1
    assert dependencies_old[0].depend_on_it is derived1_cls
    assert dependencies_old[0].access_type == 'public'

    dependencies_new = declarations.get_dependencies_from_decl(fd_cls)
    dependencies_new = [
        dependency for dependency in dependencies_new if
        dependency.depend_on_it is derived1_cls]
    assert len(dependencies_new) == 1
    assert dependencies_new[0].depend_on_it is derived1_cls
    assert dependencies_new[0].access_type == 'public'


def test_calldefs(global_ns):
    ns = global_ns.namespace('::declarations::calldef')
    return_default_args = ns.calldef('return_default_args')

    # Legacy way of fetching dependencies. Is still valid but deprecated
    warnings.simplefilter("ignore", Warning)
    dependencies_old = return_default_args.i_depend_on_them()
    warnings.simplefilter("error", Warning)
    assert len(dependencies_old) == 3
    used_types = [
        dependency.depend_on_it.decl_string
        for dependency in dependencies_old]
    assert used_types == ['int', 'int', 'bool']

    dependencies_new = declarations.get_dependencies_from_decl(
        return_default_args)
    assert len(dependencies_new) == 3
    used_types = [
        dependency.depend_on_it.decl_string
        for dependency in dependencies_new]
    assert used_types == ['int', 'int', 'bool']


def test_coverage(global_ns):
    declarations.get_dependencies_from_decl(global_ns)
