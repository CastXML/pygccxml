// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#include <string>
#include <vector>
using namespace std;

template<typename T>
class myClass {};

template<typename T, typename R>
class myClass2 {};

template<typename T, typename R, typename X>
class myClass3 {};

int main () {
  myClass<std::vector<char>(const std::string &, const std::string &)> m1;

  myClass<std::vector<int>(const int &, const int &)> m2;

  myClass2<std::vector<int>(const int &, const int &), std::vector<double>> m3;

  myClass2<std::vector<double>, std::vector<int>(const int &, const int &)> m4;

  myClass3<std::vector<double>, std::vector<int>(const int &, const int &), std::vector<int>(const int &, const int &)> m5;

  myClass3<std::vector<int>(const int &, const int &), std::vector<double>, std::vector<int>(const int &, const int &)> m6;

  myClass3<std::vector<int>(const int &, const int &), std::vector<int>(const int &, const int &), std::vector<double>> m7;

  myClass3<int, std::vector<int>(const int &, const int &), std::vector<int>(double &)> m8;

  return 0;
}


