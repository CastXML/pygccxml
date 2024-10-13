#ifndef __base_h_10062009__
#define __base_h_10062009__ 1

#include "data.h"

namespace buggy{

struct base_t{
    virtual ~base_t() {};
    virtual data_t* get_data() const = 0;
};

}

#endif//__base_h_10062009__
