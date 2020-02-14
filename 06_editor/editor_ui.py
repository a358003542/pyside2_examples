# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'editor.ui'
##
## Created by: Qt User Interface Compiler version 5.14.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.action_New = QAction(MainWindow)
        self.action_New.setObjectName(u"action_New")
        icon = QIcon()
        icon.addFile(u":/images/new.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_New.setIcon(icon)
        self.action_Open = QAction(MainWindow)
        self.action_Open.setObjectName(u"action_Open")
        icon1 = QIcon()
        icon1.addFile(u":/images/open.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_Open.setIcon(icon1)
        self.action_Save = QAction(MainWindow)
        self.action_Save.setObjectName(u"action_Save")
        icon2 = QIcon()
        icon2.addFile(u":/images/save.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_Save.setIcon(icon2)
        self.action_SaveAs = QAction(MainWindow)
        self.action_SaveAs.setObjectName(u"action_SaveAs")
        self.action_Quit = QAction(MainWindow)
        self.action_Quit.setObjectName(u"action_Quit")
        self.action_Cut = QAction(MainWindow)
        self.action_Cut.setObjectName(u"action_Cut")
        icon3 = QIcon()
        icon3.addFile(u":/images/cut.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_Cut.setIcon(icon3)
        self.action_Copy = QAction(MainWindow)
        self.action_Copy.setObjectName(u"action_Copy")
        icon4 = QIcon()
        icon4.addFile(u":/images/copy.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_Copy.setIcon(icon4)
        self.action_Paste = QAction(MainWindow)
        self.action_Paste.setObjectName(u"action_Paste")
        icon5 = QIcon()
        icon5.addFile(u":/images/paste.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_Paste.setIcon(icon5)
        self.action_About = QAction(MainWindow)
        self.action_About.setObjectName(u"action_About")
        self.action_AboutQt = QAction(MainWindow)
        self.action_AboutQt.setObjectName(u"action_AboutQt")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 26))
        self.menu_File = QMenu(self.menubar)
        self.menu_File.setObjectName(u"menu_File")
        self.menu_Edit = QMenu(self.menubar)
        self.menu_Edit.setObjectName(u"menu_Edit")
        self.menu_Help = QMenu(self.menubar)
        self.menu_Help.setObjectName(u"menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.menu_File.addAction(self.action_New)
        self.menu_File.addAction(self.action_Open)
        self.menu_File.addAction(self.action_Save)
        self.menu_File.addAction(self.action_SaveAs)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Quit)
        self.menu_Edit.addAction(self.action_Cut)
        self.menu_Edit.addAction(self.action_Copy)
        self.menu_Edit.addAction(self.action_Paste)
        self.menu_Help.addAction(self.action_About)
        self.menu_Help.addAction(self.action_AboutQt)
        self.toolBar.addAction(self.action_New)
        self.toolBar.addAction(self.action_Open)
        self.toolBar.addAction(self.action_Save)
        self.toolBar.addAction(self.action_Cut)
        self.toolBar.addAction(self.action_Copy)
        self.toolBar.addAction(self.action_Paste)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_New.setText(QCoreApplication.translate("MainWindow", u"&New", None))
#if QT_CONFIG(tooltip)
        self.action_New.setToolTip(QCoreApplication.translate("MainWindow", u"Create a new file", None))
#endif // QT_CONFIG(tooltip)
        self.action_Open.setText(QCoreApplication.translate("MainWindow", u"&Open", None))
#if QT_CONFIG(tooltip)
        self.action_Open.setToolTip(QCoreApplication.translate("MainWindow", u"Open an existing file", None))
#endif // QT_CONFIG(tooltip)
        self.action_Save.setText(QCoreApplication.translate("MainWindow", u"&Save", None))
#if QT_CONFIG(tooltip)
        self.action_Save.setToolTip(QCoreApplication.translate("MainWindow", u"Save the document to disk", None))
#endif // QT_CONFIG(tooltip)
        self.action_SaveAs.setText(QCoreApplication.translate("MainWindow", u"Save &As...", None))
        self.action_Quit.setText(QCoreApplication.translate("MainWindow", u"&Quit", None))
        self.action_Cut.setText(QCoreApplication.translate("MainWindow", u"Cut", None))
        self.action_Copy.setText(QCoreApplication.translate("MainWindow", u"Copy", None))
        self.action_Paste.setText(QCoreApplication.translate("MainWindow", u"Paste", None))
        self.action_About.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.action_AboutQt.setText(QCoreApplication.translate("MainWindow", u"AboutQt", None))
        self.menu_File.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menu_Edit.setTitle(QCoreApplication.translate("MainWindow", u"&Edit", None))
        self.menu_Help.setTitle(QCoreApplication.translate("MainWindow", u"&Help", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

