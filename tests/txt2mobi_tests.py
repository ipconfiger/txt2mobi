# coding=utf8

import os
import sys
import unittest
sys.path.append('..')

class TestTxt2MobiFunction(unittest.TestCase):
    def setUp(self):
        pass

    def test_00_init_project(self):
        from txt2mobi import utilities
        utilities.init_project()
        file_path = os.path.join(utilities.current_working_dir(), '.project.ini')
        project_file_exists = os.path.isfile(file_path)
        self.assertEqual(project_file_exists, True)
        with open(file_path, 'r') as f:
            lines = f.readlines()
        self.assertEquals(len(lines), 7)
        self.assertEquals(lines[0].strip(), '[txt2mobi]')
        self.assertEquals(lines[1].strip(), 'kindlegen=kindlegen')
        self.assertEquals(lines[2].strip(), '')
        self.assertEquals(lines[3].strip(), '[book]')
        self.assertEquals(lines[4].strip(), 'cover-img=cover.png')
        self.assertEquals(lines[5].strip(), u'title=书名'.encode('utf8'))
        self.assertEquals(lines[6].strip(), u"author=作者".encode('utf8'))
        os.remove(file_path)


if __name__ == '__main__':
    unittest.main()
