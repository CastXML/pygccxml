# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import sys

# This wrapper layer allows to execute the examples for the unittests
# in a separate environment, where the sys.path has been hacked to point
# to the pygccxml source tree (we do not want to pickup any pygccxml installed
# on the system). Unfortunately passing the PYTHONPATH as env variable to
# subprocess just appends to the sys.path ... here we want to insert at
# position 1 so that the right pygccxml is found


example_file = sys.argv[1]
example_folder = os.path.dirname(example_file)
root = os.path.normpath(
    os.path.dirname(sys.modules[__name__].__file__) + "/../")

# Add the root folder to the path, so that the examples are not run against
# whatever pygccxml version is installed
sys.path.insert(1, root)

# Hack the __file__ location, so that the example thinks it is in the
# docs/examples folder
sys.modules[__name__].__file__ = example_file

# Run the example
if sys.version_info[:2] >= (3, 0):
    with open(example_file) as f:
        code = compile(f.read(), example_file, "exec")
        exec(code, None, None)
else:
    execfile(example_file)
