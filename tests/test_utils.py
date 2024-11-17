# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

import os
import warnings

from pygccxml import utils


def test_contains_parent_dir():
    path = os.path.normpath("/mypath/folder1/folder2/folder3")
    dirs = [
        os.path.normpath("/mypath/folder1/folder2/"),
        os.path.normpath("/mypath3/folder1/folder2/folder3"),
        os.path.normpath("home"),
        os.path.normpath("/test/test1/mypath")]

    assert utils.utils.contains_parent_dir(path, dirs) is True

    dirs = [os.path.normpath("/home"), os.path.normpath("/mypath/test/")]

    assert utils.utils.contains_parent_dir(path, dirs) is False


def test_deprecation_wrapper():
    """
    The DeprecationWrapper is not part of the public API

    We still need to test it.
    """

    a = utils.utils.DeprecationWrapper(
        DeprecatedClass,
        "DeprecatedClass",
        "NewClass",
        "1.9.0")
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        a()
        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "deprecated" in str(w[-1].message)


class DeprecatedClass(object):
    """
    An empty class used for testing purposes.
    """
    pass
