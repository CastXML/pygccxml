// Copyright 2004-2013 Roman Yakovenko
// Copyright 2014 Insight Software Consortium
// Distributed under the Boost Software License, Version 1.0.
// (See accompanying file LICENSE.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef __core_ns_join_1_hpp__
#define __core_ns_join_1_hpp__

enum E11{ e11 };

namespace ns{

    enum E12{ e12 };

    namespace ns12{
        enum E13{ e13 };
    }

    namespace{
        enum E14{ e14 };
    }
}

#endif//__core_ns_join_1_hpp__
