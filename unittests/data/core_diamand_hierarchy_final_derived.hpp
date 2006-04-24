// Copyright 2004 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef __core_diamand_hierarchy_final_derived_hpp__
#define __core_diamand_hierarchy_final_derived_hpp__

#include "core_diamand_hierarchy_derived1.hpp"
#include "core_diamand_hierarchy_derived2.hpp"

namespace core{ namespace diamand_hierarchy{

class final_derived_t : public virtual derived1_t, public virtual derived2_t{
};

} }

#endif//__core_diamand_hierarchy_final_derived_hpp__
