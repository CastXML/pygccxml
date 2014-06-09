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
