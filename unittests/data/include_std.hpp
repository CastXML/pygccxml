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


