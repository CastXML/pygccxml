// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

namespace elaborated_t {

    class FooClass {};
    struct FooStruct {};
    enum FooEnum {e1};
    union FooUnion {};

    namespace yes_class {

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
        };

    namespace yes_struct {

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
        };

    namespace yes_enum {

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
        };

    namespace yes_union {

        union FooUnion u1;
        const union FooUnion u2 = {};
        volatile union FooUnion u3;
        volatile const union FooUnion e4 = {};
        const volatile union FooUnion e5 = {};

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
        };

    namespace no_class {

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
        };

    namespace no_struct {

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
        };

    namespace no_enum {

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
        };

    namespace no_union {

        FooUnion u1;
        const FooUnion u2 = {};
        volatile FooUnion u3;
        volatile const FooUnion e4 = {};
        const volatile FooUnion e5 = {};

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
        };

    namespace arguments_class {
        void testClass1(FooClass no, class FooClass yes);
        void testClass2(const FooClass no, const class FooClass yes);
        void testClass3(volatile FooClass no, volatile class FooClass yes);
        void testClass4(const volatile FooClass no, const volatile class FooClass yes);
        void testClass5(volatile const FooClass no, volatile const class FooClass yes);

        void testClass1ptr(FooClass *no, class FooClass *yes);
        void testClass2ptr(const FooClass *no, const class FooClass *yes);
        void testClass3ptr(volatile FooClass *no, volatile class FooClass *yes);
        void testClass4ptr(const volatile FooClass *no, const volatile class FooClass *yes);
        void testClass5ptr(volatile const FooClass *no, volatile const class FooClass *yes);

        void testClass1ref(FooClass &no, class FooClass &yes);
        void testClass2ref(const FooClass &no, const class FooClass &yes);
        void testClass3ref(volatile FooClass &no, volatile class FooClass &yes);
        void testClass4ref(const volatile FooClass &no, const volatile class FooClass &yes);
        void testClass5ref(volatile const FooClass &no, volatile const class FooClass &yes);
    }

    namespace arguments_struct {
        void testStruct1(FooStruct no, struct FooStruct yes);
        void testStruct2(const FooStruct no, const struct FooStruct yes);
        void testStruct3(volatile FooStruct no, volatile struct FooStruct yes);
        void testStruct4(const volatile FooStruct no, const volatile struct FooStruct yes);
        void testStruct5(volatile const FooStruct no, volatile const struct FooStruct yes);

        void testStruct1ptr(FooStruct *no, struct FooStruct *yes);
        void testStruct2ptr(const FooStruct *no, const struct FooStruct *yes);
        void testStruct3ptr(volatile FooStruct *no, volatile struct FooStruct *yes);
        void testStruct4ptr(const volatile FooStruct *no, const volatile struct FooStruct *yes);
        void testStruct5ptr(volatile const FooStruct *no, volatile const struct FooStruct *yes);

        void testStruct1ref(FooStruct &no, struct FooStruct &yes);
        void testStruct2ref(const FooStruct &no, const struct FooStruct &yes);
        void testStruct3ref(volatile FooStruct &no, volatile struct FooStruct &yes);
        void testStruct4ref(const volatile FooStruct &no, const volatile struct FooStruct &yes);
        void testStruct5ref(volatile const FooStruct &no, volatile const struct FooStruct &yes);
    }

    namespace arguments_enum {
        void testEnum1(FooEnum no, enum FooEnum yes);
        void testEnum2(const FooEnum no, const enum FooEnum yes);
        void testEnum3(volatile FooEnum no, volatile enum FooEnum yes);
        void testEnum4(const volatile FooEnum no, const volatile enum FooEnum yes);
        void testEnum5(volatile const FooEnum no, volatile const enum FooEnum yes);

        void testEnum1ptr(FooEnum *no, enum FooEnum *yes);
        void testEnum2ptr(const FooEnum *no, const enum FooEnum *yes);
        void testEnum3ptr(volatile FooEnum *no, volatile enum FooEnum *yes);
        void testEnum4ptr(const volatile FooEnum *no, const volatile enum FooEnum *yes);
        void testEnum5ptr(volatile const FooEnum *no, volatile const enum FooEnum *yes);

        void testEnum1ref(FooEnum &no, enum FooEnum &yes);
        void testEnum2ref(const FooEnum &no, const enum FooEnum &yes);
        void testEnum3ref(volatile FooEnum &no, volatile enum FooEnum &yes);
        void testEnum4ref(const volatile FooEnum &no, const volatile enum FooEnum &yes);
        void testEnum5ref(volatile const FooEnum &no, volatile const enum FooEnum &yes);
    }

    namespace arguments_union {
        void testUnion1(FooUnion no, union FooUnion yes);
        void testUnion2(const FooUnion no, const union FooUnion yes);
        void testUnion3(volatile FooUnion no, volatile union FooUnion yes);
        void testUnion4(const volatile FooUnion no, const volatile union FooUnion yes);
        void testUnion5(volatile const FooUnion no, volatile const union FooUnion yes);

        void testUnion1ptr(FooUnion *no, union FooUnion *yes);
        void testUnion2ptr(const FooUnion *no, const union FooUnion *yes);
        void testUnion3ptr(volatile FooUnion *no, volatile union FooUnion *yes);
        void testUnion4ptr(const volatile FooUnion *no, const volatile union FooUnion *yes);
        void testUnion5ptr(volatile const FooUnion *no, volatile const union FooUnion *yes);

        void testUnion1ref(FooUnion &no, union FooUnion &yes);
        void testUnion2ref(const FooUnion &no, const union FooUnion &yes);
        void testUnion3ref(volatile FooUnion &no, volatile union FooUnion &yes);
        void testUnion4ref(const volatile FooUnion &no, const volatile union FooUnion &yes);
        void testUnion5ref(volatile const FooUnion &no, volatile const union FooUnion &yes);
    }
}