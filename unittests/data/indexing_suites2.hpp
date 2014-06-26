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

#ifndef __indexing_suites2_to_be_exported_hpp__
#define __indexing_suites2_to_be_exported_hpp__

#include <vector>
#include <string>
#include <map>
#include <set>

namespace indexing_suites2 {

typedef std::vector< std::string > strings_t;

inline void do_nothing( const strings_t& ){}

struct item_t{
    item_t() : value( -1 ){}
    explicit item_t( int v) : value( v ){}

    bool operator==(item_t const& item) const {
        return value == item.value;
    }

    bool operator!=(item_t const& item) const {
        return value != item.value;
    }

    int value;
};


typedef std::vector<item_t> items_t;

typedef std::vector<item_t*> items_ptr_t;
inline items_ptr_t create_items_ptr(){
    items_ptr_t items;
    items.push_back( new item_t(0) );
    items.push_back( new item_t(1) );
    items.push_back( new item_t(2) );
    items.push_back( new item_t(3) );
    items.push_back( new item_t(4) );
    return items;
}

inline item_t get_value( const std::vector<item_t>& vec, unsigned int index ){
    return vec.at(index);
}

inline void set_value( std::vector<item_t>& vec, unsigned int index, item_t value ){
    vec.at(index);
    vec[index] = value;
}

typedef std::vector<float> fvector;
fvector empty_fvector(){ return fvector(); }

typedef std::map< std::string, std::string > name2value_t;
inline std::string get_first_name( name2value_t const * names ){
    if( !names ){
        return "";
    }
    else{
        return names->begin()->first;
    }
}


typedef std::multimap< int, int > multimap_ints_t;
inline multimap_ints_t create_multimap_ints(){
    return multimap_ints_t();
}

typedef std::set< std::string > set_strings_t;
inline set_strings_t create_set_strings(){
    return set_strings_t();
}

}

namespace pyplusplus{ namespace aliases{
    typedef std::vector<indexing_suites2::item_t*> items_ptr_t;
}}

namespace infinite_loop{
    std::map< std::string, int > test_infinite_loop();
}

#endif//__indexing_suites2_to_be_exported_hpp__
