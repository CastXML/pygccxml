/*=========================================================================
 *
 *  Copyright 2014 Insight Software Consortium
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

// Copyright 2004-2013 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#ifndef __declarations_calldef_hpp__
#define __declarations_calldef_hpp__

namespace declarations{ namespace calldef{

class some_exception_t{};

class other_exception_t{};

void no_return_no_args();

int return_no_args();

void no_return_1_arg(int arg);

int return_default_args( int arg=1, bool flag=false );

extern void static_call();

void calldef_with_throw() throw( some_exception_t, other_exception_t );

struct calldefs_t{
    calldefs_t();

    explicit calldefs_t(char);

    calldefs_t(some_exception_t);

    calldefs_t(int,double);

    calldefs_t(const calldefs_t&);

    virtual ~calldefs_t();

    calldefs_t& operator=( const calldefs_t& );
    bool operator==( const calldefs_t& );
    operator char*() const;
    virtual operator double();

    static void static_call();

    inline int member_inline_call(int i){ return i;}

    virtual void member_virtual_call();

    virtual void member_pure_virtual_call() = 0;

    void member_const_call() const;

    calldefs_t* do_smth(const calldefs_t& other);
};

namespace std{
    class iostream;
}

std::iostream& operator<<( std::iostream&, const calldefs_t& );
std::iostream& operator>>( std::iostream&, calldefs_t& );

namespace ellipsis_tester{

struct ellipsis{
    void do_smth( int, ... );
};

void do_smth_else( int, ... );

}//ellipsis_tester

} }

#endif//__declarations_calldef_hpp__
