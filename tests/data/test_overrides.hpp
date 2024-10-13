// Copyright 2020 Insight Software Consortium.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt
#ifndef simple_h
#define simple_h

#include <iostream>
class base
{
public:
  base() {};
  ~base() {};
  virtual int goodbye(int num_ref, int num_times) = 0;
};

class simple : public base
{
public:
  simple() {};
  ~simple() {};
  int hello() { return 0; };
  int goodbye(int , int) override
    {
      std::cout << "goodbye\n";
      return 10;
    } ;
};

#endif
