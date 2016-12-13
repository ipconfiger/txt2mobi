# coding=utf8

import os
import sys
import requests
import ConfigParser
from exceptions import KindleGenNotInstalledError


def current_working_dir():
    return os.getcwd()


def init_project():
    rows = []
    rows.append(u'[txt2mobi]')
    rows.append(u'kindlegen=kindlegen')
    rows.append(u'')
    rows.append(u'[book]')
    rows.append(u'cover-img=cover.png')
    rows.append(u'title=书名')
    rows.append(u'author=作者')
    with open(os.path.join(current_working_dir(), '.project.ini'), 'w') as f:
        f.write("\n".join([r.encode('utf8') for r in rows]))
        f.close()
    r = requests.get('https://raw.githubusercontent.com/ipconfiger/txt2mobi/master/resources/cover.png')
    with open(os.path.join(current_working_dir(), 'cover.png'), 'w') as f:
        f.write(r.content)
        f.close()


def check_kindlgen(command='kindlegen'):
    rt = os.system(command)
    if rt:
        raise KindleGenNotInstalledError()

class ProjectConfig(object):
    def __init__(self):
        try:
            file_path = os.path.join(current_working_dir(), '.project.ini')
            self.cf = ConfigParser.ConfigParser()
            self.cf.read(file_path)
        except Exception:
            print "当前目录未初始化"
            sys.exit(1)


    @property
    def gen_command(self):
        return self.cf.get('txt2mobi', 'kindlegen')

    @property
    def cover_image(self):
        return self.cf.get('book', 'cover-img')

    @property
    def title(self):
        return self.cf.get('book', 'title').decode('utf8')

    @property
    def author(self):
        return self.cf.get('book', 'author').decode('utf8')


def codeTrans(code):
    """
    将chardet返回的coding名字转换成系统用的
    :param code:
    :type code:
    :return:
    :rtype:
    """
    codings = {
        'utf-8': 'utf8',
        'GB2312': 'GBK'
    }
    return codings.get(code, 'utf8')
