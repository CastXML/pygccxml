#ifndef __HELLO_H__
#define __HELLO_H__

#ifdef __cplusplus
extern "C"
{
#endif


void hello_print(const char *message);
double hello_sum(double x, double y);
void do_smth( int, ... );

#ifdef __cplusplus
}
#endif

#endif /* __HELLO_H__ */
