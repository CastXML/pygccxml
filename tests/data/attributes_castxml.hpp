// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#ifndef __attributes_castxml_hpp__
#define __attributes_castxml_hpp__

#define _out_ __attribute__ ((annotate ("out")))
#define _sealed_ __attribute__ ((annotate ("sealed")))
#define _no_throw_ __attribute__ ((annotate ("no throw")))

namespace attributes{

struct _sealed_ numeric_t{

    _no_throw_ void do_nothing( _out_ int& x ){}

};

}

#endif//__attributes_castxml_hpp__

