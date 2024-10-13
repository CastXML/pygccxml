// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

int myfunc (int a, int b)
{
  int r;
  r=a+b;
  return r;
}

class Box
{
    public:
       short myinternfunc()
       {
          return _x;
       }
    private:
        short _x;
};
