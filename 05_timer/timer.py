#!/usr/bin/env python3

import os
import time
import sys

from PySide2.QtGui import QIcon, QFont
from PySide2.QtWidgets import QVBoxLayout, QPushButton, QWidget, \
    QLCDNumber, QMainWindow, QApplication, QMessageBox, \
    QSystemTrayIcon, QMenu, QHBoxLayout, QComboBox
from PySide2.QtCore import QTimer, Slot, Signal, QTranslator, QThread, QLocale

import timer_rc

VERSION = '1.1.1'


class MyWidget(QWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__()
        self.parent = parent

        self.countdown_edit_font = QFont('微软雅黑', 15)

        self.initUI()

        self.buttonStart.clicked.connect(self.parent.timerUp.start)
        self.buttonPause.clicked.connect(self.parent.timerUp.stop)
        self.buttonReset.clicked.connect(self.parent.reset)
        self.buttonCountDown.clicked.connect(self.parent.timerDown.start)
        self.buttonCountDownPause.clicked.connect(self.parent.timerDown.stop)

        self.countdown_edit_hour.currentIndexChanged.connect(
            self.countdown_edit_changed)
        self.countdown_edit_minute.currentIndexChanged.connect(
            self.countdown_edit_changed)
        self.countdown_edit_second.currentIndexChanged.connect(
            self.countdown_edit_changed)

    @Slot()
    def countdown_edit_changed(self, index):
        hour = self.countdown_edit_hour.currentIndex()
        minute = self.countdown_edit_minute.currentIndex()
        second = self.countdown_edit_second.currentIndex()

        time_sec = hour * 60 * 60 + minute * 60 + second

        self.parent.settimer(time_sec)

    def reset_countdown_edit(self):
        self.countdown_edit_hour.setCurrentIndex(0)
        self.countdown_edit_minute.setCurrentIndex(0)
        self.countdown_edit_second.setCurrentIndex(0)

    def initUI(self):
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        self.timeViewer = QLCDNumber()
        self.timeViewer.setFixedHeight(45)
        self.timeViewer.setDigitCount(8)  # 00:00:00
        mainLayout.addWidget(self.timeViewer)

        self.buttonStart = QPushButton(self.tr("start"))
        self.buttonStart.setMinimumHeight(35)
        mainLayout.addWidget(self.buttonStart)

        self.buttonPause = QPushButton(self.tr("pause"))
        self.buttonPause.setMinimumHeight(35)
        mainLayout.addWidget(self.buttonPause)

        self.buttonReset = QPushButton(self.tr("reset"))
        self.buttonReset.setMinimumHeight(35)
        mainLayout.addWidget(self.buttonReset)

        mainLayout.addSpacing(10)

        countdown_edit_hlayout = QHBoxLayout()
        self.countdown_edit_hour = QComboBox()
        self.countdown_edit_hour.setMinimumHeight(35)
        self.countdown_edit_hour.setFont(self.countdown_edit_font)
        self.countdown_edit_hour.addItems([f'{i}' for i in range(0, 24)])

        self.countdown_edit_minute = QComboBox()
        self.countdown_edit_minute.setMinimumHeight(35)
        self.countdown_edit_minute.setFont(self.countdown_edit_font)
        self.countdown_edit_minute.addItems([f'{i}' for i in range(0, 60)])

        self.countdown_edit_second = QComboBox()
        self.countdown_edit_second.setMinimumHeight(35)
        self.countdown_edit_second.setFont(self.countdown_edit_font)
        self.countdown_edit_second.addItems([f'{i}' for i in range(0, 60)])

        countdown_edit_hlayout.addWidget(self.countdown_edit_hour)

        countdown_edit_hlayout.addWidget(self.countdown_edit_minute)

        countdown_edit_hlayout.addWidget(self.countdown_edit_second)

        mainLayout.addLayout(countdown_edit_hlayout)

        self.buttonCountDown = QPushButton(self.tr("countdown"))
        self.buttonCountDown.setMinimumHeight(35)
        self.buttonCountDownPause = QPushButton(self.tr("countdown pause"))
        self.buttonCountDownPause.setMinimumHeight(35)

        mainLayout.addWidget(self.buttonCountDownPause)
        mainLayout.addWidget(self.buttonCountDown)


class MySystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super(MySystemTrayIcon, self).__init__(parent)
        self.parent = parent
        self.setIcon(QIcon(':/images/myapp.png'))
        self.activated.connect(self.onTrayIconActivated)

    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.parent.reopen()


class MakeSoundThread(QThread):
    def run(self):
        while True:
            gfun_beep(500, 3)

            self.sleep(10)

            if self.isInterruptionRequested():
                return


class Timer(QMainWindow):
    timeout = Signal()

    def __init__(self, app=None):
        super().__init__()
        self.app = app
        self.lang = QLocale.system().name()

        self.sound_thread = None

        self.time = 0
        self.timeInterval = 1000  # 默认秒

        self.timerUp = QTimer()
        self.timerUp.setInterval(self.timeInterval)
        self.timerUp.timeout.connect(self.updateUptime)

        self.timerDown = QTimer()
        self.timerDown.setInterval(self.timeInterval)
        self.timerDown.timeout.connect(self.updateDowntime)

        self.initUi()

        self.timeout.connect(self.beep)

    def initUi(self):
        self.setFixedSize(300, 400)
        self.center()
        self.setWindowTitle('timer')
        self.setWindowIcon(QIcon(':/images/myapp.png'))

        menu_control = self.menuBar().addMenu(self.tr('Contorl'))
        act_quit = menu_control.addAction(self.tr('quit'))
        act_quit.triggered.connect(self.menu_exit)

        menu_language = self.menuBar().addMenu(self.tr('Language'))
        act_chinese = menu_language.addAction('中文')
        act_chinese.triggered.connect(self.change_lang_chinese)
        act_english = menu_language.addAction('english')
        act_english.triggered.connect(self.change_lang_english)

        menu_help = self.menuBar().addMenu(self.tr('Help'))
        act_about = menu_help.addAction(self.tr('about...'))
        act_about.triggered.connect(self.about)
        act_aboutqt = menu_help.addAction('aboutqt')
        act_aboutqt.triggered.connect(self.aboutqt)

        # 绘制点什么
        self.mywidget = MyWidget(self)
        self.setCentralWidget(self.mywidget)

        self.mysystemTrayIcon = MySystemTrayIcon(self)
        menu1 = QMenu(self)
        menu_systemTrayIcon_open = menu1.addAction(self.tr('open'))
        menu_systemTrayIcon_open.triggered.connect(self.reopen)
        menu1.addSeparator()
        menu_systemTrayIcon_exit = menu1.addAction(self.tr("exit"))
        menu_systemTrayIcon_exit.triggered.connect(self.menu_exit)
        self.mysystemTrayIcon.setContextMenu(menu1)
        self.mysystemTrayIcon.show()

        # 状态栏
        self.statusBar().showMessage(self.tr('program is ready...'))
        self.statusBar().setSizeGripEnabled(False)

        self.show()

    def menu_exit(self):
        reply = QMessageBox.question(self, '信息',
                                     self.tr('are you sure to quit?'),
                                     QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.app.exit()
        else:
            # 如果主窗口不显示qt事件循环会终止
            self.showMinimized()

    def reopen(self):
        self.show()

    def updateUptime(self):
        self.time += 1
        self.settimer(self.time)

    def updateDowntime(self):
        self.time = self.time - 1
        self.settimer(self.time)
        if self.time <= 0:
            self.timeout.emit()

    def retranslateUi(self):
        self.mywidget.buttonStart.setText(self.tr("start"))
        self.mywidget.buttonPause.setText(self.tr("pause"))
        self.mywidget.buttonReset.setText(self.tr("reset"))
        self.mywidget.buttonCountDown.setText(self.tr("countdown"))
        self.mywidget.buttonCountDownPause.setText(self.tr('countdown pause'))

    def change_lang_chinese(self):
        self.app.removeTranslator(default_translator)
        translator = QTranslator()
        translator.load(':/translations/timer_zh_CN')
        self.app.installTranslator(translator)
        self.retranslateUi()
        self.lang = 'zh_CN'

    def change_lang_english(self):
        self.app.removeTranslator(default_translator)
        translator = QTranslator()
        translator.load('')
        self.app.installTranslator(translator)
        self.retranslateUi()
        self.lang = 'en'

    def settimer(self, time_sec):
        self.time = time_sec
        time_data = time.gmtime(self.time)
        hour = time_data.tm_hour
        minute = time_data.tm_min
        second = time_data.tm_sec

        text_time = f'{hour:0>2}:{minute:0>2}:{second:0>2}'
        self.mywidget.timeViewer.display(text_time)

    @Slot()
    def beep(self):
        self.timerDown.stop()
        # make a sound
        self.sound_thread = MakeSoundThread(self)
        self.sound_thread.start()

    def reset(self):
        self.time = 0
        self.settimer(self.time)
        self.mywidget.reset_countdown_edit()

        self.timerUp.stop()
        self.timerDown.stop()
        if self.sound_thread:
            self.sound_thread.requestInterruption()

    def closeEvent(self, event):
        if self.mysystemTrayIcon.isVisible():
            QMessageBox.information(self, '信息', self.tr(
                'program is still running background.'))
            self.hide()
            event.ignore()

    def about(self):
        QMessageBox.about(self, self.tr("about this software"), f"""
        a simple timer program {VERSION}
        start 启动
        pause 暂停
        reset 重设计数为0或者停止报警
        countdown 倒计时
        countdown pause 倒计时暂停""")

    def aboutqt(self):
        QMessageBox.aboutQt(self)

    # center method
    def center(self):
        screen = self.app.screens()[0]
        screen_size = screen.size()
        size = self.geometry()
        self.move((screen_size.width() - size.width()) / 2, \
                  (screen_size.height() - size.height()) / 2)


def gfun_beep(a, b):
    """make a sound , ref:\
     http://stackoverflow.com/questions/16573051/python-sound-alarm-when-code-finishes
    you need install  ``apt-get install sox``

    :param a: frenquency
    :param b: duration

    create a background thread,so this function does not block the main program
    """
    if sys.platform == "win32":
        import winsound

        def _beep(a, b):
            winsound.Beep(a, b * 1000)
    elif sys.platform == 'linux':
        def _beep(a, b):
            os.system(
                'play --no-show-progress --null \
                --channels 1 synth {0} sine {1}'.format(b, float(a)))
    from threading import Thread
    thread = Thread(target=_beep, args=(a, b))
    thread.daemon = True
    thread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 先自动加载最佳语言方案
    default_translator = QTranslator()
    default_translator.load(f':/translations/timer_{QLocale.system().name()}')
    app.installTranslator(default_translator)

    timer = Timer(app)

    timer.show()
    sys.exit(app.exec_())
