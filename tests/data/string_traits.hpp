// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#include <string>

namespace string_traits{
namespace yes{
    typedef std::string x1;
    typedef const std::string x2;
    typedef std::string& x3;
    typedef const std::string& x4;
}

namespace no{
    typedef int x1;
    typedef const int x2;
    typedef const int& x3;
}

}

namespace wstring_traits{
namespace yes{
    typedef std::wstring x1;
    typedef const std::wstring x2;
    typedef std::wstring& x3;
    typedef const std::wstring& x4;
}

namespace no{
    typedef int x1;
    typedef const int x2;
    typedef const int& x3;
}

}
