// Copyright 2021 Insight Software Consortium.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

namespace deprecation {


    class  __attribute__((deprecated("Test class Deprecated"))) test
    {
    public:
      test();
      __attribute__((deprecated("One arg constructor is Deprecated"))) test(int a);

      int hello();
      void __attribute__((deprecated("Function is deprecated"))) goodbye();
    };
     enum __attribute__((deprecated("Enumeration is Deprecated"))) com_enum {
      One = 1,
      Two = 2
    };
}