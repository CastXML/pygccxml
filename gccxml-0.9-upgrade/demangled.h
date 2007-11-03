// Copyright 2004-2007 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

template< unsigned long i1>
struct item_t{
   static const unsigned long v1 = i1;
};

struct buggy{
   typedef unsigned long ulong;
   typedef item_t< ulong( 0xDEECE66DUL ) | (ulong(0x5) << 32) > my_item_t;
   my_item_t my_item_var;
};
