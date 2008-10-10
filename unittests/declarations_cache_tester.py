# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0. (See
# accompanying file LICENSE_1_0.txt or copy at
# http://www.boost.org/LICENSE_1_0.txt)

import os, sys, unittest, os.path
import autoconfig
import pygccxml.parser
from pygccxml.parser.config import config_t
from pygccxml.parser.declarations_cache import *

class decl_cache_tester(unittest.TestCase):
    def __init__(self, *args ):
        unittest.TestCase.__init__(self, *args)
        if not os.path.exists( autoconfig.build_directory ):
            os.makedirs( autoconfig.build_directory )

    def test_file_signature(self):
        file1 = os.path.join(autoconfig.data_directory, 'decl_cache_file1.txt')
        file1_dup = os.path.join(autoconfig.data_directory, 'decl_cache_file1_duplicate.txt')
        file2 = os.path.join(autoconfig.data_directory, 'decl_cache_file2.txt')
        sig1 = file_signature(file1)
        sig1_dup = file_signature(file1_dup)
        sig2 = file_signature(file2)
        self.assert_(sig1 == sig1_dup)
        self.assert_(sig1 != sig2)
        
    def test_config_signature(self):
        diff_cfg_list = self.build_differing_cfg_list()
        def_cfg = diff_cfg_list[0]
        def_sig = configuration_signature(def_cfg)
        
        # Test changes that should cause sig changes
        for cfg in diff_cfg_list[1:]:
            self.assert_(configuration_signature(cfg) != def_sig)
        
        # Test changes that should not cause sig changes
        no_changes = def_cfg.clone()
        self.assert_(configuration_signature(no_changes) == def_sig)
        
        #start_decls_changed = def_cfg.clone()
        #start_decls_changed.start_with_declarations = "test object"
        #self.assert_(configuration_signature(start_decls_changed) == def_sig)
               
        ignore_changed = def_cfg.clone()
        ignore_changed.ignore_gccxml_output = True
        self.assert_(configuration_signature(ignore_changed) == def_sig)
        
    def test_cache_interface(self):
        cache_file = os.path.join(autoconfig.build_directory, 'decl_cache_test.test_cache_read.cache')
        file1 = os.path.join(autoconfig.data_directory, 'decl_cache_file1.txt')
        file1_dup = os.path.join(autoconfig.data_directory, 'decl_cache_file1_duplicate.txt')
        file2 = os.path.join(autoconfig.data_directory, 'decl_cache_file2.txt')
        diff_cfg_list = self.build_differing_cfg_list()
        def_cfg = diff_cfg_list[0]
        
        if os.path.exists(cache_file):
            os.remove(cache_file)
        
        cache = file_cache_t(cache_file)
        self.assert_(len(cache._file_cache_t__cache) == 0)
        
        # test creating new entries for differing files
        cache.update(file1, def_cfg, 1,[])
        self.assert_(len(cache._file_cache_t__cache) == 1)
        cache.update(file1_dup, def_cfg, 2,[])
        self.assert_(len(cache._file_cache_t__cache) == 1)
        cache.update(file2, def_cfg, 3,[])
        self.assert_(len(cache._file_cache_t__cache) == 2)
        
        self.assert_(cache.cached_value(file1,def_cfg) == 2)
        self.assert_(cache.cached_value(file2,def_cfg) == 3)
        
        # Test reading again
        cache.flush()
        cache = file_cache_t(cache_file)
        self.assert_(len(cache._file_cache_t__cache) == 2)
        self.assert_(cache.cached_value(file1,def_cfg) == 2)
        self.assert_(cache.cached_value(file2,def_cfg) == 3)
        
        # Test flushing doesn't happen if we don't touch the cache
        cache = file_cache_t(cache_file)        
        self.assert_(cache.cached_value(file1,def_cfg) == 2)  # Read from cache
        cache.flush()    # should not actually flush
        cache = file_cache_t(cache_file)
        self.assert_(len(cache._file_cache_t__cache) == 2)
        
        # Test flush culling
        cache = file_cache_t(cache_file)
        cache.update(file1_dup, def_cfg, 4,[])    # Modify cache
        cache.flush()    # should cull off one entry
        cache = file_cache_t(cache_file)
        self.assert_(len(cache._file_cache_t__cache) == 1)
        
        
    def build_differing_cfg_list(self):
        """ Return a list of configurations that all differ. """
        cfg_list = []
        def_cfg = config_t("gccxml_path",'.',['tmp'],['sym'],['unsym'],
                               None,False,"")
        cfg_list.append(def_cfg)
                
        # Test changes that should cause sig changes
        gccxml_changed = def_cfg.clone()
        gccxml_changed.gccxml_path = "other_path"
        cfg_list.append(gccxml_changed)
        
        wd_changed = def_cfg.clone()
        wd_changed.working_directory = "other_dir"
        cfg_list.append(wd_changed)
        
        #inc_changed = def_cfg.clone()
        #inc_changed.include_paths = ["/var/tmp"]
        #self.assert_(configuration_signature(inc_changed) != def_sig)
        inc_changed = config_t("gccxml_path",'.',['/var/tmp'],['sym'],['unsym'],
                               None,False,"")
        cfg_list.append(inc_changed)

        #def_changed = def_cfg.clone()
        #def_changed.define_symbols = ["symbol"]
        #self.assert_(configuration_signature(def_changed) != def_sig)
        def_changed = config_t("gccxml_path",'.',['/var/tmp'],['new-sym'],['unsym'],
                               None,False,"")
        cfg_list.append(def_changed)

        #undef_changed = def_cfg.clone()
        #undef_changed.undefine_symbols = ["symbol"]
        #self.assert_(configuration_signature(undef_changed) != def_sig)
        undef_changed = config_t("gccxml_path",'.',['/var/tmp'],['sym'],['new-unsym'],
                               None,False,"")
        cfg_list.append(undef_changed)
        
        cflags_changed = def_cfg.clone()
        cflags_changed.cflags = "new flags"
        cfg_list.append(cflags_changed)
        
        return cfg_list
        
        
def create_suite():
    suite = unittest.TestSuite()    
    suite.addTest( unittest.makeSuite(decl_cache_tester))
    return suite

def run_suite():
    unittest.TextTestRunner(verbosity=2).run( create_suite() )

if __name__ == "__main__":
    run_suite()
