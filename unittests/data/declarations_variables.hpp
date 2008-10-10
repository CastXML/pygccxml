// Copyright 2004-2008 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef __declarations_variables_hpp__
#define __declarations_variables_hpp__

namespace declarations{ namespace variables{

const long unsigned int initialized = 10122004;
int array[255];

//TODO: explain why such variables is not peeked
extern int static_var;

struct struct_variables_t{
    mutable int m_mutable;
};

struct struct_variables_holder_t{
	struct_variables_t m_struct_variables;
};

} }

#endif//__declarations_variables_hpp__

