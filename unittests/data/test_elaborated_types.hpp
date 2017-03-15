// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

namespace elaborated_t {

    struct Foo1 {};

    namespace yes {
        struct Foo1 x1 = {};
    }

    namespace no {
        Foo1 x2 = {};
    }
}