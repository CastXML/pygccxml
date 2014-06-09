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

#ifndef __bug_virtual_functions_overload_to_be_exported_hpp__
#define __bug_virtual_functions_overload_to_be_exported_hpp__

struct data_t {
    int i;
};

struct more_data_t : public data_t{
};

struct algorithm_t{
    algorithm_t(){};
    virtual data_t* f(){
        data_t* d = new data_t();
        d->i = 0;
        return d;
    }
};

class better_algorithm_t : public algorithm_t{
public:
    better_algorithm_t(){};
    virtual more_data_t* f(){
        more_data_t* d = new more_data_t();
        d->i = 1;
        return d;
    }

};

#endif//__bug_virtual_functions_overload_to_be_exported_hpp__
