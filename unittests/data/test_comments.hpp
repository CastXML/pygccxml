// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

//! Namespace Comment
//! Across multiple lines
namespace comment {

    /** class comment */
    class test
    {
    public:
      // Non-doc comment before.
      /** doc comment */
      // Non-doc comment after.
      test();

      /// cxx comment
      /// with multiple lines
      int hello();

      //! mutable field comment
      int val1 = 0;
      /// bit field comment
      double val2=2;

      /// inside class enum comment
      enum test_enum {
        One = 1,
        Two = 2
      };
    };

    /// Outside Class enum comment
    enum com_enum {
      One = 1,
      Two = 2
    };
}