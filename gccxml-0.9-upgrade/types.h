// Copyright 2004-2007 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#include <string>

struct mem_var_str_t{
    static std::string class_name;
    std::string identity(std::string x){ return x; }
};
