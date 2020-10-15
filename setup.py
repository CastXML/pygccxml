#!/usr/bin/env python
# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt

from setuptools import setup
from release_utils import utils

version = utils.find_version("../pygccxml/__init__.py")

requirements_test = {
  "coverage",
  "coveralls",
  "pycodestyle",
}
requirements_docs = {
  "sphinx",
  "sphinx_rtd_theme",
}

setup(name="pygccxml",
      version=version,
      author="Roman Yakovenko",
      author_email="romanyakovenko@gmail.com",
      maintainer="Michka Popoff and the Insight Software Consortium",
      maintainer_email="castxml@public.kitware.com",
      description="Python package for easy C++ declarations navigation.",
      url="https://github.com/CastXML/pygccxml",
      download_url="https://github.com/CastXML/pygccxml/archive/v" +
                   version + ".tar.gz",
      license="Boost",
      keywords="C++, declaration parser, CastXML, gccxml",
      packages=["pygccxml",
                "pygccxml.declarations",
                "pygccxml.parser",
                "pygccxml.utils"],
      extras_require={
          "test": list(requirements_test),
          "docs": list(requirements_docs),
      },
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "Operating System :: MacOS :: MacOS X",
          "Operating System :: Microsoft :: Windows",
          "Operating System :: POSIX",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
          "Topic :: Software Development",
          ],
      )
