// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#ifndef __classes_hpp__
#define __classes_hpp__

struct cls{};
typedef struct {} cls2;
typedef class {
   int i;
} cls3;

namespace ns{

    struct nested_cls{};
    typedef class {} nested_cls2;
    typedef struct nested_cls3 {} nested_cls3;

}

#endif//__classes_hpp__
