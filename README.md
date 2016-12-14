# txt2mobi
Convert Chinese-Novel txt book to kindle .mobi file
因为只能用于中文网络小说txt版的转换, 这里就不用英文屁话了

## 前提步骤
1. 下载KindleGen官方转换工具并安装
   因为亚马逊官网在中国区不开放send to kindle服务, 所以KindleGen工具也没有开放, 所以只能前往帮助页下载, 地址如下:
   https://kdp.amazon.com/help?topicId=A3IWA2TQYMZ5J6

2. 添加PATH
   如果是Linux或者MacOS的系统, 可以将KindleGen的可执行命令加入的PATH, 这样可以不用每次都配置了

## 安装txt2mobi

    pip install txt2mobi

## 使用方法

### 1. 创建项目目录并进入之
 
    mkdir 校花的贴身高手
    cd ./校花的贴身高手
   
### 2. 下载小说.txt文件到项目目录中

### 3. 初始化项目

    txt2mobi init

   这个时候项目目录里会多一个 .project.ini 的配置文件, 和一个默认的封面图片

### 4. 修改配置:

    [txt2mobi]
    kindlegen=kindlegen

    [book]
    cover-img=cover.png
    title=校花的贴身高手
    author=鱼人二代
    
   [book]节点的不必说了大家都懂, kindlegen这项是KindleGen的命令路径, 比如在windows下我估摸着应该是
   
    kindlegen=c:/KindleGen/kindlegen.exe 
   
   没有windows的机器来测试, 但是在Mac下如果完成了前提步骤的话, 这里可以不用管
   
### 5. 测试和执行

   如果一切无问题, 可以先测试一次, 测试命令会生成转换的中间文件, 但是不会调用KindleGen生成mobi文件, 用于检测生成是否有问题
   
   
    txt2mobi test
   
   
   生成的数据文件是 book.html 你可以用浏览器打开检测标题什么的是否分割正常, 如果有问题, 比如出现了无法识别的标题, 你可以
   
     1. fork本项目, 修改 txt2html.py 的74行,方法__is_chapter_title的代码, 如果能在给我发一个pullrequest, 那将是极好的
     2. 在issuse里发, 并附上小说txt(或者截取几个章节的内容, 但是最好是原始文件), 我会想办法增加这类文件的支持
   
   这个项目暂时只支持utf8和gbk(gb2312)编码的文件, 可以自动识别毋须手动转换, 但是如果是其他无法支持的编码, 也请参照上面的方法
   
   如果生成的html和章节索引(ncx文件)没有问题的话, 就可以执行生成命令了
   
    txt2mobi gen
   
   生成完成后会在项目目录里生成  书名.mobi 文件, 就是转换好的结果了

### 6. 发送到Kindle

   有两个办法.
   
   1.通过 邮件发送给 Kindle的邮箱, 然后Amazon会帮你push给你的Kindle, 详情可以参见: https://www.amazon.cn/gp/help/customer/display.html?nodeId=201974220
   2.在项目目录执行
   
    txt2mobi trans
    
   然后在Kindle上打开浏览器, 输入 http://电脑的ip:8000 点击project.mobi 就可以下载生成好的书到Kindle了
 
 祝 玩得开心
   
   
