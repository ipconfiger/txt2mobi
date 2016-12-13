# coding=utf8

import os
import sys
import unittest
import traceback
import shutil
sys.path.append('..')

class TestTxt2MobiFunction(unittest.TestCase):
    def setUp(self):
        pass

    def test_00_init_project(self):
        """
        测试初始化项目目录的功能
        :return:
        :rtype:
        """
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

        cover_file_path = os.path.join(utilities.current_working_dir(), 'cover.png')
        cover_file_exists = os.path.isfile(cover_file_path)
        self.assertEquals(cover_file_exists, True)

    def test_01_check_kindlegen(self):
        """
        测试检测kindlegen是否已经安装的功能,(成功运行测试需要正确安装kindlegen)
        :return:
        :rtype:
        """
        from txt2mobi import utilities
        from txt2mobi.exceptions import KindleGenNotInstalledError
        utilities.check_kindlgen()
        try:
            utilities.check_kindlgen(command='error_command')
            self.assertFalse(True)
        except KindleGenNotInstalledError, e:
            pass

    def test_02_load_project_config(self):
        """
        检测加载项目配置文件
        :return:
        :rtype:
        """
        from txt2mobi.utilities import ProjectConfig
        config = ProjectConfig()
        self.assertEqual(config.gen_command, 'kindlegen')
        self.assertEqual(config.cover_image, 'cover.png')
        self.assertEqual(config.title, u'书名')
        self.assertEqual(config.author, u'作者')


    def test_03_gen(self):
        from txt2mobi.scaffold import generate_project
        dist_path = os.path.join(os.getcwd(), 'book.txt')
        dir_path = os.path.join(os.getcwd(), 'samples')
        onlyfiles = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('txt')]
        for file_path in onlyfiles:
            shutil.copy(file_path, dist_path)
            generate_project()
            break


if __name__ == '__main__':
    unittest.main()
