// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

namespace elaborated_t {

    struct Foo1 {};

    namespace yes {

        struct Foo1 x1 = {};
        const struct Foo1 x2 = {};
        volatile struct Foo1 x3 = {};
        volatile const struct Foo1 x4 = {};
        const volatile struct Foo1 x5 = {};

        typedef struct Foo1 y1;
        typedef const struct Foo1 y2;
        typedef volatile struct Foo1 y3;
        typedef volatile const struct Foo1 y4;
        typedef const volatile struct Foo1 y5;

        struct Foo1 *x1ptr;
        const struct Foo1 *x2ptr;
        volatile struct Foo1 *x3ptr;
        volatile const struct Foo1 *x4ptr;
        const volatile struct Foo1 *x5ptr;

        typedef struct Foo1 *y1ptr;
        typedef const struct Foo1 *y2ptr;
        typedef volatile struct Foo1 *y3ptr;
        typedef volatile const struct Foo1 *y4ptr;
        typedef const volatile struct Foo1 *y5ptr;

    }

    namespace no {

        Foo1 x1 = {};
        const Foo1 x2 = {};
        volatile Foo1 x3 = {};
        volatile const Foo1 x4 = {};
        const volatile Foo1 x5 = {};

        typedef Foo1 y1;
        typedef const Foo1 y2;
        typedef volatile Foo1 y3;
        typedef volatile const Foo1 y4;
        typedef const volatile Foo1 y5;

        Foo1 *x1ptr;
        const Foo1 *x2ptr;
        volatile Foo1 *x3ptr;
        volatile const Foo1 *x4ptr;
        const volatile Foo1 *x5ptr;

        typedef Foo1 *y1ptr;
        typedef const Foo1 *y2ptr;
        typedef volatile Foo1 *y3ptr;
        typedef volatile const Foo1 *y4ptr;
        typedef const volatile Foo1 *y5ptr;

    }
}