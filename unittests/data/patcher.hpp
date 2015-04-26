// Copyright 2014-2015 Insight Software Consortium.
// Copyright 2004-2008 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#ifndef __patcher_hpp__
#define __patcher_hpp__

#include <string>
#include <vector>

namespace ns1{ namespace ns2{

enum fruit{ apple, orange };

} }

void fix_enum( ns1::ns2::fruit arg=ns1::ns2::apple );

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

/*struct default_arg_t{};*/
/*default_arg_t create_default_argument();*/
/*void double_call( default_arg_t x=create_default_argument() );*/
#endif//__patcher_hpp__
