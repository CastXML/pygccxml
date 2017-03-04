// Copyright 2014-2016 Insight Software Consortium.
// Copyright 2004-2008 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#include <sstream>

// Demonstration of the real problem with basic c++
namespace Test1 {

// Forward declaration
class Base2;

// Base 1, with pointer to Base2
class Base1 {
  private:
    Base1();

  protected:
    Base2* aBasePtr2;
};

// Base 2, child class of Base1
class Base2: public Base1 {
  private:
    Base2();
};

// Child class of Base2
// Holds a pointer to Base2
class Child: public Base2 {
  private:
    Child();

  protected:
    Base2* aBasePtr2;
};

}

// Real-life test with std::istream where this happened
namespace Test2 {

class FileStreamDataStream {
  public:
    FileStreamDataStream(const std::istream* s) {}

  protected:
    std::istream* mInStream;
  };
}

