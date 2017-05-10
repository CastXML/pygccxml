// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
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

