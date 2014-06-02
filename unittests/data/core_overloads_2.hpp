// Copyright 2004-2013 Roman Yakovenko
// Copyright 2014 Insight Software Consortium
// Distributed under the Boost Software License, Version 1.0.
// (See accompanying file LICENSE.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef __core_overloads_2_hpp__
#define __core_overloads_2_hpp__
#include <string>
#include <set>
namespace core{ namespace overloads{

void do_nothing( std::set< std::string > );
void do_nothing( std::set< std::wstring > );

} }

#endif//__core_overloads_2_hpp__

