// Will only be defined when -fopenmp flag is included
// in ccflags of corresponding config object.
#ifdef _OPENMP
  namespace ccflags_test_namespace{}
#endif
