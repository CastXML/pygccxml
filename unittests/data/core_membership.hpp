// Copyright 2004-2013 Roman Yakovenko
// Copyright 2014 Insight Software Consortium
// Distributed under the Boost Software License, Version 1.0.
// (See accompanying file LICENSE.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

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

