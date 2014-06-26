// Copyright 2014 Insight Software Consortium.
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
