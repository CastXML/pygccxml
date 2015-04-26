// Copyright 2014-2015 Insight Software Consortium.
// Copyright 2004-2008 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#include <string>

namespace string_traits{
namespace yes{
    typedef std::string x1;
    typedef const std::string x2;
}

namespace no{
    typedef int x1;
    typedef std::string& x2;
}

}

namespace wstring_traits{
namespace yes{
    typedef std::wstring x1;
    typedef const std::wstring x2;
}

namespace no{
    typedef int x1;
    typedef std::wstring& x2;
}

}
