// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#ifndef __declarations_variables_hpp__
#define __declarations_variables_hpp__

namespace declarations{ namespace variables{

const long unsigned int initialized = 10122004;
int array[255];

static int static_var;
extern int extern_var;

struct struct_variables_t{
    mutable int m_mutable;
};

struct struct_variables_holder_t{
	struct_variables_t m_struct_variables;
};

struct struct_static_variables_t{
    static const int ssv_static_var;
    static const int ssv_static_var_value = 1;
};

} }

#endif//__declarations_variables_hpp__

