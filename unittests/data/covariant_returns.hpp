// Copyright 2014-2017 Insight Software Consortium.
// Copyright 2004-2009 Roman Yakovenko.
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
