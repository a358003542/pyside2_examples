#!/usr/bin/env python
# -*-coding:utf-8-*-


import os
import subprocess

if __name__ == '__main__':
    os.chdir('pyqt-official')
    os.chdir('qtdemo')
    subprocess.run('python qtdemo.py')
