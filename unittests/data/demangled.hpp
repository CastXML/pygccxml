// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
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
