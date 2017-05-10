// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#ifndef __patcher_hpp__
#define __patcher_hpp__

#include <string>
#include <vector>

namespace ns1{ namespace ns2{

enum fruit{ apple, orange };
void fix_enum2( fruit arg=apple );

} }

void fix_enum( ns1::ns2::fruit arg=ns1::ns2::apple );

namespace ns3{

using namespace ns1::ns2;
void fix_enum3( fruit arg=orange );

}

#if __cplusplus >= 201103L || defined(_MSC_VER)
namespace ns4{

enum class color {red, green, blue};
void fix_enum4( color arg=color::blue );

}

namespace ns5{

using namespace ns4;
void fix_enum5( color arg=color::blue );

}
#endif

typedef unsigned long long ull;
void fix_numeric( ull arg=(ull)-1 );

namespace fx{
    enum{ unnamed = 0 };
    void fix_unnamed( int x=unnamed );
}

namespace function_call{
    inline int calc( int,int, int){ return 0; }
    void fix_function_call( int i=calc( 1,2,3) );
}

namespace fundamental{
    enum spam { eggs };
    void fix_fundamental(unsigned int v=eggs);
}


namespace typedef_{

struct original_name{
    original_name(){}
};

typedef original_name alias;

}

void typedef__func( const typedef_::alias& position = typedef_::alias() );

namespace osg{
    struct node{};
    node* clone_tree( const std::vector<std::string> &types=std::vector<std::string>() );

}

namespace ns1{

static int const DEFAULT_1 = 0;
struct st1{
    static long const DEFAULT_2 = 10;
    void fun1( int arg1=DEFAULT_1, long=DEFAULT_2 );
};

}

static int const DEFAULT_1 = 20;
int fun2( int arg1=DEFAULT_1, int arg2=ns1::DEFAULT_1, long arg3=::ns1::st1::DEFAULT_2 );


enum ACE_Log_Priority_Index
{
  LM_INVALID_BIT_INDEX = 32
};
static int log_priority_enabled(long priority_index = LM_INVALID_BIT_INDEX);


/*struct default_arg_t{};*/
/*default_arg_t create_default_argument();*/
/*void double_call( default_arg_t x=create_default_argument() );*/
#endif//__patcher_hpp__
