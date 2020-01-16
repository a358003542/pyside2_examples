#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QApplication


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle('myapp')
        self.setWindowIcon(QIcon('icons/myapp.ico'))


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    mywidget = MyWidget()
    mywidget.show()
    sys.exit(myapp.exec_())
