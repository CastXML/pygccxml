#include <iostream>
using namespace std;

namespace ns{
    class Test 
    { 
        public: 
        string var;  
    }; 
    
    int TestFunction1(Test a, Test b) 
    {
        return 0;
    }

    int TestFunction2(Test a, Test b=Test()) 
    {
        return 0;
    }
}
