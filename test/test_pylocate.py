import os
import unittest
import pylocate

try:
    from unittest import mock
except ImportError:
    # Python 2
    import mock

here = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(here, "data")

class TestLocate(unittest.TestCase):
    """General tests and assumptions about pylocate
    """

    def test_finds_py_files(self):
        """This tests that locate can find files in
        the ``./test/data`` directory using a glob pattern.
        """
        results = sorted(list(pylocate.locate(data_dir, patterns=("*.py", ))))
        expected = sorted([
            os.path.join(data_dir, "1", "script-2.py"),
            os.path.join(data_dir, "1", "2", "script.py"),
        ])
        self.assertEqual(expected, results)

    def test_accepts_a_str_as_single_pattern(self):
        results = sorted(list(pylocate.locate(data_dir, patterns=("*.py"))))
        expected = sorted([
            os.path.join(data_dir, "1", "script-2.py"),
            os.path.join(data_dir, "1", "2", "script.py"),
        ])
        self.assertEqual(expected, results)
    
    def test_matches_multiple_patterns_properly(self):
        results = sorted(list(pylocate.locate(data_dir, patterns=("*.py", "*.txt"))))
        expected = sorted([
            os.path.join(data_dir, "this.txt"),
            os.path.join(data_dir, "1", "script-2.py"),
            os.path.join(data_dir, "1", "that.txt"),
            os.path.join(data_dir, "1", "2", "script.py"),
            os.path.join(data_dir, "1", "2", "the-other.txt"),
        ])
        self.assertEqual(expected, results)

    def test_looks_in_zip_files(self):
        results = sorted(list(pylocate.locate(data_dir, patterns=("*.bat"), examine_zips=True)))
        expected = sorted([
            os.path.join(data_dir, "1", "2", "3.zip", "3", "4", "in-zip-2.bat"),
            os.path.join(data_dir, "1", "2", "3.zip", "3", "in-zip.bat"),
        ])
        self.assertEqual(expected, results)

    def test_matches_multiple_patterns_properly_within_zip(self):
        results = sorted(list(pylocate.locate(data_dir, patterns=("*.bat", "*.sh"), examine_zips=True)))
        expected = sorted([
            os.path.join(data_dir, "1", "2", "3.zip", "3", "4", "in-zip-2.bat"),
            os.path.join(data_dir, "1", "2", "3.zip", "3", "4", "test.sh"),
            os.path.join(data_dir, "1", "2", "3.zip", "3", "in-zip.bat"),
        ])
        self.assertEqual(expected, results)

    def test_matches_on_partial_pathname(self):
        results = sorted(list(pylocate.locate(data_dir, patterns=("*1/2/*.py", ))))
        expected = sorted([
            os.path.join(data_dir, "1", "2", "script.py"),
        ])
        self.assertEqual(expected, results)

    def test_accepts_test_parameter(self):
        results = sorted(list(pylocate.locate(data_dir, patterns=("*.txt", "*that*"), matchall=True)))
        expected = sorted([
            os.path.join(data_dir, "1", "that.txt"),
        ])
        self.assertEqual(expected, results)

    def test_accepts_regex_instead_of_glob(self):
        results = sorted(list(pylocate.locate(data_dir, patterns=(r".*1.*2.*script\.py", ), regex=True)))
        expected = sorted([
            os.path.join(data_dir, "1", "2", "script.py"),
        ])
        self.assertEqual(expected, results)

    def test_allows_multiple_directories(self):
        directories = (
            data_dir,
            os.path.join(data_dir, "1", "2"),
        )
        results = sorted(list(pylocate.locate(directories, patterns=("*.py"))))
        expected = sorted([
            os.path.join(data_dir, "1", "script-2.py"),
            os.path.join(data_dir, "1", "2", "script.py"),
            os.path.join(data_dir, "1", "2", "script.py"),
        ])
        self.assertEqual(expected, results)

class TestCLI(unittest.TestCase):

    @mock.patch("pylocate.pylocate.locate")
    def test_accepts_directories(self, mock_locate):
        pylocate.main(argv=("-d", data_dir, "-p", "*.py"))
        mock_locate.assert_called_with(directories=[data_dir],
                                       patterns=["*.py"],
                                       matchall=False,
                                       regex=False,
                                       examine_zips=False)
    
    @mock.patch("pylocate.pylocate.locate")
    def test_accepts_no_params(self, mock_locate):
        pylocate.main(argv=[])
        mock_locate.assert_called_with(matchall=False, regex=False, examine_zips=False)

    @mock.patch("pylocate.pylocate.locate")
    def test_accepts_matchall(self, mock_locate):
        pylocate.main(argv=["--matchall"])
        mock_locate.assert_called_with(matchall=True, regex=False, examine_zips=False)

    @mock.patch("pylocate.pylocate.locate")
    def test_accepts_regex(self, mock_locate):
        pylocate.main(argv=["--regex"])
        mock_locate.assert_called_with(matchall=False, regex=True, examine_zips=False)

    @mock.patch("pylocate.pylocate.locate")
    def test_accepts_examine_zips(self, mock_locate):
        pylocate.main(argv=["--examine-zips"])
        mock_locate.assert_called_with(matchall=False, regex=False, examine_zips=True)

