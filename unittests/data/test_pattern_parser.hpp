// Copyright 2014-2016 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#include <vector>
using namespace std;

template<typename T>
class myClass {};

int main () {
  myClass<std::vector<char>(const std::string &, const std::string &)> m;
  return 0;
}


