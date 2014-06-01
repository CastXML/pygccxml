// Copyright 2004-2013 Roman Yakovenko
// Copyright 2014 Insight Software Consortium
// Distributed under the Boost Software License, Version 1.0.
// (See accompanying file LICENSE.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef __core_class_hierarchy_hpp__
#define __core_class_hierarchy_hpp__

//TODO("To add virtual inheritance case");

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

class derived_private_t : private base_t{
};

class multi_derived_t : derived_private_t, protected base_t, private other_base_t{
};

} }

#endif//__core_class_hierarchy_hpp__
