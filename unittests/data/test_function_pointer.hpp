// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

// func1 is a function pointer
// In this case, func1 is the declaration of a function which has two arguments
// (on the right) and returns nothing (void on the left)
void (*func1)(int, double);

// Another pointer, but not a function pointer
int const volatile* myPointer;

// A struct
struct some_struct_t{};

// Another function pointer
typedef void (some_struct_t::*x8)();
