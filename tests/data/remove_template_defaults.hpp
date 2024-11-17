// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
// Distributed under the Boost Software License, Version 1.0.
// See http://www.boost.org/LICENSE_1_0.txt

#ifndef __remove_template_defaults_hpp__
#define __remove_template_defaults_hpp__

#if defined( __GCCXML__ )
    #if defined( __GNUC__ )
        #include <ext/hash_set>
        #include <ext/hash_map>
        #define HASH_XXX_NS __gnu_cxx
    #else
        #include <hash_set>
        #include <hash_map>
        #if !defined( __PYGCCXML_MSVC9__ )
            #define HASH_XXX_NS std
        #else
            #define HASH_XXX_NS stdext
        #endif

    #endif

    #define HASH_XXX_UMAP hash_map
    #define HASH_XXX_USET hash_set
    #define HASH_XXX_UMMAP hash_multimap
    #define HASH_XXX_UMMSET hash_multiset
#endif

#if defined( __castxml__ )

    #if defined( __llvm__ )
        // This is for CastXML and llvm

        // When parsing with clang//llvm use the new c++11 (c++0x even ?)
        // unordered_maps and unordered_sets

        // First, include a library that does nothing ...
        // This will force the preprocessor to load _LIBCPP_VERSION
        #include <ciso646>

        #if defined( _LIBCPP_VERSION )
            // libc++ (mostly OS X)
            #include <unordered_map>
            #include <unordered_set>
            #define HASH_XXX_NS std
        #else
            // libstd++ (mostly Linux)
            #include <tr1/unordered_map>
            #include <tr1/unordered_set>
            #define HASH_XXX_NS std::tr1
        #endif
        #define HASH_XXX_UMAP unordered_map
        #define HASH_XXX_USET unordered_set
        #define HASH_XXX_UMMAP unordered_multimap
        #define HASH_XXX_UMMSET unordered_multiset
    #elif defined( _MSC_VER )
        // This is for CastXML and Visual Studio
        #include <unordered_map>
        #include <unordered_set>
        #define HASH_XXX_NS std::tr1
        #define HASH_XXX_UMAP unordered_map
        #define HASH_XXX_USET unordered_set
        #define HASH_XXX_UMMAP unordered_multimap
        #define HASH_XXX_UMMSET unordered_multiset
    #else
        #if ((__GNUC__ > 4) || \
             (__GNUC__ == 4 && __GNUC_MINOR__ > 4) || \
             (__GNUC__ == 4 && __GNUC_MINOR__ == 4 && __GNUC_PATCHLEVEL__ == 7))

            // Use TR1 containers for gcc >= 4.4.7 or MSCV + castxml
            // (this might work on older versions of gcc too, needs testing)
            #include <tr1/unordered_map>
            #include <tr1/unordered_set>
            #define HASH_XXX_NS std::tr1

            #define HASH_XXX_UMAP unordered_map
            #define HASH_XXX_USET unordered_set
            #define HASH_XXX_UMMAP unordered_multimap
            #define HASH_XXX_UMMSET unordered_multiset
        #else
            // Older versions of gcc are not tested.
            // 4.4.7 is already quite old.
            #error "Not tested"
        #endif

    #endif

#endif

#include <string>
#include <vector>
#include <deque>
#include <queue>
#include <list>
#include <set>
#include <map>

namespace rtd{

template <class T>
struct type {};

namespace vectors{
    typedef std::vector< int > v_int;
    typedef std::vector< std::string > v_string;
    typedef std::vector< v_int > v_v_int;
}

namespace lists{
    typedef std::list< int > l_int;
    typedef std::list< std::wstring > l_wstring;
}

namespace deques{
    typedef std::deque< std::vector< int > > d_v_int;
    typedef std::deque< std::list< std::string > > d_l_string;
}

namespace queues{
    typedef std::queue< int > q_int;
    typedef std::queue< std::string > q_string;

}

namespace priority_queues{
    typedef std::priority_queue< int > pq_int;
    typedef std::priority_queue< std::string > pq_string;

}

namespace sets{
    typedef std::set< std::vector< int > > s_v_int;
    typedef std::set< std::string > s_string;

}

namespace multiset_sets{
    typedef std::multiset< std::vector< int > > ms_v_int;
    typedef std::multiset< std::string > ms_string;

}

namespace maps{
    typedef std::map< int, double > m_i2d;
    typedef std::map< std::wstring, double > m_wstr2d;
    typedef std::map< const std::vector< int >, m_wstr2d > m_v_i2m_wstr2d;

    inline std::map<std::string, int> f2() {
        std::map<std::string, int> list;
        return list;
    }

}

namespace multimaps{
    typedef std::multimap< int, double > mm_i2d;
    typedef std::multimap< std::wstring const, double > mm_wstr2d;
    typedef std::multimap< std::vector< int > const, mm_wstr2d const > mm_v_i2mm_wstr2d;
}

namespace hash_sets{
    typedef HASH_XXX_NS::HASH_XXX_USET< std::vector< int > > hs_v_int;
    typedef HASH_XXX_NS::HASH_XXX_USET< std::string > hs_string;

}

namespace hash_multisets{
    typedef HASH_XXX_NS::HASH_XXX_UMMSET< std::vector< int > > mhs_v_int;
    typedef HASH_XXX_NS::HASH_XXX_UMMSET< std::string > mhs_string;
}

namespace hash_maps{
    typedef HASH_XXX_NS::HASH_XXX_UMAP< int, double > hm_i2d;
    typedef HASH_XXX_NS::HASH_XXX_UMAP< std::wstring, double > hm_wstr2d;
}

namespace hash_multimaps{
    typedef HASH_XXX_NS::HASH_XXX_UMMAP< int, double > hmm_i2d;
    typedef HASH_XXX_NS::HASH_XXX_UMMAP< std::wstring const, double > hmm_wstr2d;
    typedef HASH_XXX_NS::HASH_XXX_UMMAP< std::vector< int > const, hmm_wstr2d const > hmm_v_i2mm_wstr2d;
}

inline void f1( type< sets::s_v_int > ){
}

}

#endif//__remove_template_defaults_hpp__
