# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os

from . import autoconfig

from pygccxml import parser
from pygccxml import declarations


__code = os.linesep.join([
    'struct a{};',
    'struct b{};',
    'struct c{};',
    'struct d : public a{};',
    'struct e : public a, public b{};',
    'struct f{};',
    'struct g : public d, public f{};',
    'struct h : public f{};',
    'struct i : public h, public g{};'])


__recursive_bases = {
    'a': set(),
    'b': set(),
    'c': set(),
    'd': {'a'},
    'e': {'a', 'b'},
    'f': set(),
    'g': {'d', 'f', 'a'},
    'h': {'f'},
    'i': {'h', 'g', 'd', 'f', 'a'}}

__recursive_derived = {
    'a': {'d', 'e', 'g', 'i'},
    'b': {'e'},
    'c': set(),
    'd': {'g', 'i'},
    'e': set(),
    'f': {'g', 'h', 'i'},
    'g': {'i'},
    'h': {'i'},
    'i': set()}


def test_recursive_bases():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    src_reader = parser.source_reader_t(config)
    decls = declarations.make_flatten(src_reader.read_string(__code))
    classes = [
        inst for inst in decls if isinstance(inst, declarations.class_t)]
    for class_ in classes:
        assert class_.name in __recursive_bases
        all_bases = class_.recursive_bases
        control_bases = __recursive_bases[class_.name]
        assert len(control_bases) == len(all_bases)
        all_bases_names = [hi.related_class.name for hi in all_bases]
        assert set(all_bases_names) == control_bases


def test_recursive_derived():
    config = autoconfig.cxx_parsers_cfg.config.clone()
    src_reader = parser.source_reader_t(config)
    decls = declarations.make_flatten(src_reader.read_string(__code))
    classes = [
        inst for inst in decls if isinstance(
            inst,
            declarations.class_t)]
    for class_ in classes:
        assert class_.name in __recursive_derived
        all_derived = class_.recursive_derived
        control_derived = __recursive_derived[class_.name]
        assert len(control_derived) == len(all_derived)
        all_derived_names = [hi.related_class.name for hi in all_derived]
        assert set(all_derived_names) == control_derived
