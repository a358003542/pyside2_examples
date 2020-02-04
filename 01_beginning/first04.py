#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PySide2.QtGui import QIcon, QFont
from PySide2.QtWidgets import QWidget, QApplication, QToolTip, QMessageBox


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle('myapp')
        self.setWindowIcon(QIcon('icons/myapp.ico'))
        self.setToolTip('看什么看^_^')
        QToolTip.setFont(QFont('微软雅黑', 12))

    def closeEvent(self, event):
        # 重新定义colseEvent
        reply = QMessageBox.question(self, '信息',
                                     "你确定要退出吗？",
                                     QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    mywidget = MyWidget()
    mywidget.show()
    sys.exit(myapp.exec_())
