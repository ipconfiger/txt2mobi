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
    book_count = book.book_count()
    for idx in range(1, book_count + 1):
        os.system(book.gen_command(idx))
        src_path = os.path.join(current_working_dir(), 'project-%s.mobi' % idx)
        des_path = os.path.join(current_working_dir(), '%s-%s.mobi' % (book.name.encode('utf8'), idx))
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
        book.trim()
        break
    # 生成opf文件
    book_count = book.book_count()
    for idx in range(1, book_count+1):
        try:
            opf_path = os.path.join(current_working_dir(), 'project-%s.opf' % idx)
            with open(opf_path, 'w') as f:
                f.write(book.gen_opf_file(idx))
                f.close()
            print "opf文件生成完毕"

            # 生成ncx文件
            ncx_path = os.path.join(current_working_dir(), 'toc-%s.ncx' % idx)
            with open(ncx_path, 'w') as f:
                f.write(book.gen_ncx(idx))
                f.close()
            print "ncx文件生成完毕"

            # 生成book.html
            book_path = os.path.join(current_working_dir(), 'book-%s.html' % idx)
            with open(book_path, 'w') as f:
                f.write(book.gen_html_file(idx))
                f.close()
            print "book-%s.html生成完毕" % idx
        except EncodingError, e:
            print "文件编码异常无法解析,请尝试用iconv来转码成utf8后再试,或者提交issuse"
            sys.exit(1)
    return book



