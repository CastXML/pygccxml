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

namespace binary_operator{
namespace yes{
    typedef std::string yes1;

    struct trivial{
        bool operator==(const trivial& other);
    };

    typedef trivial yes2;

    struct external{
    };

    bool operator==( const external& left, const external& right );

    typedef external yes3;
}
namespace no{

    struct x1{
    private:
        bool operator==( const x1& other );
    };

    typedef x1 no1;
}
}
