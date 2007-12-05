// Copyright 2004-2007 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef example_hpp_12_10_2006
#define example_hpp_12_10_2006

#include <vector>
#include <string>
#include <map>

namespace unittests{

struct test_results{
    
    enum status{ ok, fail, error };
    
    typedef std::map< std::string, status > result_container;
    
    void update( const std::string& name, status result ){
        m_results[ name ] = result;
    }
    
private:    
    result_container m_results;
};
    
struct test_case{
    
    test_case( const std::string& name )
    : m_name( name )
    {}
    
    virtual void set_up(){}
        
    virtual void tear_down(){}
    
    virtual void run() = 0;
        
private:
    const std::string m_name;
};

struct test_suite : public test_case{
    
    typedef std::vector< test_case* > test_container;
    
    test_suite( const std::string& name, const test_container& tests )
    : test_case(name)
      , m_tests( tests )
    {}
        
    virtual void run();
       
    const test_results& get_results() const 
    { return m_results; }
    
private:    
    const test_container m_tests;
    test_results m_results;
};
    
}

#endif//example_hpp_12_10_2006
