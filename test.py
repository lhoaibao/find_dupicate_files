# ---------------Library import ----------------
import unittest
import find_duplicate_files as fdf
from os import getcwd, stat
from os.path import join


# ---------------Test class---------------------
class test_find_duplicate_files(unittest.TestCase):
    def test_scan_files(self):
        """
        test some testcase of function scan_files
        """
        self.assertFalse(fdf.valid_path('some thing wrong'))
        result = fdf.scan_files(join(getcwd(), 'test'))
        self.assertNotIn(join(getcwd(), 'test/symlink/symlink'), result)

    def test_group_files_by_size(self):
        """
        test some testcase of function group_files_by_size
        """
        file_path_names = fdf.scan_files(join(getcwd(), 'test'))
        result = fdf.group_files_by_size(file_path_names)
        self.assertNotIn(join(getcwd(), 'test/empty'), result)

    def test_group_files_by_checksum(self):
        """
        test some testcase of function group_files_by_checksum
        """
        expect = ["/home/lhoaibao/lhoaibao/test/checksum/a",
                  "/home/lhoaibao/lhoaibao/test/checksum/b"]
        file_path_names = fdf.scan_files(join(getcwd(), 'test/checksum'))
        groups = fdf.group_files_by_size(file_path_names)
        result = fdf.group_files_by_checksum(groups[0])
        self.assertEqual(set(expect), set(result[0]))


if __name__ == '__main__':
    unittest.main()
