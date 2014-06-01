// Copyright 2004-2013 Roman Yakovenko
// Copyright 2014 Insight Software Consortium
// Distributed under the Boost Software License, Version 1.0.
// (See accompanying file LICENSE.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef __bit_fields_hpp__
#define __bit_fields_hpp__

namespace bit_fields{

struct fields_t{
    unsigned int x : 1;
    unsigned int y : 7;
    unsigned int z;
};

}

#endif//__bit_fields_hpp__
