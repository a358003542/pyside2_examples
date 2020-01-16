#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PySide2.QtGui import QIcon, QFont
from PySide2.QtWidgets import QMainWindow, QApplication, QToolTip, QMessageBox


class MyWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.resize(800, 600)
        self.center()
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

    # center method
    def center(self):
        screen = self.app.screens()[0]
        screen_size = screen.size()
        size = self.geometry()
        self.move((screen_size.width() - size.width()) / 2, \
                  (screen_size.height() - size.height()) / 2)


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    mywindow = MyWindow(myapp)
    mywindow.show()
    mywindow.statusBar().showMessage('程序已就绪...')
    sys.exit(myapp.exec_())
