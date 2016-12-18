# coding=utf8
__author__ = 'liming'

from setuptools import setup

setup(name='txt2mobi',
      version='0.0.3',
      description='Convert Chinese-Novel txt book to kindle .mobi file',
      url='https://github.com/ipconfiger/txt2mobi',
      author='Alexander.Li',
      author_email='superpowerlee@gmail.com',
      license='GNU GENERAL PUBLIC LICENSE',
      packages=['txt2mobi'],
      install_requires=[
          'chardet',
      ],
      entry_points = {
        'console_scripts': ['txt2mobi=txt2mobi.main:main'],
      },
      zip_safe=False)