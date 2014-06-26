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

#ifndef __remove_template_defaults_hpp__
#define __remove_template_defaults_hpp__

#if defined( __GNUC__ )
    #include <ext/hash_set>
    #include <ext/hash_map>
    #define HASH_XXX_NS __gnu_cxx
#else
    #include <hash_set>
    #include <hash_map>
	#if defined( __GCCXML__ ) && !defined( __PYGCCXML_MSVC9__ )
		#define HASH_XXX_NS std
	#else
		#define HASH_XXX_NS stdext
	#endif//GCCXML
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

    inline std::map<std::string, int> f2(){}

}

namespace multimaps{
    typedef std::multimap< int, double > mm_i2d;
    typedef std::multimap< std::wstring const, double > mm_wstr2d;
    typedef std::multimap< std::vector< int > const, mm_wstr2d const > mm_v_i2mm_wstr2d;
}

namespace hash_sets{
    typedef HASH_XXX_NS::hash_set< std::vector< int > > hs_v_int;
    typedef HASH_XXX_NS::hash_set< std::string > hs_string;

}

namespace hash_multisets{
    typedef HASH_XXX_NS::hash_multiset< std::vector< int > > mhs_v_int;
    typedef HASH_XXX_NS::hash_multiset< std::string > mhs_string;
}

namespace hash_maps{
    typedef HASH_XXX_NS::hash_map< int, double > hm_i2d;
    typedef HASH_XXX_NS::hash_map< std::wstring, double > hm_wstr2d;
}

namespace hash_multimaps{
    typedef HASH_XXX_NS::hash_multimap< int, double > hmm_i2d;
    typedef HASH_XXX_NS::hash_multimap< std::wstring const, double > hmm_wstr2d;
    typedef HASH_XXX_NS::hash_multimap< std::vector< int > const, hmm_wstr2d const > hmm_v_i2mm_wstr2d;
}

inline void f1( type< sets::s_v_int > ){
}

}

#endif//__remove_template_defaults_hpp__
