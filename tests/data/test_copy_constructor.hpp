// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

typedef const int & myvar;

class test
{
    public:
        // The copy constructor
        test(const test & t0){};

        // A constructor
        test(const float & t0){};

        // A constructor with a typedef
        test(myvar t0){};
};

// An empty class; C++ will automatically create a copy constructor
class test2 {};
