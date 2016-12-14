# coding=utf8

import os
import sys
import shutil
from txt2mobi.exceptions import EncodingError
from utilities import current_working_dir, init_project
from txt2html import Book



def op_init_project():
    """
    初始化项目目录
    :return:
    :rtype:
    """
    init_project()


def generate_project():
    """
    生成项目文件
    :return:
    :rtype:
    """
    book = test_project()
    os.system(book.gen_command())
    src_path = os.path.join(current_working_dir(), 'project.mobi')
    des_path = os.path.join(current_working_dir(), '%s.mobi' % book.name.encode('utf8'))
    shutil.move(src_path, des_path)

def test_project():
    """
    测试项目, 跑一遍, 生成文件但是不调用kindlegen
    :return:
    :rtype:
    """
    dir_path = current_working_dir()
    onlyfiles = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith('txt')]
    for file_path in onlyfiles:
        book = Book(file_path)
        break
    # 生成opf文件
    try:
        opf_path = os.path.join(current_working_dir(), 'project.opf')
        with open(opf_path, 'w') as f:
            f.write(book.gen_opf_file())
            f.close()
        print "opf文件生成完毕"

        # 生成ncx文件
        ncx_path = os.path.join(current_working_dir(), 'toc.ncx')
        with open(ncx_path, 'w') as f:
            f.write(book.gen_ncx())
            f.close()
        print "ncx文件生成完毕"

        # 生成book.html
        book_path = os.path.join(current_working_dir(), 'book.html')
        with open(book_path, 'w') as f:
            f.write(book.gen_html_file())
            f.close()
        print "book.html生成完毕"
        return book
    except EncodingError, e:
        print "文件编码异常无法解析,请尝试用iconv来转码成utf8后再试,或者提交issuse"
        sys.exit(1)



