/*=========================================================================
 *
 *  Copyright Insight Software Consortium
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *         http://www.apache.org/licenses/LICENSE-2.0.txt
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 *=========================================================================*/

// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

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
