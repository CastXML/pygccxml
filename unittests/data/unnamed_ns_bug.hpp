// Copyright 2004-2013 Roman Yakovenko
// Copyright 2014 Insight Software Consortium
// Distributed under the Boost Software License, Version 1.0.
// (See accompanying file LICENSE.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef __unnamed_ns_bug_hpp__
#define __unnamed_ns_bug_hpp__

// unnamed namespace
namespace{
   bool bool_var;
}

namespace ns{

class test_t{
public:
   int var;
};

}


#endif//__unnamed_ns_bug_hpp__
