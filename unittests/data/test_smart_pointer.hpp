// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#include <iostream>
#include <memory>
#include <vector>
#include <set>

std::shared_ptr<int> yes1(new int { 6 });
std::auto_ptr<double> yes2( new double { 7.0 } );

std::vector<int> no1;
std::set< std::string > no2;
