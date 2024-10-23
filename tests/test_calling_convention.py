# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

from pygccxml import declarations


def test_extract():
    data = [
        ('thiscall',
            '(public: __thiscall std::auto_ptr<class pof::number_t>' +
            '::auto_ptr<class pof::number_t>(class std::auto_ptr' +
            '<class pof::number_t> &))'),
        ('',  "(const pof::number_t::`vftable')")]

    for expected, text in data:
        got = declarations.CALLING_CONVENTION_TYPES.extract(text)
        assert got == expected
