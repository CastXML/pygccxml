#ifndef __data_h_10062009__
#define __data_h_10062009__ 1

namespace std{

template<class T1, class T2>
struct pair{
    typedef pair<T1, T2> _Myt;
    typedef T1 first_type;
    typedef T2 second_type;

    pair(): first(T1()), second(T2())
    {}

    pair(const T1& t1, const T2& t2)
    : first(t1), second(t2)
    {}

    T1 first;	// the first stored value
    T2 second;	// the second stored value
};
}

namespace buggy{

struct data_t{
    typedef std::pair<data_t*, data_t*> pair_t;
};

}

#endif//__data_h_10062009__
