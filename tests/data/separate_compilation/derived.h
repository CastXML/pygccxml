#ifndef __derived_h_10062009__
#define __derived_h_10062009__ 1

#include "base.h"

namespace buggy{

class derived_t: public base_t{
public:

    virtual ~derived_t() {};
    virtual data_t* get_data() const;

private:
    data_t::pair_t data_pair;
};

}

#endif//__derived_h_10062009__
