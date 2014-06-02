// Copyright 2004-2013 Roman Yakovenko
// Copyright 2014 Insight Software Consortium
// Distributed under the Boost Software License, Version 1.0.
// (See accompanying file LICENSE.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)


#ifndef __include_std_hpp__
#define __include_std_hpp__

#include <set>
#include <map>
#include <list>
#include <vector>
#include <locale>
#include <utility>
#include <iostream>

namespace instantiate{
    std::string str_a;
    std::wstring str_w;
    std::set<int> set_of_int;
    std::list<int> list_of_int;
    std::vector<int> vector_of_int;
    std::map< std::pair< std::wstring, std::string >, int > map_of_smth;
}

#endif//__include_std_hpp__


