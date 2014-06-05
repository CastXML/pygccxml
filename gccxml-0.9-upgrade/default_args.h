// Copyright 2004-2007 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#include <string>
#include <vector>

typedef unsigned long long ull;
void fix_numeric( ull arg=(ull)-1 );

namespace function_call{
    inline int calc( int,int, int){ return 0; }
    void fix_function_call( int i=calc( 1,2,3) );
}

namespace typedef_{

struct original_name{
    original_name(){}
};

typedef original_name alias;

}
 
void typedef__func( const typedef_::alias& position = typedef_::alias() );

using namespace typedef_;
void typedef__func2( const typedef_::alias& position = alias() );

namespace osg{
    struct node{};
    node* clone_tree( const std::vector<std::string> &types=std::vector<std::string>() );
    
}

/*struct default_arg_t{};*/
/*default_arg_t create_default_argument();*/
/*void double_call( default_arg_t x=create_default_argument() );*/
