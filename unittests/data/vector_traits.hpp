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

// Copyright 2004-2008 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#include <string>
#include <vector>



struct _0_{};

typedef std::vector< _0_ > container;


namespace vector_traits{
namespace yes{
    struct _1_{
        typedef int value_type;
        typedef std::vector< int > container;

        container do_nothing(){};
    };

    struct _2_{
        typedef _0_ value_type;
        typedef std::vector< _0_ > container;

        container do_nothing(){};
    };

    struct _3_{
        typedef std::string value_type;
        typedef std::vector< std::string > container;

        container do_nothing(){};
    };

    struct _4_{
        typedef std::vector<int> value_type;
        typedef std::vector< std::vector<int> > container;

        container do_nothing(){};
    };

    struct _5_{
        typedef int value_type;
        typedef const std::vector< int > container;

        container do_nothing(){};
    };

}

namespace no{
    struct _1_{
        template< class T >
        struct vector{};

        typedef vector<int> container;
    };

    struct _2_{
        typedef const std::vector< const int >& container;
    };
}

}

void do_nothing( std::vector< std::wstring >& );
