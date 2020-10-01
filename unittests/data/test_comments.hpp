// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

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
};
