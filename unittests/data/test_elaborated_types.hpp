// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

namespace elaborated_t {

    class Foo1 {};
    struct Foo2 {};

    namespace yes {

        class Foo1 c1 = {};
        const class Foo1 c2 = {};
        volatile class Foo1 c3 = {};
        volatile const class Foo1 c4 = {};
        const volatile class Foo1 c5 = {};

        typedef class Foo1 cc1;
        typedef const class Foo1 cc2;
        typedef volatile class Foo1 cc3;
        typedef volatile const class Foo1 cc4;
        typedef const volatile class Foo1 cc5;

        class Foo1 *c1ptr;
        const class Foo1 *c2ptr;
        volatile class Foo1 *c3ptr;
        volatile const class Foo1 *c4ptr;
        const volatile class Foo1 *c5ptr;

        typedef class Foo1 *cc1ptr;
        typedef const class Foo1 *cc2ptr;
        typedef volatile class Foo1 *cc3ptr;
        typedef volatile const class Foo1 *cc4ptr;
        typedef const volatile class Foo1 *cc5ptr;

        struct Foo2 s1 = {};
        const struct Foo2 s2 = {};
        volatile struct Foo2 s3 = {};
        volatile const struct Foo2 s4 = {};
        const volatile struct Foo2 s5 = {};

        typedef struct Foo2 ss1;
        typedef const struct Foo2 ss2;
        typedef volatile struct Foo2 ss3;
        typedef volatile const struct Foo2 ss4;
        typedef const volatile struct Foo2 ss5;

        struct Foo2 *s1ptr;
        const struct Foo2 *s2ptr;
        volatile struct Foo2 *s3ptr;
        volatile const struct Foo2 *s4ptr;
        const volatile struct Foo2 *s5ptr;

        typedef struct Foo2 *ss1ptr;
        typedef const struct Foo2 *ss2ptr;
        typedef volatile struct Foo2 *ss3ptr;
        typedef volatile const struct Foo2 *ss4ptr;
        typedef const volatile struct Foo2 *ss5ptr;

    }

    namespace no {

        Foo1 c1 = {};
        const Foo1 c2 = {};
        volatile Foo1 c3 = {};
        volatile const Foo1 c4 = {};
        const volatile Foo1 c5 = {};

        typedef Foo1 cc1;
        typedef const Foo1 cc2;
        typedef volatile Foo1 cc3;
        typedef volatile const Foo1 cc4;
        typedef const volatile Foo1 cc5;

        Foo1 *c1ptr;
        const Foo1 *c2ptr;
        volatile Foo1 *c3ptr;
        volatile const Foo1 *c4ptr;
        const volatile Foo1 *c5ptr;

        typedef Foo1 *cc1ptr;
        typedef const Foo1 *cc2ptr;
        typedef volatile Foo1 *cc3ptr;
        typedef volatile const Foo1 *cc4ptr;
        typedef const volatile Foo1 *cc5ptr;

        Foo2 s1 = {};
        const Foo2 s2 = {};
        volatile Foo2 s3 = {};
        volatile const Foo2 s4 = {};
        const volatile Foo2 s5 = {};

        typedef Foo2 ss1;
        typedef const Foo2 ss2;
        typedef volatile Foo2 ss3;
        typedef volatile const Foo2 ss4;
        typedef const volatile Foo2 ss5;

        Foo2 *s1ptr;
        const Foo2 *s2ptr;
        volatile Foo2 *s3ptr;
        volatile const Foo2 *s4ptr;
        const volatile Foo2 *s5ptr;

        typedef Foo2 *ss1ptr;
        typedef const Foo2 *ss2ptr;
        typedef volatile Foo2 *ss3ptr;
        typedef volatile const Foo2 *ss4ptr;
        typedef const volatile Foo2 *ss5ptr;

    }
}