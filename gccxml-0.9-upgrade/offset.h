// Copyright 2014-2015 Insight Software Consortium.
// Copyright 2004-2007 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

struct xyz_t{
    int do_smth( double );
    int m_some_member;
};

typedef int (xyz_t::*mfun_ptr_t)( double );

typedef int (xyz_t::*mvar_ptr_t);
