// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

struct abstract{
  virtual void do_smth() = 0;
};

struct holder{
  abstract* ptr1;
  abstract* const ptr2;
};
