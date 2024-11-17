# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations

code = \
    """
class A {
public:
    virtual ~A() = 0;
    unsigned int a : 1;
    unsigned int unused : 31;
};
"""


def test_gccxml_10184():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    decls = parser.parse_string(code, config)
    global_ns = declarations.get_global_namespace(decls)
    assert global_ns.variable('a').bits == 1
    assert global_ns.variable('unused').bits == 31
