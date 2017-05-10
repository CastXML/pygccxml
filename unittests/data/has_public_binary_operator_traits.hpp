// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#include <string>
#include <vector>

namespace binary_operator{
namespace yesequal{
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
namespace noequal{

    struct x1{
    private:
        bool operator==( const x1& other );
    };

    typedef x1 no1;
}
namespace yesless{
    typedef std::string yes1;

    struct trivial{
        bool operator<(const trivial& other);
    };

    typedef trivial yes2;

    struct external{
    };

    bool operator<( const external& left, const external& right );

    typedef external yes3;
}
namespace noless{

    struct x1{
    private:
        bool operator<( const x1& other );
    };

    typedef x1 no1;
}
}
