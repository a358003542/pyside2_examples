# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Fri Jul 26 06:49:55 2013
#      by: PySide2 UI code generator 5.0.1-snapshot-2a99e59669ee
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 413)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.vboxlayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.vboxlayout.setContentsMargins(9, 9, 9, 9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")
        self.mainFrame = QtWidgets.QFrame(self.centralwidget)
        self.mainFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mainFrame.setObjectName("mainFrame")
        self.gridlayout = QtWidgets.QGridLayout(self.mainFrame)
        self.gridlayout.setContentsMargins(9, 9, 9, 9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")
        self.agreeCheckBox = QtWidgets.QCheckBox(self.mainFrame)
        self.agreeCheckBox.setObjectName("agreeCheckBox")
        self.gridlayout.addWidget(self.agreeCheckBox, 6, 0, 1, 5)
        self.label = QtWidgets.QLabel(self.mainFrame)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label, 5, 0, 1, 1)
        self.nameLabel = QtWidgets.QLabel(self.mainFrame)
        self.nameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.nameLabel.setObjectName("nameLabel")
        self.gridlayout.addWidget(self.nameLabel, 0, 0, 1, 1)
        self.maleRadioButton = QtWidgets.QRadioButton(self.mainFrame)
        self.maleRadioButton.setObjectName("maleRadioButton")
        self.gridlayout.addWidget(self.maleRadioButton, 1, 1, 1, 1)
        self.passwordLabel = QtWidgets.QLabel(self.mainFrame)
        self.passwordLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.passwordLabel.setObjectName("passwordLabel")
        self.gridlayout.addWidget(self.passwordLabel, 3, 0, 1, 1)
        self.countryCombo = QtWidgets.QComboBox(self.mainFrame)
        self.countryCombo.setObjectName("countryCombo")
        self.countryCombo.addItem("")
        self.countryCombo.addItem("")
        self.countryCombo.addItem("")
        self.countryCombo.addItem("")
        self.countryCombo.addItem("")
        self.countryCombo.addItem("")
        self.countryCombo.addItem("")
        self.gridlayout.addWidget(self.countryCombo, 4, 1, 1, 4)
        self.ageLabel = QtWidgets.QLabel(self.mainFrame)
        self.ageLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ageLabel.setObjectName("ageLabel")
        self.gridlayout.addWidget(self.ageLabel, 2, 0, 1, 1)
        self.countryLabel = QtWidgets.QLabel(self.mainFrame)
        self.countryLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.countryLabel.setObjectName("countryLabel")
        self.gridlayout.addWidget(self.countryLabel, 4, 0, 1, 1)
        self.genderLabel = QtWidgets.QLabel(self.mainFrame)
        self.genderLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.genderLabel.setObjectName("genderLabel")
        self.gridlayout.addWidget(self.genderLabel, 1, 0, 1, 1)
        self.passwordEdit = QtWidgets.QLineEdit(self.mainFrame)
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordEdit.setObjectName("passwordEdit")
        self.gridlayout.addWidget(self.passwordEdit, 3, 1, 1, 4)
        self.femaleRadioButton = QtWidgets.QRadioButton(self.mainFrame)
        self.femaleRadioButton.setObjectName("femaleRadioButton")
        self.gridlayout.addWidget(self.femaleRadioButton, 1, 2, 1, 2)
        self.ageSpinBox = QtWidgets.QSpinBox(self.mainFrame)
        self.ageSpinBox.setMinimum(12)
        self.ageSpinBox.setProperty("value", 22)
        self.ageSpinBox.setObjectName("ageSpinBox")
        self.gridlayout.addWidget(self.ageSpinBox, 2, 1, 1, 2)
        self.nameCombo = QtWidgets.QComboBox(self.mainFrame)
        self.nameCombo.setEditable(True)
        self.nameCombo.setObjectName("nameCombo")
        self.gridlayout.addWidget(self.nameCombo, 0, 1, 1, 4)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 1, 4, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(61, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1, 2, 3, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.mainFrame)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.NoButton|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox, 7, 3, 1, 2)
        self.professionList = QtWidgets.QListWidget(self.mainFrame)
        self.professionList.setObjectName("professionList")
        item = QtWidgets.QListWidgetItem()
        self.professionList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.professionList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.professionList.addItem(item)
        self.gridlayout.addWidget(self.professionList, 5, 1, 1, 4)
        self.vboxlayout.addWidget(self.mainFrame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 29))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.exitAction = QtWidgets.QAction(MainWindow)
        self.exitAction.setObjectName("exitAction")
        self.aboutQtAction = QtWidgets.QAction(MainWindow)
        self.aboutQtAction.setObjectName("aboutQtAction")
        self.editStyleAction = QtWidgets.QAction(MainWindow)
        self.editStyleAction.setObjectName("editStyleAction")
        self.aboutAction = QtWidgets.QAction(MainWindow)
        self.aboutAction.setObjectName("aboutAction")
        self.menu_File.addAction(self.editStyleAction)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.exitAction)
        self.menu_Help.addAction(self.aboutAction)
        self.menu_Help.addAction(self.aboutQtAction)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.label.setBuddy(self.professionList)
        self.nameLabel.setBuddy(self.nameCombo)
        self.passwordLabel.setBuddy(self.passwordEdit)
        self.ageLabel.setBuddy(self.ageSpinBox)
        self.countryLabel.setBuddy(self.countryCombo)

        self.retranslateUi(MainWindow)
        self.countryCombo.setCurrentIndex(6)
        self.professionList.setCurrentRow(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Style Sheet"))
        self.agreeCheckBox.setToolTip(_translate("MainWindow", "Please read the LICENSE file before checking"))
        self.agreeCheckBox.setText(_translate("MainWindow", "I accept the terms and &conditions"))
        self.label.setText(_translate("MainWindow", "Profession:"))
        self.nameLabel.setText(_translate("MainWindow", "&Name:"))
        self.maleRadioButton.setToolTip(_translate("MainWindow", "Check this if you are male"))
        self.maleRadioButton.setText(_translate("MainWindow", "&Male"))
        self.passwordLabel.setText(_translate("MainWindow", "&Password:"))
        self.countryCombo.setToolTip(_translate("MainWindow", "Specify country of origin"))
        self.countryCombo.setStatusTip(_translate("MainWindow", "Specify country of origin"))
        self.countryCombo.setItemText(0, _translate("MainWindow", "Egypt"))
        self.countryCombo.setItemText(1, _translate("MainWindow", "France"))
        self.countryCombo.setItemText(2, _translate("MainWindow", "Germany"))
        self.countryCombo.setItemText(3, _translate("MainWindow", "India"))
        self.countryCombo.setItemText(4, _translate("MainWindow", "Italy"))
        self.countryCombo.setItemText(5, _translate("MainWindow", "Norway"))
        self.countryCombo.setItemText(6, _translate("MainWindow", "Pakistan"))
        self.ageLabel.setText(_translate("MainWindow", "&Age:"))
        self.countryLabel.setText(_translate("MainWindow", "Country:"))
        self.genderLabel.setText(_translate("MainWindow", "Gender:"))
        self.passwordEdit.setToolTip(_translate("MainWindow", "Specify your password"))
        self.passwordEdit.setStatusTip(_translate("MainWindow", "Specify your password"))
        self.passwordEdit.setText(_translate("MainWindow", "Password"))
        self.femaleRadioButton.setToolTip(_translate("MainWindow", "Check this if you are female"))
        self.femaleRadioButton.setText(_translate("MainWindow", "&Female"))
        self.ageSpinBox.setToolTip(_translate("MainWindow", "Specify your age"))
        self.ageSpinBox.setStatusTip(_translate("MainWindow", "Specify your age"))
        self.nameCombo.setToolTip(_translate("MainWindow", "Specify your name"))
        self.professionList.setToolTip(_translate("MainWindow", "Select your profession"))
        self.professionList.setStatusTip(_translate("MainWindow", "Specify your name here"))
        self.professionList.setWhatsThis(_translate("MainWindow", "Specify your name here"))
        __sortingEnabled = self.professionList.isSortingEnabled()
        self.professionList.setSortingEnabled(False)
        item = self.professionList.item(0)
        item.setText(_translate("MainWindow", "Developer"))
        item = self.professionList.item(1)
        item.setText(_translate("MainWindow", "Student"))
        item = self.professionList.item(2)
        item.setText(_translate("MainWindow", "Fisherman"))
        self.professionList.setSortingEnabled(__sortingEnabled)
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.exitAction.setText(_translate("MainWindow", "&Exit"))
        self.aboutQtAction.setText(_translate("MainWindow", "About Qt"))
        self.editStyleAction.setText(_translate("MainWindow", "Edit &Style..."))
        self.aboutAction.setText(_translate("MainWindow", "About"))

