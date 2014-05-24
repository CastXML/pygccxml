
import os
import pep8
import unittest


class tester_t(unittest.TestCase):

    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args)

    def test_pep8_conformance(self):
        """Pep8 conformance test

        Runs only on the unittest directory for the moment.
        """

        print("\r\n")

        # Get the path to current directory
        path = os.path.dirname(os.path.realpath(__file__))

        pep8style = pep8.StyleGuide()
        result = pep8style.check_files(paths=[path])

        if result.total_errors != 0:
            self.assertEqual(
                result.total_errors, 0,
                "Found code style errors (and warnings).")


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
