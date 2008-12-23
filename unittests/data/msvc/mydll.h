#pragma once

#include <memory>


class __declspec(dllexport) number_t{
public:
	number_t();
	explicit number_t(int value);
	virtual ~number_t();
	void print_it() const;
	int get_value() const;
	int get_value(){ return m_value; }
	void set_value(int x);

	number_t clone() const;
	std::auto_ptr<number_t> clone_ptr() const;
private:
	int m_value;
};

template class __declspec(dllexport) std::auto_ptr< number_t >;

typedef std::auto_ptr< number_t > number_aptr_t;

enum{ auto_ptr_size = sizeof( number_aptr_t ) };

__declspec(dllexport) void do_smth( number_aptr_t& );

__declspec(dllexport) extern int my_global_int;

typedef void(*do_smth_type)( number_aptr_t& );

__declspec(dllexport) extern volatile int my_volatile_global_variable;

__declspec(dllexport) extern int my_global_array[10];

__declspec(dllexport) void* get_pvoid(void*);
__declspec(dllexport) void** get_ppvoid(void);


class __declspec(dllexport) myclass_t{
public:
    static int my_static_member;
    static const int my_const_static_member;
    volatile int my_volatile_member;
    
    do_smth_type* get_do_smth(){ return 0; }
    void set_do_smth(do_smth_type*){};
    
};