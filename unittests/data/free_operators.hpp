// Copyright 2004-2013 Roman Yakovenko
// Copyright 2014 Insight Software Consortium
// Distributed under the Boost Software License, Version 1.0.
// (See accompanying file LICENSE.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef __free_operators_to_be_exported_hpp__
#define __free_operators_to_be_exported_hpp__

namespace free_operators{

struct number{
    int i;

    number operator*( int ii ) const {
        number n2 = { i * ii };
        return n2;
    }
};

struct rational{
    int x, y;
};

number operator+( const number& x, int y ){
    number z;
    z.i = x.i + y;
    return z;
}

bool operator!( const number& x ){
    return !x.i;
}

number operator*( const number& n,  double i ){
    number n2 = { n.i * i };
    return n2;
}

number operator*( double i, const number& n ){
    number n2 = { n.i * i };
    return n2;
}

rational operator*( int i, const rational& r ){
    rational rr = { r.x * i, r.y };
    return rr;
}

bool operator!( const rational& x ){
    return !x.x;
}


}


#endif//__free_operators_to_be_exported_hpp__
