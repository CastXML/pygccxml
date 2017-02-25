# Copyright 2014-2017 Insight Software Consortium.
# Copyright 2004-2009 Roman Yakovenko.
# Distributed under the Boost Software License, Version 1.0.
# See http://www.boost.org/LICENSE_1_0.txt


class xml_generators(object):
    """
    Helper class for the xml generator versions
    """
    __gccxml_06 = "GCC-XML 0.6"
    __gccxml_07 = "GCC-XML 0.7"
    __gccxml_09 = "GCC-XML 0.9"
    __gccxml_09_buggy = "GCC-XML 0.9 BUGGY"
    __castxml = "CastXML"
    __separator = "@"

    def __init__(self, logger, xml_output_version):

        if xml_output_version is None:
            logger.debug("GCCXML version - 0.6")
            xml_generator = self.__gccxml_06
        elif xml_output_version <= 1.114:
            logger.debug("GCCXML version - 0.7")
            xml_generator = self.__gccxml_07
        elif 1.115 <= xml_output_version <= 1.126:
            logger.debug(
                "GCCXML version - 0.9 BUGGY ( %s )", xml_output_version)
            xml_generator = self.__gccxml_09_buggy
        elif 1.126 <= xml_output_version <= 1.135:
            logger.debug("GCCXML version - 0.9 ( %s )", xml_output_version)
            xml_generator = self.__gccxml_09
        else:
            # CastXML starts with revision 1.136, but still writes the GCCXML
            # tag and the 0.9 version number in the XML files for backward
            # compatibility.
            logger.debug("CASTXML version - None ( %s )", xml_output_version)
            xml_generator = self.__castxml

        self._xml_generator_version = xml_generator
        self._xml_output_version = xml_output_version
        self._is_gccxml = "GCC-XML" in xml_generator
        self._is_castxml = "CastXML" in xml_generator

    def get_string_repr(self):
        return self._xml_generator_version + \
               self.__separator + \
               str(self._xml_output_version)

    @property
    def is_gccxml(self):
        return self._is_gccxml

    @property
    def is_castxml(self):
        return self._is_castxml

    @property
    def is_gccxml_06(self):
        print("here", self._xml_generator_version)
        return self._xml_generator_version == self.__gccxml_06

    @property
    def is_gccxml_07(self):
        return self._xml_generator_version == self.__gccxml_07

    @property
    def is_gccxml_09(self):
        return self._xml_generator_version == self.__gccxml_09

    @property
    def is_gccxml_09_buggy(self):
        return self._xml_generator_version == self.__gccxml_09_buggy

    @property
    def xml_output_version(self):
        return self._xml_output_version
