// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

// See https://github.com/CastXML/pygccxml/issues/180
// variant introduced in C++17
#include <variant>
std::variant<int, double, float> value;
