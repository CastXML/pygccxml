
import os
import unittest
import subprocess


class tester_t(unittest.TestCase):

    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args)

    def test_example(self):
        """Runs the example in the docs directory"""

        env = os.environ.copy()

        # Get the path to current directory
        path = os.path.dirname(os.path.realpath(__file__))
        # Set the COVERAGE_PROCESS_START env. variable.
        # Allows to cover files run in a subprocess
        # http://nedbatchelder.com/code/coverage/subprocess.html
        env["COVERAGE_PROCESS_START"] = path + "/../.coveragerc"
        path += "/../docs/example/example.py"
        return_code = subprocess.call(["python", path], env=env)
        self.assertFalse(
            return_code,
            msg="The example did not run correctly")


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
