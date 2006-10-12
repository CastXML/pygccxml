// Copyright 2004 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef example_hpp_12_10_2006
#define example_hpp_12_10_2006


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

#endif//example_hpp_12_10_2006
