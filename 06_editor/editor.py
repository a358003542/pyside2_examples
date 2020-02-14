#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PySide2.QtCore import QCoreApplication, QMetaObject, QPoint, \
    QRect, QSize, Qt, Slot, QTranslator, QLocale, \
    QSettings, QFile, QIODevice, QTextStream, QFileInfo
from PySide2.QtGui import QIcon, QFont, QKeySequence
from PySide2.QtWidgets import QWidget, QMainWindow, QApplication, QMessageBox, \
    QMenu, QAction, QFileDialog, QTextEdit, QMenuBar, QStatusBar, QToolBar

VERSION = '1.0.0'

import editor_rc


class Editor(QMainWindow):
    def __init__(self, app=None):
        super().__init__()
        self.app = app
        self.lang = QLocale.system().name()

        self.curFile = ''

        self.setupUi()

        self.action_New.triggered.connect(self.newFile)
        self.action_Open.triggered.connect(self.open)
        self.action_Save.triggered.connect(self.save)
        self.action_SaveAs.triggered.connect(self.saveAs)
        self.action_Quit.triggered.connect(self.close)

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.action_Cut.triggered.connect(self.textEdit.cut)
        self.action_Copy.triggered.connect(self.textEdit.copy)
        self.action_Paste.triggered.connect(self.textEdit.paste)

        self.action_About.triggered.connect(self.about)
        self.action_AboutQt.triggered.connect(
            QApplication.instance().aboutQt)

        self.action_Cut.setEnabled(False)
        self.action_Copy.setEnabled(False)
        self.textEdit.copyAvailable.connect(self.action_Cut.setEnabled)
        self.textEdit.copyAvailable.connect(self.action_Copy.setEnabled)

        self.statusBar().showMessage(self.tr("Ready"))

        # self.readSettings()

        # self.textEdit.textChanged.connect(self.setWindowModified)

        # self.setCurrentFile('')

    @Slot()
    def closeEvent(self, event):
        if self.maybeSave():
            self.writeSettings()
            event.accept()
        else:
            event.ignore()

    @Slot()
    def newFile(self):
        print('hello')
        if self.maybeSave():
            self.textEdit.clear()
            self.setCurrentFile('')

    @Slot()
    def open(self):
        if self.maybeSave():
            fileName, _ = QFileDialog.getOpenFileName(self)
            if fileName:
                self.loadFile(fileName)

    @Slot()
    def save(self):
        if self.curFile:
            return self.saveFile(self.curFile)

        return self.saveAs()

    @Slot()
    def saveAs(self):
        fileName, _ = QFileDialog.getSaveFileName(self)
        if fileName:
            return self.saveFile(fileName)

        return False

    @Slot()
    def about(self):
        QMessageBox.about(self, self.tr("About Application"),
                          self.tr(
                              "The <b>Application</b> example demonstrates how to write "
                              "modern GUI applications using Qt, with a menu bar, "
                              "toolbars, and a status bar."))

    def readSettings(self):
        settings = QSettings("Trolltech", "Application Example")
        pos = settings.value("pos", QPoint(200, 200))
        size = settings.value("size", QSize(400, 400))
        self.resize(size)
        self.move(pos)

    def writeSettings(self):
        settings = QSettings("Trolltech", "Application Example")
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())

    def maybeSave(self):
        if self.textEdit.document().isModified():
            ret = QMessageBox.warning(self, self.tr("Application"),
                                      self.tr('''The document has been modified.
                    Do you want to save your changes?'''),
                                      QMessageBox.Save | QMessageBox.Discard
                                      | QMessageBox.Cancel)

            if ret == QMessageBox.Save:
                return self.save()

            if ret == QMessageBox.Cancel:
                return False

        return True

    def loadFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QIODevice.ReadOnly | QIODevice.Text):
            QMessageBox.warning(self, self.tr("Application"),
                                self.tr("Cannot read file %s:\n%s." % (
                                    fileName, file.errorString())))
            return

        inf = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.textEdit.setPlainText(inf.readAll())
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File loaded", 2000)

    def saveFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QIODevice.WriteOnly | QIODevice.Text):
            QMessageBox.warning(self, "Application",
                                "Cannot write file %s:\n%s." % (
                                    fileName, file.errorString()))
            return False

        outf = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outf << self.textEdit.toPlainText()
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File saved", 2000)
        return True

    def setCurrentFile(self, fileName):
        self.curFile = fileName
        self.textEdit.document().setModified(False)
        if self.curFile:
            shownName = self.strippedName(self.curFile)
        else:
            shownName = 'untitled.txt'
        self.setWindowTitle("%s-Application" % shownName)

    def setWindowModified(self):
        if self.curFile:
            shownName = self.strippedName(self.curFile)
        else:
            shownName = 'untitled.txt'
        self.setWindowTitle("-*-%s-Application" % shownName)

    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()

    def setupUi(self):
        self.resize(1024, 768)
        self.center()
        self.setWindowTitle(self.tr('simple text editor'))
        self.setWindowIcon(QIcon(':/images/editor.ico'))

        self.action_New = QAction(self)
        self.action_New.setText(self.tr("&New"))
        self.action_New.setShortcut(QKeySequence.New)
        self.action_New.setIcon(QIcon(":/images/new.png"))
        self.action_New.setToolTip(self.tr("Create a new file"))
        self.action_New.setStatusTip(self.tr("Create a new file"))

        self.action_Open = QAction(self)
        self.action_Open.setIcon(QIcon(":/images/open.png"))

        self.action_Save = QAction(self)
        self.action_Save.setIcon(QIcon(":/images/save.png"))

        self.action_SaveAs = QAction(self)
        self.action_Quit = QAction(self)
        self.action_Cut = QAction(self)
        self.action_Cut.setIcon(QIcon(":/images/cut.png"))

        self.action_Copy = QAction(self)
        self.action_Copy.setIcon(QIcon(":/images/copy.png"))

        self.action_Paste = QAction(self)
        self.action_Paste.setIcon(QIcon(":/images/paste.png"))

        self.action_About = QAction(self)
        self.action_AboutQt = QAction(self)
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 800, 26))
        self.menu_File = QMenu(self.menubar)
        self.menu_Edit = QMenu(self.menubar)
        self.menu_Help = QMenu(self.menubar)
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolBar)

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

        self.action_Open.setText(self.tr("Open"))
        self.action_Open.setToolTip(self.tr("Open an existing file"))

        self.action_Save.setText(self.tr("Save"))
        self.action_Save.setToolTip(self.tr("Save the document to disk"))

        self.action_SaveAs.setText(self.tr("Save As..."))
        self.action_Quit.setText(self.tr("Quit"))
        self.action_Cut.setText(self.tr("Cut"))
        self.action_Copy.setText(self.tr("Copy"))
        self.action_Paste.setText(self.tr("Paste"))
        self.action_About.setText(self.tr("About"))
        self.action_AboutQt.setText(self.tr("AboutQt"))
        self.menu_File.setTitle(self.tr("File"))
        self.menu_Edit.setTitle(self.tr("Edit"))
        self.menu_Help.setTitle(self.tr("Help"))
        self.toolBar.setWindowTitle(self.tr("toolBar"))

    def center(self):
        screen = self.app.screens()[0]
        screen_size = screen.size()
        size = self.geometry()
        self.move((screen_size.width() - size.width()) / 2, \
                  (screen_size.height() - size.height()) / 2)


def main():
    app = QApplication(sys.argv)
    # 先自动加载最佳语言方案
    default_translator = QTranslator()
    default_translator.load(f':/translations/editor_{QLocale.system().name()}')

    app.installTranslator(default_translator)

    editor = Editor(app)

    editor.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
