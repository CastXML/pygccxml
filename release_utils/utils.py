#!/usr/bin/env python
# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import io
import os
import re


def find_version(file_path):
    """
    Find the version of pygccxml.

    Used by setup.py and the sphinx's conf.py.
    Inspired by https://packaging.python.org/single_source_version/

    Args:
        file_path (str): path to the file containing the version.
    """

    with io.open(
            os.path.join(
                os.path.dirname(__file__),
                os.path.normpath(file_path)),
            encoding="utf8") as fp:
        content = fp.read()

    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              content, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")
