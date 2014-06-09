/*=========================================================================
 *
 *  Copyright 2014 Insight Software Consortium
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *         http://www.apache.org/licenses/LICENSE-2.0.txt
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 *=========================================================================*/

// Copyright 2004-2013 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

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
