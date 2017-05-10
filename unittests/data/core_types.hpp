// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#ifndef __core_types_hpp__
#define __core_types_hpp__

#include <iostream>

#define USE_SYMBOL( X ) enum{ x##__LINE__ = sizeof(X) };


namespace core{ namespace types{

typedef void typedef_void;
typedef char typedef_char;
typedef signed char typedef_signed_char;
typedef unsigned char typedef_unsigned_char;
typedef wchar_t typedef_wchar_t;
typedef short int typedef_short_int;
typedef signed short int typedef_signed_short_int;
typedef short unsigned int typedef_short_unsigned_int;
typedef bool typedef_bool;
typedef int typedef_int;
typedef signed int typedef_signed_int;
typedef unsigned int typedef_unsigned_int;
typedef long int typedef_long_int;
typedef long unsigned int typedef_long_unsigned_int;
typedef long long int typedef_long_long_int;
typedef long long unsigned int typedef_long_long_unsigned_int;
typedef float typedef_float;
typedef double typedef_double;
typedef long double typedef_long_double;

typedef const int typedef_const_int;
USE_SYMBOL( typedef_const_int );

typedef int * typedef_pointer_int;
typedef int& typedef_reference_int;
typedef const unsigned int * const typedef_const_unsigned_int_const_pointer;
typedef volatile int typedef_volatile_int;
typedef const volatile int typedef_const_volatile_int;
int array255[255];

enum EFavoriteDrinks{ WATER, MILK, GIN_BEEFEATER, LIQUEUR_IRISH_CREAM  };
typedef EFavoriteDrinks typedef_EFavoriteDrinks;

typedef int (*function_ptr)(int, double);

struct exception{};

struct members_pointers_t{
	int some_function( double hi, int i ){
		return 0;
	}
	int some_function( double hi) const throw( exception ){
		return 0;
	};
    int m_some_const_member;
    int xxx;
};

typedef int (members_pointers_t::*member_function_ptr_t)( double )const;

typedef int (members_pointers_t::*member_variable_ptr_t);

member_variable_ptr_t member_variable_ptr_ = 0;

} }

#endif//__core_types_hpp__

