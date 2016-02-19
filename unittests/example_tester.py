
import os
import fnmatch
import unittest
import subprocess


class tester_t(unittest.TestCase):

    def test_example(self):
        """Runs the example in the docs directory"""

        env = os.environ.copy()

        # Get the path to current directory
        path = os.path.dirname(os.path.realpath(__file__))
        # Set the COVERAGE_PROCESS_START env. variable.
        # Allows to cover files run in a subprocess
        # http://nedbatchelder.com/code/coverage/subprocess.html
        env["COVERAGE_PROCESS_START"] = path + "/../.coveragerc"
        path += "/../docs/examples"

        # Find all the examples files
        file_paths = []
        for root, dirnames, filenames in os.walk(path):
            for file_path in fnmatch.filter(filenames, '*.py'):
                file_paths.append(os.path.join(root, file_path))

        for file_path in file_paths:
            return_code = subprocess.call(["python", file_path], env=env)
            self.assertFalse(
                return_code,
                msg="The example %s did not run correctly" % file_path)


def create_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(tester_t))
    return suite


def run_suite():
    unittest.TextTestRunner(verbosity=2).run(create_suite())

if __name__ == "__main__":
    run_suite()
