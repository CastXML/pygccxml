// Copyright 2004-2013 Roman Yakovenko
// Copyright 2014 Insight Software Consortium
// Distributed under the Boost Software License, Version 1.0.
// (See accompanying file LICENSE.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef example_hpp_12_10_2006
#define example_hpp_12_10_2006


namespace unittests{

struct test_results{

    enum status{ ok, fail, error };

    void update( const char* test_name, status result );
};

struct test_case{

    test_case( const char* test_case_name );

    virtual void set_up(){}

    virtual void tear_down(){}

    virtual void run() = 0;

private:
    const char* m_name;
};

class test_container;

struct test_suite : public test_case{

    test_suite( const char* name, const test_container& tests );

    void run();

    const test_results& get_results() const
    { return m_results; }

private:
    test_container* m_tests;
    test_results m_results;
};

}

#endif//example_hpp_12_10_2006
