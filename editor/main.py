#!/usr/bin/env python3
#-*-coding:utf-8-*-

import sys

#
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QIcon
from PySide2.QtCore import QTranslator,QLocale

from Editor import Editor


#
def main():
    app = QApplication(sys.argv)

    translator = QTranslator()
    if translator.load('editor_'+ QLocale.system().name()+'.qm',":/translations/"):
        app.installTranslator(translator)

    translator_qt = QTranslator()
    if translator_qt.load('qt_'+ QLocale.system().name()+'.qm',":/translations/"):
    #    print('i found qt')
        app.installTranslator(translator_qt)


    mainwindow = Editor()
    mainwindow.setWindowTitle('simple text editor')
    mainwindow.setWindowIcon(QIcon(':/images/editor.ico'))
    mainwindow.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
