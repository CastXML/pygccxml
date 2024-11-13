# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import fnmatch
import subprocess


def test_example():
    """Runs the example in the docs directory"""

    env = os.environ.copy()

    # Get the path to current directory
    path = os.path.dirname(os.path.realpath(__file__))
    # Set the COVERAGE_PROCESS_START env. variable.
    # Allows to cover files run in a subprocess
    # http://nedbatchelder.com/code/coverage/subprocess.html
    env["COVERAGE_PROCESS_START"] = path + "/../.coveragerc"

    # Find all the examples files
    file_paths = []
    for root, _, filenames in os.walk(path + "/../docs/examples"):
        for file_path in fnmatch.filter(filenames, '*.py'):
            file_paths.append(os.path.join(root, file_path))

    for file_path in file_paths:
        return_code = subprocess.call(
            ["python", path + "/example_tester_wrap.py", file_path],
            env=env)
        assert return_code == 0
