// Copyright 2004-2013 Roman Yakovenko
// Copyright 2014 Insight Software Consortium
// Distributed under the Boost Software License, Version 1.0.
// (See accompanying file LICENSE.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

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
