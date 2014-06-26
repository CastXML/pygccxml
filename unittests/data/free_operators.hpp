/*=========================================================================
 *
 *  Copyright Insight Software Consortium
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *         http://www.apache.org/licenses/LICENSE-2.0.txt
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 *=========================================================================*/

// Copyright 2004-2008 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

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
