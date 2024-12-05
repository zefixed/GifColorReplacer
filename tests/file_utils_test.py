import os
import sys
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import file_utils


class TestFileUtils:
    # Make one dir
    def test_make_dir_1(self):
        file_utils.make_dir("test\\test.gif")
        assert os.path.exists("test") is True
        shutil.rmtree("test")

    # Make two dir
    def test_make_dir_2(self):
        file_utils.make_dir("test\\test\\test.gif")
        assert os.path.exists("test\\test") is True
        shutil.rmtree("test")

    # Make two dirs and test exists first
    def test_make_dir_3(self):
        file_utils.make_dir("test\\test\\test.gif")
        file_utils.make_dir("test\\test.gif")
        assert os.path.exists("test") is True
        shutil.rmtree("test")

    # Not make a dir and test it is not exists
    def test_make_dir_4(self):
        assert os.path.exists("test") is False
