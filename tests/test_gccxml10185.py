# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import pytest

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

code = \
    """
template <typename T> struct A {};
template <int N> struct A<const char[N]>
{ static int size(const char[N]) { return N - 1; } };
"""


def test_partial_template():
    """
    The purpose of this test was to check if changes to GCCXML
    would lead to changes in the outputted xml file (Meaning
    the bug was fixed).

    GCCXML wrongly outputted partial template specialization.
    CastXML does not have this bug. In this case we check if
    the template specialization can not be found; which is the
    expected/wanted behaviour.

    https://github.com/CastXML/CastXML/issues/20

    """

    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse_string(code, config)
    global_ns = declarations.get_global_namespace(decls)
    with pytest.raises(declarations.declaration_not_found_t):
        global_ns.class_('A<const char [N]>')
