#!/usr/bin/env python
# Copyright 2014 Insight Software Consortium.
# Copyright 2004-2008 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

from setuptools import setup

setup(name="pygccxml",
      version="v1.6.0",
      author="Roman Yakovenko",
      author_email="roman yakovenko at gmail com",
      maintainer="Michka Popoff and the Insight Software Consortium",
      maintainer_email="gccxml@gccxml.org",
      description="Python package for easy C++ declarations navigation.",
      url="https://github.com/gccxml/pygccxml",
      download_url="https://github.com/gccxml/pygccxml/archive/master.zip",
      license="Boost",
      keywords="C++, declaration parser, gccxml",
      install_requires=["Python >= 2.7"],
      packages=["pygccxml",
                "pygccxml.declarations",
                "pygccxml.parser",
                "pygccxml.binary_parsers",
                "pygccxml.utils"],
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "Operating System :: MacOS :: MacOS X",
          "Operating System :: Microsoft :: Windows",
          "Operating System :: POSIX",
          "Programming Language :: Python",
          "Topic :: Software Development",
          ],
      )
