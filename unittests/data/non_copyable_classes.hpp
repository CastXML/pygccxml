// Copyright 2014 Insight Software Consortium.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

// A non copyable class, see:
// http://stackoverflow.com/questions/2173746/how-do-i-make-this-c-object-non-copyable

#ifndef __non_copyable_classes_hpp__
#define __non_copyable_classes_hpp__

namespace non_copyable{

// A first base class, which can not be copied
class Foo1 {
  private:
    Foo1();
    Foo1( const Foo1& ); // non construction-copyable
    Foo1& operator=( const Foo1& ); // non copyable
  protected:
    int var;
  public:
    void set_values (int a)
      { var=a; }
};

class MainFoo1: public Foo1 {
  public:
    int get_var()
      { return var; }
};

// -----------------------------------------------

// Foo2 is a base class, with a non copiable const
// The constant is of type fundamental (int)
class Foo2 {
  private:
    Foo2();
  protected:
    const int var;
};

// Use the base class
class MainFoo2: public Foo2 {
  public:
    int get_var()
      { return var; }
};

// -----------------------------------------------

// A class which does nothing
class Something
{
public:
    int m_nValue;
};

// Foo3 is a base class, with a non copiable const
// The constant is a class
// See http://www.learncpp.com/cpp-tutorial/810-const-class-objects-and-member-functions/
class Foo3 {
  private:
    Foo3();
  protected:
    const Something cSomething; // calls default constructor
};

// Use the base class
class MainFoo3 : Foo3 {
  public:
    char b;
};

// -----------------------------------------------

// Foo4 is a base class, with a non copiable const
// The constant is an array
class Foo4 {
  private:
    Foo4();
  protected:
    const int foo [5];
};

// Use the base class
class MainFoo4 : Foo4 {
  public:
    char b;
};

}

#endif//__non_copyable_classes_hpp__
