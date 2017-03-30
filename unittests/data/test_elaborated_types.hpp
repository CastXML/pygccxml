// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

namespace elaborated_t {

    class FooClass {};
    struct FooStruct {};
    enum FooEnum {e1};
    union FooUnion {};

    namespace yes {

        class FooClass c1 = {};
        const class FooClass c2 = {};
        volatile class FooClass c3 = {};
        volatile const class FooClass c4 = {};
        const volatile class FooClass c5 = {};

        typedef class FooClass cc1;
        typedef const class FooClass cc2;
        typedef volatile class FooClass cc3;
        typedef volatile const class FooClass cc4;
        typedef const volatile class FooClass cc5;

        class FooClass *c1ptr;
        const class FooClass *c2ptr;
        volatile class FooClass *c3ptr;
        volatile const class FooClass *c4ptr;
        const volatile class FooClass *c5ptr;

        typedef class FooClass *cc1ptr;
        typedef const class FooClass *cc2ptr;
        typedef volatile class FooClass *cc3ptr;
        typedef volatile const class FooClass *cc4ptr;
        typedef const volatile class FooClass *cc5ptr;

        struct FooStruct s1 = {};
        const struct FooStruct s2 = {};
        volatile struct FooStruct s3 = {};
        volatile const struct FooStruct s4 = {};
        const volatile struct FooStruct s5 = {};

        typedef struct FooStruct ss1;
        typedef const struct FooStruct ss2;
        typedef volatile struct FooStruct ss3;
        typedef volatile const struct FooStruct ss4;
        typedef const volatile struct FooStruct ss5;

        struct FooStruct *s1ptr;
        const struct FooStruct *s2ptr;
        volatile struct FooStruct *s3ptr;
        volatile const struct FooStruct *s4ptr;
        const volatile struct FooStruct *s5ptr;

        typedef struct FooStruct *ss1ptr;
        typedef const struct FooStruct *ss2ptr;
        typedef volatile struct FooStruct *ss3ptr;
        typedef volatile const struct FooStruct *ss4ptr;
        typedef const volatile struct FooStruct *ss5ptr;

        enum FooEnum e1;
        //const enum FooEnum e2; (not valid c++)
        volatile enum FooEnum e3;
        //volatile const enum FooEnum e4; (not valid c++)
        //const volatile enum FooEnum e5; (not valid c++)

        enum FooEnum *e1ptr;
        const enum FooEnum *e2ptr;
        volatile enum FooEnum *e3ptr;
        volatile const enum FooEnum *e4ptr;
        const volatile enum FooEnum *e5ptr;

        typedef enum FooEnum *ee1ptr;
        typedef const enum FooEnum *ee2ptr;
        typedef volatile enum FooEnum *ee3ptr;
        typedef volatile const enum FooEnum *ee4ptr;
        typedef const volatile enum FooEnum *ee5ptr;

        union FooUnion u1;
        const union FooUnion u2;
        volatile union FooUnion u3;
        volatile const union FooUnion e4;
        const volatile union FooUnion e5;

        union FooUnion *u1ptr;
        const union FooUnion *u2ptr;
        volatile union FooUnion *u3ptr;
        volatile const union FooUnion *u4ptr;
        const volatile union FooUnion *u5ptr;

        typedef union FooUnion *uu1ptr;
        typedef const union FooUnion *uu2ptr;
        typedef volatile union FooUnion *uu3ptr;
        typedef volatile const union FooUnion *uu4ptr;
        typedef const volatile union FooUnion *uu5ptr;

    }

    namespace no {

        FooClass c1 = {};
        const FooClass c2 = {};
        volatile FooClass c3 = {};
        volatile const FooClass c4 = {};
        const volatile FooClass c5 = {};

        typedef FooClass cc1;
        typedef const FooClass cc2;
        typedef volatile FooClass cc3;
        typedef volatile const FooClass cc4;
        typedef const volatile FooClass cc5;

        FooClass *c1ptr;
        const FooClass *c2ptr;
        volatile FooClass *c3ptr;
        volatile const FooClass *c4ptr;
        const volatile FooClass *c5ptr;

        typedef FooClass *cc1ptr;
        typedef const FooClass *cc2ptr;
        typedef volatile FooClass *cc3ptr;
        typedef volatile const FooClass *cc4ptr;
        typedef const volatile FooClass *cc5ptr;

        FooStruct s1 = {};
        const FooStruct s2 = {};
        volatile FooStruct s3 = {};
        volatile const FooStruct s4 = {};
        const volatile FooStruct s5 = {};

        typedef FooStruct ss1;
        typedef const FooStruct ss2;
        typedef volatile FooStruct ss3;
        typedef volatile const FooStruct ss4;
        typedef const volatile FooStruct ss5;

        FooStruct *s1ptr;
        const FooStruct *s2ptr;
        volatile FooStruct *s3ptr;
        volatile const FooStruct *s4ptr;
        const volatile FooStruct *s5ptr;

        typedef FooStruct *ss1ptr;
        typedef const FooStruct *ss2ptr;
        typedef volatile FooStruct *ss3ptr;
        typedef volatile const FooStruct *ss4ptr;
        typedef const volatile FooStruct *ss5ptr;

        FooEnum e1;
        //const enum FooEnum e2; (not valid c++)
        volatile FooEnum e3;
        //volatile const FooEnum e4; (not valid c++)
        //const volatile FooEnum e5; (not valid c++)

        FooEnum *e1ptr;
        const FooEnum *e2ptr;
        volatile FooEnum *e3ptr;
        volatile const FooEnum *e4ptr;
        const volatile FooEnum *e5ptr;

        typedef FooEnum *ee1ptr;
        typedef const FooEnum *ee2ptr;
        typedef volatile FooEnum *ee3ptr;
        typedef volatile const FooEnum *ee4ptr;
        typedef const volatile FooEnum *ee5ptr;

        FooUnion u1;
        const FooUnion u2;
        volatile FooUnion u3;
        volatile const FooUnion e4;
        const volatile FooUnion e5;

        FooUnion *u1ptr;
        const FooUnion *u2ptr;
        volatile FooUnion *u3ptr;
        volatile const FooUnion *u4ptr;
        const volatile FooUnion *u5ptr;

        typedef FooUnion *uu1ptr;
        typedef const FooUnion *uu2ptr;
        typedef volatile FooUnion *uu3ptr;
        typedef volatile const FooUnion *uu4ptr;
        typedef const volatile FooUnion *uu5ptr;

    }
}