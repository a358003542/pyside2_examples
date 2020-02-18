#!/usr/bin/env python
# -*-coding:utf-8-*-

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QSystemTrayIcon, QDialog, QVBoxLayout, QTextEdit, \
    QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None, icon=None):
        super(SystemTrayIcon, self).__init__(parent)
        self.parent = parent

        if icon is not None:
            self.setIcon(QIcon(icon))

        self.activated.connect(self.onTrayIconActivated)

    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.parent.show()


class Loginfo(QDialog):
    def __init__(self, parent=None, log_info=None):
        super().__init__()
        self.parent = parent
        self.setupUi()

        if log_info is None:
            log_info = []

        for log in log_info:
            self.textEdit.append(log)

    def setupUi(self):
        self.resize(500, 500)
        self.verticalLayout = QVBoxLayout()
        self.textEdit = QTextEdit(self)
        self.verticalLayout.addWidget(self.textEdit)

        self.setLayout(self.verticalLayout)

        self.horizontalLayout_2 = QHBoxLayout()

        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding,
                                 QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton = QPushButton(self)
        self.horizontalLayout_2.addWidget(self.pushButton)

        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding,
                                  QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.pushButton.setText(self.tr("Ok"))
        self.pushButton.clicked.connect(self.close)

