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

#ifndef __demangled_hpp
#define __demangled_hpp

namespace demangled{

template< unsigned long i1, unsigned long i2, unsigned long i3>
struct item_t{
   static const unsigned long v1 = i1;
   static const unsigned long v2 = i2;
   static const unsigned long v3 = i3;
};

struct buggy{
   typedef unsigned long ulong;
   typedef item_t< ulong( 0xDEECE66DUL ) | (ulong(0x5) << 32), 0xB, ulong(1) << 31 > my_item_t;
   my_item_t my_item_var;
};


}

void set_a();

#endif//__demangled_hpp
