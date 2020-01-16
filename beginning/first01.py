#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PySide2.QtWidgets import QApplication, QWidget


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 800, 600)
        # 坐标0 0 大小800 600
        self.setWindowTitle('myapp')


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    mywidget = MyWidget()
    mywidget.show()
    sys.exit(myapp.exec_())
