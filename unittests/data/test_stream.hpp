// Copyright 2014-2016 Insight Software Consortium.
// Copyright 2004-2008 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#include <sstream>

namespace Test2 {

class FileStreamDataStream {
  public:
    FileStreamDataStream(const std::istream* s) {}

  protected:
    std::istream* mInStream;
  };
}

