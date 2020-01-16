#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PySide2.QtGui import QIcon, QFont
from PySide2.QtWidgets import QMainWindow, QApplication, QToolTip, QMessageBox


class MyWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.initUI()

    def initUI(self):
        self.resize(800, 600)
        self.center()
        self.setWindowTitle('myapp')
        self.setWindowIcon(QIcon('icons/myapp.ico'))
        self.setToolTip('看什么看^_^')
        QToolTip.setFont(QFont('微软雅黑', 12))

        # 菜单栏
        menu_control = self.menuBar().addMenu('Contorl')
        act_quit = menu_control.addAction('quit')
        act_quit.triggered.connect(self.close)

        menu_help = self.menuBar().addMenu('Help')
        act_about = menu_help.addAction('about...')
        act_about.triggered.connect(self.about)
        act_aboutqt = menu_help.addAction('aboutqt')
        act_aboutqt.triggered.connect(self.aboutqt)

        # 状态栏
        self.statusBar().showMessage('程序已就绪...')
        self.show()

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

    def about(self):
        QMessageBox.about(self, "about this software", "wise system")

    def aboutqt(self):
        QMessageBox.aboutQt(self)

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
    sys.exit(myapp.exec_())
