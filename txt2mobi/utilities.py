# coding=utf8

import os


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