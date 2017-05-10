// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

// Demonstrate some code where a struct without name is passed to a
// templated function. See bug #55

template <typename type>
void
function(type &var) {};

int main()
{
    // Create foo, a struct with no name
    struct { } foo;
    function(foo);
}
