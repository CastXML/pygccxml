// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt


namespace declarations {
    namespace calldef {

        class some_exception_t{};

        class other_exception_t{};

        void calldef_with_throw() throw( some_exception_t, other_exception_t );

    }
}
