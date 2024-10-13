#if defined _WIN32 || defined __CYGWIN__
    #define IMPORT_SYMBOL __declspec(dllimport)
    #define EXPORT_SYMBOL __declspec(dllexport)
    #define PRIVATE_SYMBOL
#else
    #if __GNUC__ >= 4
        #define IMPORT_SYMBOL __attribute__ ((visibility("default")))
        #define EXPORT_SYMBOL __attribute__ ((visibility("default")))
        #define PRIVATE_SYMBOL  __attribute__ ((visibility("hidden")))
    #else
        #define IMPORT_SYMBOL
        #define EXPORT_SYMBOL
        #define PRIVATE_SYMBOL
  #endif
#endif
