import os
import unittest
import autoconfig

import pprint
from pygccxml.msvc import mspdb
from pygccxml import declarations
from pygccxml.msvc import common_utils as msvc_utils

pdb_file = r'E:\development\language-binding\pyplusplus_dev\pyplusplus\cpptypes\mydll\release\mydll.pdb'

reader = mspdb.decl_loader_t( pdb_file )
opt = mspdb.enums.UNDECORATE_NAME_OPTIONS.UNDNAME_SHORT_UNIQUE
opt = 0

public_smbls = {}
for smbl in reader.public_symbols.iterkeys():
    name = smbl.name
    undecorated_name = smbl.get_undecoratedNameEx(opt).strip()
    if undecorated_name.endswith( ')const' ):
        undecorated_name = undecorated_name[ : -len('const')]
    public_smbls[ name ] = undecorated_name
    public_smbls[ undecorated_name ] = name

pprint.pprint( public_smbls )

#~ for smbl in reader.symbols.itervalues():
    #~ if not smbl.classParent:
        #~ continue
    #~ undecorated_name = smbl.get_undecoratedNameEx(opt)
    #~ if not undecorated_name:
        #~ continue
    #~ undecorated_name = undecorated_name.strip()
    #~ if undecorated_name not in public_smbls:
        #~ continue
    #~ print '--------------------------------------'
    #~ print 'mem fun: ', undecorated_name
    #~ if smbl.classParent:
        #~ print 'parent class: ', smbl.classParent.name
    #~ else:
        #~ print 'no parent'
    #~ print '======================================'
reader.read()
f = file( 'decls.cpp', 'w+' )
declarations.print_declarations( reader.global_ns, writer=lambda line: f.write(line+'\n') )
f.close()

#~ f = file( 'symbols.txt', 'w+')
#~ for smbl in reader.symbols.itervalues():
    #~ f.write( smbl.uname )
    #~ f.write( os.linesep )
    #~ f.write( '\t' + str(smbl.name) )
#~ f.close()

