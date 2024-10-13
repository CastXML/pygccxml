// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#ifndef __core_class_hierarchy_hpp__
#define __core_class_hierarchy_hpp__

namespace core{ namespace class_hierarchy{

class base_t{
public:
    virtual ~base_t(){};
};

class other_base_t{
};

class derived_public_t : public base_t{
};

class derived_protected_t : protected base_t{
};

class derived_private_t : private virtual base_t{
};

class multi_derived_t : derived_private_t, protected virtual base_t, private other_base_t{
};

} }

#endif//__core_class_hierarchy_hpp__
