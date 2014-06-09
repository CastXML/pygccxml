/*=========================================================================
 *
 *  Copyright 2014 Insight Software Consortium
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

// Copyright 2004-2013 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

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

