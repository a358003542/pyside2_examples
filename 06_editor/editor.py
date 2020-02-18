#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PySide2.QtCore import QRect, QSize, Qt, Slot, QTranslator, QLocale, \
    QSettings, QFile, QIODevice, QTextStream, QFileInfo
from PySide2.QtGui import QIcon, QFont, QKeySequence
from PySide2.QtWidgets import QMainWindow, QApplication, QMessageBox, \
    QMenu, QAction, QFileDialog, QTextEdit, QMenuBar, QStatusBar, QToolBar

from my_python_module.pyside2_helper import SystemTrayIcon

VERSION = '1.0.0'
ORGANIZATION_NAME = 'cdwanze'
APPLICATION_NAME = 'editor'

import editor_rc


class TextEdit(QTextEdit):
    """
    自建文本编辑器类 后续应该有更多的定制内容
    """

    def __init__(self, parent=None):
        super(TextEdit, self).__init__()
        self.parent = parent


class Editor(QMainWindow):
    def __init__(self, app=None):
        super().__init__()
        self.app = app
        self.lang = QLocale.system().name()

        self.curFile = ''

        self.setupUi()

        self.set_signal_slot()

        self.statusBar().showMessage(self.tr('program is ready...'))

        self.read_settings()

        self.textEdit.textChanged.connect(self.set_window_title_modified)

        self.setCurrentFile('')

    def set_signal_slot(self):
        self.action_new.triggered.connect(self.newFile)
        self.action_open.triggered.connect(self.open)
        self.action_save.triggered.connect(self.save)
        self.action_saveas.triggered.connect(self.saveAs)
        self.action_quit.triggered.connect(self.menu_exit)

        self.action_cut.triggered.connect(self.textEdit.cut)
        self.action_copy.triggered.connect(self.textEdit.copy)
        self.action_paste.triggered.connect(self.textEdit.paste)

        self.action_about.triggered.connect(self.about)
        self.action_aboutqt.triggered.connect(QApplication.instance().aboutQt)

        self.textEdit.copyAvailable.connect(self.action_cut.setEnabled)
        self.textEdit.copyAvailable.connect(self.action_copy.setEnabled)

    def ask_for_save(self):
        """
        1. save do the save action return saved filename or False
        2. discard do nothing return True
        3. cancel return False all the following process also need to be passed.
        if return True or filename 则表明保存动作pass 可以继续后面的动作
        elif return False 则表明用户放弃了 后续动作也应该一并丢弃
        :return:
        """
        ret = QMessageBox.warning(self, self.tr("Application"),
                                  self.tr(f'The document has been modified.\n'
                                          f'Do you want to save your changes?'),
                                  QMessageBox.Save | QMessageBox.Discard
                                  | QMessageBox.Cancel)
        if ret == QMessageBox.Save:
            return self.save()
        elif ret == QMessageBox.Discard:
            return True
        elif ret == QMessageBox.Cancel:
            return False

    @Slot()
    def newFile(self):
        """
        新建文件动作
        1. return False 新建文件动作放弃
        2. return True 新建文件动作完成
        :return:
        """
        if self.is_need_save():
            save_status = self.ask_for_save()
            if not save_status:
                return False

        self.textEdit.clear()
        self.setCurrentFile('')
        return True

    @Slot()
    def open(self):
        """
        打开文件动作
        :return:
        """
        if self.is_need_save():
            save_status = self.ask_for_save()
            if not save_status:
                return False

        fileName, _ = QFileDialog.getOpenFileName(self)
        if fileName:
            self.loadFile(fileName)
            return fileName
        else:
            return False

    @Slot()
    def save(self):
        """
        保存动作 如果没有当前文件名 则执行另存为动作
        :return:
        """
        if self.curFile:
            return self.save_file(self.curFile)
        else:
            return self.saveAs()

    def save_file(self, filename):
        """
        实际保存文件行为
        保存成功返回实际保存的文件名
        :param filename:
        :return:
        """
        file = QFile(filename)
        if not file.open(QIODevice.WriteOnly | QIODevice.Text):
            QMessageBox.warning(self, "Application",
                                "Cannot write file %s:\n%s." % (
                                    filename, file.errorString()))
            return False

        outf = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outf << self.textEdit.toPlainText()
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(filename)
        self.statusBar().showMessage("File saved", 2000)
        return filename

    @Slot()
    def saveAs(self):
        fileName, _ = QFileDialog.getSaveFileName(self)
        if fileName:
            return self.save_file(fileName)
        else:
            return False

    def read_settings(self):
        settings = QSettings("editor.ini", QSettings.IniFormat)
        size = settings.value("size", QSize(1024, 768))
        self.resize(size)

    def write_settings(self):
        settings = QSettings("editor.ini", QSettings.IniFormat)
        settings.setValue("size", self.size())

    def is_need_save(self):
        if self.textEdit.document().isModified():
            return True
        else:
            return False

    def loadFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QIODevice.ReadOnly | QIODevice.Text):
            QMessageBox.warning(self, self.tr("Application"),
                                self.tr("Cannot read file %s:\n%s." % (
                                    fileName, file.errorString())))
            return False

        inf = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.textEdit.setPlainText(inf.readAll())
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File loaded", 2000)
        return fileName

    def setCurrentFile(self, filename):
        self.curFile = filename
        self.textEdit.document().setModified(False)
        if self.curFile:
            shown_name = Editor.get_stripped_name(self.curFile)
        else:
            shown_name = 'untitled.txt'
        self.setWindowTitle("%s-Application" % shown_name)

    def set_window_title_modified(self):
        if self.curFile:
            shown_name = Editor.get_stripped_name(self.curFile)
        else:
            shown_name = 'untitled.txt'
        self.setWindowTitle("-*-%s-Application" % shown_name)

    @staticmethod
    def get_stripped_name(full_filename):
        return QFileInfo(full_filename).fileName()

    def menu_exit(self):
        """
        实际退出动作
        :return:
        """
        self.write_settings()

        if self.is_need_save():
            save_status = self.ask_for_save()
            if not save_status:
                return False

        reply = QMessageBox.question(self, '信息',
                                     self.tr('are you sure to quit?'),
                                     QMessageBox.Yes,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.app.exit()
        else:
            # 如果主窗口不显示qt事件循环会终止
            self.showMinimized()

    @Slot()
    def about(self):
        QMessageBox.about(self, self.tr("About Application"),
                          self.tr(
                              "The <b>Application</b> example demonstrates "
                              "how to write "
                              "modern GUI applications using Qt, "
                              "with a menu bar, "
                              "toolbars, and a status bar."))

    def set_action_object(self):
        self.action_new = QAction(self)
        self.action_new.setText(self.tr("New"))
        self.action_new.setShortcut(QKeySequence.New)
        self.action_new.setIcon(QIcon(":/images/new.png"))
        self.action_new.setToolTip(self.tr("Create a new file"))
        self.action_new.setStatusTip(self.tr("Create a new file"))

        self.action_open = QAction(self)
        self.action_open.setText(self.tr("Open"))
        self.action_open.setShortcut(QKeySequence.Open)
        self.action_open.setToolTip(self.tr("Open an existing file"))
        self.action_open.setIcon(QIcon(":/images/open.png"))
        self.action_open.setStatusTip(self.tr("Open an existing file"))

        self.action_save = QAction(self)
        self.action_save.setIcon(QIcon(":/images/save.png"))
        self.action_save.setText(self.tr("Save"))
        self.action_save.setShortcut(QKeySequence.Save)
        self.action_save.setToolTip(self.tr("Save the document to disk"))
        self.action_save.setStatusTip(self.tr("Save the document to disk"))

        self.action_saveas = QAction(self)
        self.action_saveas.setText(self.tr("Save As..."))
        self.action_saveas.setShortcut(QKeySequence.SaveAs)

        self.action_quit = QAction(self)
        self.action_quit.setText(self.tr("Quit"))
        self.action_quit.setShortcut(QKeySequence.Quit)

        self.action_cut = QAction(self)
        self.action_cut.setText(self.tr("Cut"))
        self.action_cut.setIcon(QIcon(":/images/cut.png"))
        self.action_cut.setShortcut(QKeySequence.Cut)

        self.action_copy = QAction(self)
        self.action_copy.setText(self.tr("Copy"))
        self.action_copy.setIcon(QIcon(":/images/copy.png"))
        self.action_copy.setShortcut(QKeySequence.Copy)

        self.action_paste = QAction(self)
        self.action_paste.setText(self.tr("Paste"))
        self.action_paste.setIcon(QIcon(":/images/paste.png"))
        self.action_paste.setShortcut(QKeySequence.Paste)

        self.action_about = QAction(self)
        self.action_about.setText(self.tr("About"))

        self.action_aboutqt = QAction(self)
        self.action_aboutqt.setText(self.tr("AboutQt"))

    def setupUi(self):
        self.resize(1024, 768)
        self.center()
        self.setWindowTitle(self.tr('simple text editor'))
        self.setWindowIcon(QIcon(':/images/editor.ico'))

        self.set_action_object()

        self.textEdit = TextEdit()
        self.setCentralWidget(self.textEdit)

        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 800, 26))
        self.menu_file = QMenu(self.menubar)
        self.menu_edit = QMenu(self.menubar)
        self.menu_settings = QMenu(self.menubar)
        self.menu_help = QMenu(self.menubar)
        self.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.toolBar = QToolBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_edit.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.menu_file.addAction(self.action_new)
        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_saveas)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_quit)
        self.menu_edit.addAction(self.action_cut)
        self.menu_edit.addAction(self.action_copy)
        self.menu_edit.addAction(self.action_paste)
        self.menu_help.addAction(self.action_about)
        self.menu_help.addAction(self.action_aboutqt)
        self.toolBar.addAction(self.action_new)
        self.toolBar.addAction(self.action_open)
        self.toolBar.addAction(self.action_save)
        self.toolBar.addAction(self.action_cut)
        self.toolBar.addAction(self.action_copy)
        self.toolBar.addAction(self.action_paste)

        self.menu_file.setTitle(self.tr("File"))
        self.menu_edit.setTitle(self.tr("Edit"))
        self.menu_help.setTitle(self.tr("Help"))
        self.toolBar.setWindowTitle(self.tr("toolBar"))

        self.set_systemtray()

    def set_systemtray(self):
        """
        设置系统托盘
        :return:
        """
        self.mysystemTrayIcon = SystemTrayIcon(self, icon=':/images/editor.ico')
        menu1 = QMenu(self)
        menu_systemTrayIcon_open = menu1.addAction(self.tr('open'))
        menu_systemTrayIcon_open.triggered.connect(self.show)
        menu1.addSeparator()
        menu_systemTrayIcon_exit = menu1.addAction(self.tr("exit"))
        menu_systemTrayIcon_exit.triggered.connect(self.menu_exit)
        self.mysystemTrayIcon.setContextMenu(menu1)
        self.mysystemTrayIcon.show()

    def closeEvent(self, event):
        if self.mysystemTrayIcon.isVisible():
            QMessageBox.information(self, '信息', self.tr(
                'program is still running background.'))
            self.hide()
            event.ignore()

    def center(self):
        screen = self.app.screens()[0]
        screen_size = screen.size()
        size = self.geometry()
        self.move((screen_size.width() - size.width()) / 2, \
                  (screen_size.height() - size.height()) / 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 先自动加载最佳语言方案
    default_translator = QTranslator()
    default_translator.load(f':/translations/editor_{QLocale.system().name()}')
    app.installTranslator(default_translator)

    app.setOrganizationName(ORGANIZATION_NAME)
    app.setApplicationName(APPLICATION_NAME)

    editor = Editor(app)

    editor.show()
    sys.exit(app.exec_())
