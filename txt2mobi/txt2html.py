# coding=utf8

import chardet
from utilities import codeTrans, ProjectConfig
from exceptions import EncodingError


config = ProjectConfig()

def get_coding(file_content):
    result = chardet.detect(file_content)
    if result.get('confidence') > 0.8:
        return result.get('encoding')
    return 'utf-8'


def unicode_line(file_content):
    print "正在识别文件字符集..."
    coding = codeTrans(get_coding(file_content[:500]))
    print "文件字符集:", coding
    lines = file_content.split('\n')
    try:
        return [line.decode(coding) for line in lines]
    except:
        raise EncodingError


class Chapter(object):
    """
    章节对象
    """
    def __init__(self, title, idx):
        self.title = title
        self.lines = []
        self.idx = idx

    def append_line(self, line):
        line = line.replace('\r', '').replace('\n', '')
        self.lines.append(line)

    def as_html(self):
        rows = ["    <h3 id=\"ch%s\">%s</h3>" % (self.idx, self.title.encode('utf8'))]
        for line in self.lines:
            rows.append("    <p>%s</p>" % line.encode('utf8'))
        rows.append("    <mbp:pagebreak />")
        print "章节", self.title, "生成完毕"
        return "\n".join(rows)

    def as_ncx(self):
        ncx = """      <navPoint id="ch%(idx)s" playOrder="%(idx)s">
            <navLabel>
                <text>
                    %(title)s

                </text>
            </navLabel>
            <content src="book.html#ch%(idx)s" />
        </navPoint>""" % dict(idx=self.idx, title=self.title.encode('utf8'))
        print "章节索引", self.title, "生成完毕"
        return ncx


class Book(object):
    """
    书对象
    """
    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            lines = unicode_line(f.read())
            f.close()
        self.chapters = []
        self.process_lines(lines)

    def __is_chapter_title(self, line):
        """
        检测是否章节标题
        :param line:
        :type line:
        :return:
        :rtype:
        """
        if line.startswith(u'第'):
            if 3 < len(line.strip()) < 30 and u"第" in line and u"章" in line:
                return True
        line = line.replace(u"．", u".").replace(u":", u".")
        if line.split('.')[0].isdigit():
            if 3 < len(line.strip()) < 20:
                return True
        return False

    def process_lines(self, lines):
        """
        循环处理所有的行
        :param lines:
        :type lines:
        :return:
        :rtype:
        """
        idx = 1
        chapter = Chapter(u"前言", 0)
        for line in lines:
            if self.__is_chapter_title(line):
                chapter = Chapter(line.strip(), idx)
                self.chapters.append(chapter)
                idx+=1
            else:
                if len(line.strip()):
                    chapter.append_line(line)

    def gen_menu(self):
        """
        生成目录html
        :return:
        :rtype:
        """
        menu_base = """
    <div id="toc">
        <h2>
            目录<br />
        </h2>
        <ul>
%s
        </ul>
    </div>
    <div class="pagebreak"></div>
        """ % "\n".join(["            <li><a href=\"#ch%s\">%s</a></li>" % (chapter.idx, chapter.title.encode('utf8')) for chapter in self.chapters])
        return menu_base

    def gen_html_file(self):
        """
        生成HTML文件
        :return:
        :rtype:
        """
        menu = self.gen_menu()
        book_name = config.title.encode('utf8')
        contents = "\n".join([chapter.as_html() for chapter in self. chapters])

        data = dict(book_name=book_name, menu=menu, content=contents)

        html_base = """<!DOCTYPE html
PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="zh" xml:lang="zh">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>%(book_name)s</title>
    <style type="text/css">
    p { margin-top: 1em; text-indent: 0em; }

    h1 {margin-top: 1em}
    h2 {margin: 2em 0 1em; text-align: center; font-size: 2.5em;}
    h3 {margin: 0 0 2em; font-weight: normal; text-align:center; font-size: 1.5em; font-style: italic;}

    .center { text-align: center; }
    .pagebreak { page-break-before: always; }
    </style>
</head>
<body>
%(menu)s
<!-- Your book goes here -->
%(content)s
</body>
</html>
        """ % data
        return html_base

    def gen_ncx(self):
        """
        生成NCX文件内容
        :return:
        :rtype:
        """
        data = dict(
            book_name=config.title.encode('utf8'),
            menavPoints="\n".join([chapter.as_ncx() for chapter in self.chapters])
        )
        ncx_base = """<?xml version="1.0"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
 <head>
 </head>
        <docTitle>
               <text>%(book_name)s</text>
        </docTitle>
    <navMap>
        %(menavPoints)s
    </navMap>
</ncx>
        """ % data
        return ncx_base

    def gen_opf_file(self):
        """
        生成项目文件
        :return:
        :rtype:
        """
        opf_file = """<?xml version="1.0" encoding="utf-8"?>
<package unique-identifier="uid" xmlns:opf="http://www.idpf.org/2007/opf" xmlns:asd="http://www.idpf.org/asdfaf">
    <metadata>
        <dc-metadata  xmlns:dc="http://purl.org/metadata/dublin_core" xmlns:oebpackage="http://openebook.org/namespaces/oeb-package/1.0/">
            <dc:Title>%(title)s</dc:Title>
            <dc:Language>zh-cn</dc:Language>
            <dc:Creator>%(author)s</dc:Creator>
            <dc:Copyrights>%(author)s</dc:Copyrights>
            <dc:Publisher>Alexander.Li</dc:Publisher>
            <x-metadata>
                <EmbeddedCover>%(cover)s</EmbeddedCover>
            </x-metadata>
        </dc-metadata>
    </metadata>
    <manifest>
        <item id="toc" properties="nav" href="book.html" media-type="application/xhtml+xml"/>
        <item id="content" media-type="application/xhtml+xml" href="book.html"></item>
        <item id="cover-image" media-type="image/png" href="%(cover)s"/>
    </manifest>
    <spine toc="ncx">
        <itemref idref="cover-image"/>
        <itemref idref="toc"/>
        <itemref idref="content"/>
    </spine>
    <guide>
        <reference type="toc" title="%(title_name)s" href="book.html"/>
        <reference type="content" title="Book" href="book.html"/>
    </guide>
</package>
        """ % dict(
            title_name=u"目录".encode('utf8'),
            author=config.author.encode('utf8'),
            title=config.title.encode('utf8'),
            cover=config.cover_image
        )
        return opf_file

    def gen_command(self):
        return "%s project.opf" % config.gen_command.encode('utf')
