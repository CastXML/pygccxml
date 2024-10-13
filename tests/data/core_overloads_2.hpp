// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#ifndef __core_overloads_2_hpp__
#define __core_overloads_2_hpp__
#include <string>
#include <set>
namespace core{ namespace overloads{

void do_nothing( std::set< std::string > );
void do_nothing( std::set< std::wstring > );

} }

#endif//__core_overloads_2_hpp__

