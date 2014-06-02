// Copyright 2004-2013 Roman Yakovenko
// Copyright 2014 Insight Software Consortium
// Distributed under the Boost Software License, Version 1.0.
// (See accompanying file LICENSE.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef __atributes_hpp__
#define __atributes_hpp__

#ifdef __GCCXML__

#define _out_ __attribute( (gccxml( "out" ) ) )
#define _sealed_ __attribute( (gccxml( "sealed" ) ) )
#define _no_throw_ __attribute( (gccxml( "no throw" ) ) )

namespace attributes{

_sealed_ struct numeric_t{

    _no_throw_ void do_nothing( _out_ int& x ){}

};

}

#endif//__GCCXML__

#endif//__atributes_hpp__

