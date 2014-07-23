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
    Foo1( const Foo1& other ); // non construction-copyable
    Foo1& operator=( const Foo1& ); // non copyable
  protected:
    int var;
  public:
    void set_values (int a)
      { var=a; }
};

// A second base class, with a non copiable const
class Foo2 {
  private:
  	Foo2();
  protected:
    const int var;
};

class MainFoo1: public Foo1 {
  public:
    int get_var()
      { return var; }
};

class MainFoo2: public Foo2 {
  public:
    int get_var()
      { return var; }
};

}

#endif//__non_copyable_classes_hpp__