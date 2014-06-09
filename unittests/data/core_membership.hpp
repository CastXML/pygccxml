/*=========================================================================
 *
 *  Copyright Insight Software Consortium
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

// Copyright 2004-2008 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#ifndef __core_membership_hpp__
#define __core_membership_hpp__

enum{ GLOBAL_NS_UNNAMED_ENUM = 18 };
enum EGlobal{ GLOBAL_NS };

namespace core{ namespace membership{

namespace enums_ns{
   enum{ WITHIN_NS_UNNAMED_ENUM = 3 };
   enum EWithin{ WITHIN_NS };
}

namespace{//unnamed namespace
    enum{ WITHIN_UNNAMED_NS_UNNAMED_ENUM = 1977 };
    enum EWithinUnnamed{ WITHIN_UNNAMED_NS };
}

class class_for_nested_enums_t{
public:
    enum ENestedPublic{ nested_enum_public };
protected:
    enum ENestedProtected{ nested_enum_protected };
private:
    enum ENestedPrivate{ nested_enum_private };
};

} }

#endif//__core_membership_hpp__

