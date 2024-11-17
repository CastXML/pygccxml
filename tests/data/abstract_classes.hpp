// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#ifndef __abstract_classes_hpp__
#define __abstract_classes_hpp__

namespace abstract_classes{

class abstract_i{
    virtual int do_your_things() const = 0;
};

class derived_abstract_i: public abstract_i{
};

class implementation : public abstract_i{
    virtual int do_your_things() const
    { return 1; }
};

}

#endif//__abstract_classes_hpp__

