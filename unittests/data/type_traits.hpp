// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

//Almost all test cases have been taken
//from boost.type_traits (http://www.boost.org) library.

#include <string>
#include <iostream>
#include <vector>
#include <set>
#include <map>
#include "noncopyable.hpp"

#define TYPE_PERMUTATION( BASE, NAME )                        \
    typedef BASE NAME##_t;                                    \
    typedef BASE const NAME##_const_t;                        \
    typedef BASE volatile NAME##_volatile_t;                  \
    typedef BASE const volatile NAME##_const_volatile_t;


struct some_struct_t{
    void do_smth();
    int member;
};

namespace is_std_ostream{
namespace yes{
    typedef std::ostream ostream_type1;
    typedef std::ostream& ostream_type2;
    typedef const std::ostream& ostream_type3;
}
namespace no{
    typedef int int__;
}
}

namespace is_std_wostream{
namespace yes{
    typedef std::wostream wostream_type1;
    typedef std::wostream& wostream_type2;
    typedef const std::wostream& wostream_type3;
}
namespace no{
    typedef int int__;
}
}


struct incomplete_type;

namespace is_void{
namespace yes{
    TYPE_PERMUTATION( void, void )
}
namespace no{
    typedef void* void_ptr_t;
    typedef int int_t;
    typedef some_struct_t some_struct_alias_t;
    typedef incomplete_type incomplete_type_alias_t;
    typedef void(*function_t)();
    typedef void (some_struct_t::*member_function_t)();
} }

namespace is_void_pointer{
namespace yes{
    void *void_ptr1;
    typedef void *void_ptr2;
    void *ptr1 = 0;
}
namespace no{
    const void *ptr1;
    volatile void *ptr2;
    const volatile void *ptr3;
    typedef bool bool_t;
    typedef int int_t;
    typedef some_struct_t some_struct_alias_t;
    typedef incomplete_type incomplete_type_alias_t;
    typedef void(*function_t)();
    typedef void (some_struct_t::*member_function_t)();
} }

namespace is_bool{
namespace yes{
    TYPE_PERMUTATION( bool, bool )
}
namespace no{
    typedef void* void_ptr_t;
    typedef int int_t;
    typedef some_struct_t some_struct_alias_t;
    typedef incomplete_type incomplete_type_alias_t;
    typedef void(*function_t)();
    typedef void (some_struct_t::*member_function_t)();
} }

namespace is_noncopyable{

namespace detail{
    struct x{
    private:
        x( const x& );
        x& operator=(const x& );
    };

    struct y_type{
        union {
            struct {
                float x, y, z;
            };
            float val[3];
        };

        static const y_type zero;
    };

    struct instantiate_tmpls{
        instantiate_tmpls()
        : v(), s(), ms()
        {}

        std::vector< int > v;
        std::set< std::string > s;
        std::multimap< std::string, std::string > ms;
    };


    class a_t{
    public:

        static char get_a(){ return 'a'; }

    private:
        a_t(){};
        ~a_t(){};
    };

    class b_t{
        ~b_t(){}
    public:

        static char get_b(){ return 'b'; }

    };

    class c_t : public boost::noncopyable{
    public:
        static char get_c(){ return 'c'; }

    };

    class d_t{
    private:
        d_t( const d_t& );
    public:
        d_t(){}
        ~d_t(){}
        static char get_d(){ return 'd'; }

    };

    class dd_t : public d_t{
    public:
        dd_t(){}
        ~dd_t(){}
        static char get_dd(){ return 'D'; }
    };

    struct e_t{
        virtual void do_smth() = 0;
    private:
        c_t c;
    };

    struct f_t{
        f_t() : i(0){}
        virtual void do_smth() = 0;
    private:
        const int i;
    };

    struct g_t{
        enum E{e};
        g_t() : e_(e){}
        virtual void do_smth() = 0;
    private:
        const E e_;
    };

    struct const_item{ const int values[10]; };

    void test_const_item(const_item by_value);

    struct const_container{ const const_item items[10]; };

    void test_const_container(const_container by_value);

    enum semantic{ position, normal, binormal };
    enum element_type{ float_, color, short_ };

    struct vertex{
        protected:
            unsigned short source;
            size_t offset;
            semantic sem;
            element_type el_type;
        public:
            vertex( int x, int y, int z );

            bool operator==( const vertex& ) const;
    };
}

namespace yes{
    typedef detail::x x;
    typedef detail::a_t a_t;
    typedef detail::b_t b_t;
    typedef detail::c_t c_t;
    typedef detail::d_t d_t;
    typedef detail::dd_t dd_t;
    typedef detail::f_t f_t;
    typedef detail::g_t g_t;
    typedef detail::const_container const_container_t;
    typedef detail::const_item const_item_t;
    typedef detail::const_item *const_item_t_ptr;

}
namespace no{
    typedef std::string string_type;
    typedef detail::y_type y_type;
    typedef std::vector< int > vector_of_int_type;
    typedef std::set< std::string > string_set_type;
    typedef std::multimap< std::string, std::string > s2s_multimap_type;
    typedef detail::vertex vertex_type;
    typedef detail::vertex *vertex_type_ptr;
}
}



namespace is_calldef_pointer{

namespace details{
struct X{
    void do_smth( int ) const;
};

}

namespace yes{
    typedef void (*ff1)( int, int );
    typedef void ( details::X::*mf1)( int ) const;

    TYPE_PERMUTATION( ff1, ff1_type );
    TYPE_PERMUTATION( mf1, mf1_type );
}

namespace no{
    typedef int int_;
}

}

namespace is_integral{
namespace yes{

    TYPE_PERMUTATION( bool, bool )
    TYPE_PERMUTATION( char, char )
    TYPE_PERMUTATION( unsigned char, uchar )
    TYPE_PERMUTATION( short, short )
    TYPE_PERMUTATION( unsigned short, ushort )
    TYPE_PERMUTATION( int, int )
    TYPE_PERMUTATION( unsigned int, uint )
    TYPE_PERMUTATION( long, long )
    TYPE_PERMUTATION( unsigned long, ulong )
    TYPE_PERMUTATION( long long int, llint )
    TYPE_PERMUTATION( long long unsigned int, ulli )
}
namespace no{
    typedef some_struct_t some_struct_alias_t;
    typedef float* float_ptr_t;
    typedef float& float_ref_t;
    typedef const float& const_float_ref_t;
    typedef incomplete_type incomplete_type_alias;
    typedef void(*function_t)();
    typedef void (some_struct_t::*member_function_t)();
    TYPE_PERMUTATION( void, void )
    TYPE_PERMUTATION( float, float )
    TYPE_PERMUTATION( double, double )
    TYPE_PERMUTATION( long double, ldouble )
} }

namespace is_floating_point{
namespace yes{

    TYPE_PERMUTATION( float, float )
    TYPE_PERMUTATION( double, double )
    TYPE_PERMUTATION( long double, ldouble )
}
namespace no{
    typedef some_struct_t some_struct_alias_t;
    typedef float* float_ptr_t;
    typedef float& float_ref_t;
    typedef const float& const_float_ref_t;
    typedef incomplete_type incomplete_type_alias;
    typedef void(*function_t)();
    typedef void (some_struct_t::*member_function_t)();
    TYPE_PERMUTATION( void, void )
    TYPE_PERMUTATION( bool, bool )
    TYPE_PERMUTATION( char, char )
    TYPE_PERMUTATION( unsigned char, uchar )
    TYPE_PERMUTATION( short, short )
    TYPE_PERMUTATION( unsigned short, ushort )
    TYPE_PERMUTATION( int, int )
    TYPE_PERMUTATION( unsigned int, uint )
    TYPE_PERMUTATION( long, long )
    TYPE_PERMUTATION( unsigned long, ulong )
    TYPE_PERMUTATION( long long int, llint )
    TYPE_PERMUTATION( long long unsigned int, ulli )
} }

namespace is_fundamental{
namespace yes{

    TYPE_PERMUTATION( void, void )
    TYPE_PERMUTATION( bool, bool )
    TYPE_PERMUTATION( char, char )
    TYPE_PERMUTATION( unsigned char, uchar )
    TYPE_PERMUTATION( short, short )
    TYPE_PERMUTATION( unsigned short, ushort )
    TYPE_PERMUTATION( int, int )
    TYPE_PERMUTATION( unsigned int, uint )
    TYPE_PERMUTATION( long, long )
    TYPE_PERMUTATION( unsigned long, ulong )
    TYPE_PERMUTATION( long long int, llint )
    TYPE_PERMUTATION( long long unsigned int, ulli )
    TYPE_PERMUTATION( float, float )
    TYPE_PERMUTATION( double, double )
    TYPE_PERMUTATION( long double, ldouble )
}
namespace no{
    typedef some_struct_t some_struct_alias_t;
    typedef float* float_ptr_t;
    typedef float& float_ref_t;
    typedef const float& const_float_ref_t;
    typedef incomplete_type incomplete_type_alias;
    typedef void(*function_t)();
    typedef void (some_struct_t::*member_function_t)();

} }

namespace is_pointer{
namespace yes{
    typedef int* int_ptr_t;
    typedef const int* const_int_ptr_t;
    typedef volatile int* volatile_int_ptr_t;
    typedef some_struct_t* some_struct_ptr_t;
    typedef int* const int_const_ptr_t;
    typedef int* volatile int_volatile_ptr_t;
    typedef void(*function_t)();
    typedef void (some_struct_t::*member_function_t)();
}

namespace no{
    typedef int int_t;
    typedef int& int_ref_t;
    typedef some_struct_t some_struct_alias_t;
    typedef int*& int_ptr_ref_t;
} }


namespace remove_pointer{
namespace before{
    typedef int* x1;
    typedef const int* x2;
    typedef volatile int* x3;
    typedef some_struct_t* x4;
    typedef int* const x5;
    typedef int* volatile x6;
    typedef void(*x7)();
    // typedef void (some_struct_t::*x8)();
    // The last test is disabled but is covered by test_function_pointer.py
    // I do not know how to write the c++ code in the after pointer removal
    // namespace, as just removing the * will not work. But as this case is
    // covered elsewhere, it is okay to skip that one.
    // TODO: decide if last test (some_struct::*x8) needs to be removed
    // completely or written differently.
}

namespace after{
    typedef int x1;
    typedef const int x2;
    typedef volatile int x3;
    typedef some_struct_t x4;
    typedef int const x5;
    typedef int volatile x6;
    typedef void(x7)();
    // typedef void (some_struct_t::*x8)();
} }


namespace is_reference{
namespace yes{

    typedef int& int_ref_t;
    typedef const int& const_int_ref_t;
    typedef int const& int_const_ref_t;
    typedef some_struct_t& some_struct_ref_t;
    typedef int*& int_ptr_ref_t;
}

namespace no{
    typedef int* int_ptr_t;
    typedef const int* const_int_ptr_t;
    typedef volatile int* volatile_int_ptr_t;
    typedef some_struct_t* some_struct_ptr_t;
    typedef int* const int_const_ptr_t;
    typedef int* volatile int_volatile_ptr_t;
    typedef void(*function_t)();
    typedef void (some_struct_t::*member_function_t)();
    typedef int int_t;
} }

namespace remove_reference{
namespace before{

    typedef int& x1;
    typedef const int& x2;
    typedef some_struct_t& x3;
    typedef int*& x4;
    typedef void (some_struct_t::*x5)();
}

namespace after{
    typedef int x1;
    typedef const int x2;
    typedef some_struct_t x3;
    typedef int* x4;
    typedef void (some_struct_t::*x5)();
} }

namespace is_const{
namespace yes{

    typedef const void const_void_t;
    typedef const incomplete_type const_incomplete_type_t;
    typedef int* const int_const_t;
    typedef int* volatile const int_volatile_const_t;
    typedef int* const volatile int_const_volatile_t;
}

namespace no{
    typedef int* int_ptr_t;
    typedef const int* const_int_ptr_t;
    typedef volatile int* volatile_int_ptr_t;
    typedef some_struct_t* some_struct_ptr_t;
    typedef int* volatile int_volatile_ptr_t;
    typedef void(*function_t)();
    typedef void (some_struct_t::*member_function_t)();
    typedef int int_t;
    typedef const int& const_int_ref_t;
} }

namespace remove_const{
namespace before{
    typedef const void x1;
    typedef const incomplete_type x2;
    typedef int* const x3;
    typedef int* volatile x4;
    typedef void const * x5;
    typedef int volatile const x6;
    typedef int const volatile x7;

    typedef char arr_42[42];
    typedef char const arr_c_42[42];
    typedef char volatile arr_v_42[42];
    typedef char const volatile arr_cv_42[42];
    typedef char volatile const arr_vc_42[42];
}

namespace after{
    typedef void x1;
    typedef incomplete_type x2;
    typedef int* x3;
    typedef int* volatile x4;
    typedef void const * x5;
    typedef int volatile x6;
    typedef int volatile x7;

    typedef char arr_42[42];
    typedef char arr_c_42[42];
    typedef char volatile arr_v_42[42];
    typedef char volatile arr_cv_42[42];
    typedef char volatile arr_vc_42[42];
} }

namespace is_volatile{
namespace yes{

    typedef void * volatile vvoid_ptr_t;
    typedef volatile int volatile_int_t;
    typedef int* volatile const int_volatile_const_t;
    typedef int* const volatile int_const_volatile_t;
}

namespace no{
    typedef void volatile * void_ptr_to_v_t;
    typedef int* int_ptr_t;
    typedef const int* const_int_ptr_t;
    typedef int* volatile_int_ptr_t;
    typedef some_struct_t* some_struct_ptr_t;
    typedef int* int_volatile_ptr_t;
    typedef void(*function_t)();
    typedef void (some_struct_t::*member_function_t)();
    typedef int int_t;
} }

namespace remove_volatile{
namespace before{

    typedef void * volatile x1;
    typedef volatile int x2;
    typedef int* x3;
    typedef void volatile * x4;
    typedef int volatile const x5;
    typedef int const volatile x6;

    typedef char arr_42[42];
    typedef char const arr_c_42[42];
    typedef char volatile arr_v_42[42];
    typedef char const volatile arr_cv_42[42];
    typedef char volatile const arr_vc_42[42];
}

namespace after{
    typedef void * x1;
    typedef int x2;
    typedef int* x3;
    typedef void volatile * x4;
    typedef int const x5;
    typedef int const x6;

    typedef char arr_42[42];
    typedef char const arr_c_42[42];
    typedef char arr_v_42[42];
    typedef char const arr_cv_42[42];
    typedef char const arr_vc_42[42];
} }


namespace remove_cv{
namespace before{

    typedef void * volatile x10;
    typedef void * const volatile x11;
    typedef void * const x12;

    typedef volatile int x20;
    typedef const volatile int x21;
    typedef const int x22;

    typedef int* volatile x30;
    typedef int* const volatile x31;
    typedef int* const x32;

    typedef void(*x40)();

    typedef char arr_42[42];
    typedef char const arr_c_42[42];
    typedef char volatile arr_v_42[42];
    typedef char const volatile arr_cv_42[42];
    typedef char volatile const arr_vc_42[42];
}

namespace after{
    typedef void * x10;
    typedef void * x11;
    typedef void * x12;

    typedef int x20;
    typedef int x21;
    typedef int x22;

    typedef int* x30;
    typedef int* x31;
    typedef int* x32;

    typedef void(*x40)();

    typedef char arr_42[42];
    typedef char arr_c_42[42];
    typedef char arr_v_42[42];
    typedef char arr_cv_42[42];
    typedef char arr_vc_42[42];
} }


namespace is_enum{

    enum color{ red, green, blue };

namespace yes{
    typedef color COLOR;
}

namespace no{
    typedef int* int_ptr_t;
    typedef const int* const_int_ptr_t;
    typedef int* volatile_int_ptr_t;
    typedef some_struct_t* some_struct_ptr_t;
    typedef int* int_volatile_ptr_t;
    typedef void(*function_t)();
    typedef void (some_struct_t::*member_function_t)();
    typedef int int_t;
} }

namespace has_trivial_constructor{

namespace details{

    struct const_item{ const int values[10]; };
    struct const_container{ const const_item items[10]; };

#if __cplusplus >= 201103L || defined(_MSC_VER)
    // C++11 and later must use braces to trigger aggregate initialization.
    // Using parentheses will cause value-initialization, and since the
    // two classes above have implicitly deleted default constructors,
    // that causes default initialization to be performed, which is ill-formed.
    // Note: MSVC is using c++11 but still defines __cplusplus as 199711L. In
    // that case use the c++11 feature, because that specific one is supported.
    void test_const_item( const_item x = const_item{} );
    void test_const_container( const_container x = const_container{} );
#else
    void test_const_item( const_item x = const_item() );
    void test_const_container( const_container x = const_container() );
#endif

}

namespace yes{
    struct x{
        x(){}
    };
}

namespace no{

    class y{
        private:
        y(){}
    };

    class singleton_t
    {
    private:
        static singleton_t *m_instance;

        singleton_t () {}
        ~singleton_t () {}

    public:
        static singleton_t* instance();
    };

    typedef details::const_item const_item;
    typedef details::const_container const_container;
} }

namespace has_public_constructor{
namespace yes{
    struct x{
        x(){}
    };

    struct z{int i;};
}

namespace no{
    class y{
        private:
        y(){}
    };
} }

namespace has_public_destructor{
namespace yes{
    struct x{
        ~x(){}
    };
}

namespace no{
    class y{
        private:
        ~y(){}
    };
} }

namespace has_copy_constructor{
namespace yes{
    struct x{
        x(const x&){}
    };
    typedef is_noncopyable::detail::vertex vertex_type;
}

namespace no{
    class y{
        private:
        y(const y&){}
    };
} }

namespace is_base_and_derived{
namespace yes{
    struct base{};
    struct derived : public base {};
}

namespace no{
    struct unrelated1{};
    struct unrelated2{};
} }

namespace has_any_non_copyconstructor{
namespace yes{
    struct x{
        x(int){}
    };
}

namespace no{
    class y{
        private:
        y(){}
    };
} }

namespace is_unary_operator{

struct dummy{
    bool operator!(){ return true; }
    int operator++(){ return 0; }
    int operator+(const dummy& ){ return 0; }
};

inline int operator++( dummy& ){ return 0; }
inline int operator*( const dummy&, const dummy& ){ return 0; }

dummy& operator+=( dummy& x, const dummy& ){
    return x;
}

}

namespace is_array{

namespace yes{
    int yes1[2];
    const int yes2[2] = {0};
    const volatile int yes3[2] = {0};
    int yes4[2][3];
    int const yes5[2] = {0};
}

namespace no{
    typedef int no1;
    typedef int* no2;
    typedef const int* no3;
    typedef const volatile int* no4;
    typedef int*const no5;
    typedef const int*volatile no6;
    typedef const volatile int*const no7;
    typedef void( * no8)( const int[2] );
} }

namespace is_convertible{

template <class T>
struct convertible_from{
    convertible_from(T);
};

template <class T>
struct convertible_to{
    operator T ();

};

struct base{};

struct other{};

struct derived : base {};

struct derived_protected : protected base {};

struct derived_private : private base {};

struct base2{};

struct middle2 : virtual base2 {};

struct derived2 : middle2 {};

enum fruit{ apple };

template < typename source_type_, typename target_type_, int value_ >
struct tester_t{
    typedef source_type_ source_type;
    typedef target_type_ target_type;
    enum expected{ value=value_ };
};

template < typename source_type_, typename target_type_, int value_ >
struct tester_source_t{
    typedef source_type_ source_type;
    typedef target_type_ target_type;
    enum expected{ value=value_ };

private:
    enum { sizeof_source = sizeof( source_type ) };
};

template < typename source_type_, typename target_type_, int value_ >
struct tester_target_t{
    typedef source_type_ source_type;
    typedef target_type_ target_type;
    enum expected{ value=value_ };

private:
    enum { sizeof_target = sizeof( target_type ) };
};

template < typename source_type_, typename target_type_, int value_ >
struct tester_both_t{
    typedef source_type_ source_type;
    typedef target_type_ target_type;
    enum expected{ value=value_ };

private:
    enum { sizeof_source = sizeof( source_type ) };
    enum { sizeof_target = sizeof( target_type ) };
};

struct  x1 : public tester_t< const int *, int*, false >{};
struct  x2 : public tester_t< int *, const int*, true >{};
struct  x3 : public tester_t< const int&, int&, false >{};
struct  x4 : public tester_t< const int&, int, true >{};
struct  x5 : public tester_t< const int&, char, true >{};
struct  x6 : public tester_t< const int&, char&, false >{};
struct  x7 : public tester_t< const int&, char*, false >{};
struct  x8 : public tester_t< int&, const int&, true >{};
struct  x9 : public tester_t< int *, const int*, true >{};
struct x10 : public tester_t< int&, const int&, true >{};
struct x11 : public tester_t< float, int, true >{};
struct x12 : public tester_t< double, int, true >{};
struct x13 : public tester_t< double, float, true >{};
struct x14 : public tester_t< long, int, true >{};
struct x15 : public tester_t< int, char, true >{};
struct x16 : public tester_t< long long, int, true >{};
struct x17 : public tester_t< long long, char, true >{};
struct x18 : public tester_t< long long, float, true >{};
struct x19 : public tester_t< float, int, true >{};
struct x20 : public tester_t< float, void, false >{};
struct x21 : public tester_t< void, void, true >{};
struct x22 : public tester_t< double, void*, true >{};
struct x23 : public tester_t< double, int*, false >{};
struct x24 : public tester_t< int, int*, false >{};
struct x25 : public tester_t< const int, int*, false >{};
struct x26 : public tester_t< const int&, int*, false >{};
struct x27 : public tester_t< double*, int*, false >{};
struct x28 : public tester_source_t< convertible_to<int>, int, true >{};
struct x29 : public tester_target_t< int, convertible_to<int>, false >{};
struct x30 : public tester_source_t< convertible_to<float const&>, float, true >{};
struct x31 : public tester_target_t< float, convertible_to<float const&>, false >{};
struct x32 : public tester_source_t< convertible_to<float&>, float, true >{};
struct x33 : public tester_target_t< float, convertible_to<float&>, false >{};
struct x34 : public tester_source_t< convertible_to<char>, float, true >{};
struct x35 : public tester_target_t< float, convertible_to<char>, false >{};
struct x36 : public tester_source_t< convertible_to<char const&>, float, true >{};
struct x37 : public tester_target_t< float, convertible_to<char const&>, false >{};
struct x38 : public tester_source_t< convertible_to<char&>, float, true >{};
struct x39 : public tester_target_t< float, convertible_to<char&>, false >{};
struct x40 : public tester_source_t< convertible_to<char>, char, true >{};
struct x41 : public tester_source_t< convertible_to<char const&>, char, true >{};
struct x42 : public tester_source_t< convertible_to<char&>, char, true >{};
struct x43 : public tester_source_t< convertible_to<float>, float&, true >{};
struct x44 : public tester_source_t< convertible_to<float>, float const&, true >{};
struct x45 : public tester_source_t< convertible_to<float&>, float&, true >{};
struct x46 : public tester_source_t< convertible_to<float const&>, float const&, true >{};
struct x47 : public tester_source_t< convertible_to<float const&>, float&, false >{};
struct x48 : public tester_target_t< float, convertible_from<float>, true >{};
struct x49 : public tester_target_t< float, convertible_from<float const&>, true >{};
struct x50 : public tester_target_t< float, convertible_from<float&>, true >{};
struct x51 : public tester_target_t< float, convertible_from<char>, true >{};
struct x52 : public tester_target_t< float, convertible_from<char const&>, true >{};
struct x53 : public tester_target_t< float, convertible_from<char&>, false >{};
struct x54 : public tester_target_t< char, convertible_from<char>, true >{};
struct x55 : public tester_target_t< char, convertible_from<char const&>, true >{};
struct x56 : public tester_target_t< char, convertible_from<char&>, true >{};
struct x57 : public tester_target_t< float&, convertible_from<float> , true >{};
struct x58 : public tester_target_t< float const&, convertible_from<float> , true >{};
struct x59 : public tester_target_t< float&, convertible_from<float&> , true >{};
struct x60 : public tester_target_t< float const&, convertible_from<float const&>, true >{};
struct x61 : public tester_target_t< float&, convertible_from<float const&>, true >{};
struct x62 : public tester_target_t< int,  convertible_from<int>, true >{};
struct x63 : public tester_t< const int*, int[3], false >{};
struct x64 : public tester_t< int(&)[4], const int*, true >{};
struct x65 : public tester_t< int(&)(int), int(*)(int), true >{};
struct x66 : public tester_t< int[2], int*, true >{};
struct x67 : public tester_t< int[2], const int*, true >{};
struct x68 : public tester_t< const int[2], int*, false >{};
struct x69 : public tester_t< int*, int[3], false >{};
struct x70 : public tester_t< float, int&, false >{};
struct x71 : public tester_t< float, const int&, true >{};
struct x72 : public tester_t< other, void*, true >{};
struct x73 : public tester_t< int, void*, false >{};
struct x74 : public tester_t< fruit, void*, false >{};
struct x75 : public tester_t< other, int*, false >{};
struct x76 : public tester_t< other*, int*, false >{};
struct x77 : public tester_t< fruit, int, true >{};
struct x78 : public tester_t< fruit, double, true >{};
struct x79 : public tester_t< fruit, char, true >{};
struct x80 : public tester_t< fruit, wchar_t, true >{};
struct x81 : public tester_t< derived, base, true >{};
struct x82 : public tester_t< derived, derived, true >{};
struct x83 : public tester_t< base, base, true >{};
struct x84 : public tester_t< base, derived, false >{};
struct x85 : public tester_t< other, base, false >{};
struct x86 : public tester_t< middle2, base2, true >{};
struct x87 : public tester_t< derived2, base2, true >{};
struct x88 : public tester_t< derived*, base*, true >{};
struct x89 : public tester_t< base*, derived*, false >{};
struct x90 : public tester_t< derived&, base&, true >{};
struct x91 : public tester_t< base&, derived&, false >{};
struct x92 : public tester_t< const derived*, const base*, true >{};
struct x93 : public tester_t< const base*, const derived*, false >{};
struct x94 : public tester_t< const derived&, const base&, true >{};
struct x95 : public tester_t< const base&, const derived&, false >{};
struct x96 : public tester_t< derived_private, base, false >{};
struct x97 : public tester_t< derived_protected, base, true >{};
struct x98 : public tester_t< derived_protected, derived_private, false >{};



// : public tester_t< test_abc3, const test_abc1&, true >{};
// : public tester_t< non_int_pointer, void*, true >{};
// : public tester_t< test_abc1&, test_abc2&, false >{};
// : public tester_t< test_abc1&, int_constructible, false >{};
// : public tester_t< int_constructible, test_abc1&, false >{};
// : public tester_t< test_abc1&, test_abc2, false >{};

//~  : public tester_t< polymorphic_derived1,polymorphic_base, true >{};
//~  : public tester_t< polymorphic_derived2,polymorphic_base, true >{};
//~  : public tester_t< polymorphic_base,polymorphic_derived1, false >{};
//~  : public tester_t< polymorphic_base,polymorphic_derived2, false >{};
//~ #ifndef BOOST_NO_IS_ABSTRACT
//~  : public tester_t< test_abc1,test_abc1, false >{};
//~  : public tester_t< Base,test_abc1, false >{};
//~  : public tester_t< polymorphic_derived2,test_abc1, false >{};
//~  : public tester_t< int,test_abc1, false >{};
//~ #endif


}
