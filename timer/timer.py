#!/usr/bin/env python3

import os
import time
import sys

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QVBoxLayout, QPushButton, QSpinBox, QWidget, \
    QLCDNumber, QLabel, QMainWindow, QApplication, QMessageBox, \
    QSystemTrayIcon, QMenu
from PySide2.QtCore import QTimer, Slot, Signal, QTranslator, QThread, QLocale

import timer_rc

# 先自动加载最佳语言方案
default_translator = QTranslator()
default_translator.load(f':translations/timer_{QLocale.system().name()}')


class MyWidget(QWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__()
        self.parent = parent

        self.initUI()

        self.buttonStart.clicked.connect(self.parent.timerUp.start)
        self.buttonPause.clicked.connect(self.parent.timerUp.stop)
        self.buttonReset.clicked.connect(self.parent.reset)
        self.buttonCountDown.clicked.connect(self.parent.timerDown.start)
        self.buttonCountDownPause.clicked.connect(self.parent.timerDown.stop)
        self.timeSpinBox.valueChanged.connect(self.parent.settimer)

    def initUI(self):
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        self.timeViewer = QLCDNumber()
        self.timeViewer.setFixedHeight(45)
        mainLayout.addWidget(self.timeViewer)

        self.timeForHuman = QLabel()
        mainLayout.addWidget(self.timeForHuman)

        self.buttonStart = QPushButton(self.tr("start"))
        mainLayout.addWidget(self.buttonStart)

        self.buttonPause = QPushButton(self.tr("pause"))
        mainLayout.addWidget(self.buttonPause)

        self.buttonReset = QPushButton(self.tr("reset"))
        mainLayout.addWidget(self.buttonReset)

        mainLayout.addSpacing(15)

        self.timeSpinBox = QSpinBox()
        self.timeSpinBox.setRange(0, 10000)
        mainLayout.addWidget(self.timeSpinBox)

        self.buttonCountDown = QPushButton(self.tr("countdown"))
        mainLayout.addWidget(self.buttonCountDown)
        self.buttonCountDownPause = QPushButton(self.tr("countdown pause"))
        mainLayout.addWidget(self.buttonCountDownPause)


class MySystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super(MySystemTrayIcon, self).__init__(parent)
        self.parent = parent
        self.setIcon(QIcon(':images/myapp.png'))
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
        self.lang = ''

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
        self.resize(300, 300)
        self.center()
        self.setWindowTitle('timer')
        self.setWindowIcon(QIcon(':images/myapp.png'))

        menu_control = self.menuBar().addMenu('Contorl')
        act_quit = menu_control.addAction(self.tr('quit'))
        act_quit.triggered.connect(self.menu_exit)

        menu_language = self.menuBar().addMenu('Language')
        act_chinese = menu_language.addAction('chinese')
        act_chinese.triggered.connect(self.change_lang_chinese)
        act_english = menu_language.addAction('english')
        act_english.triggered.connect(self.change_lang_english)

        menu_help = self.menuBar().addMenu('Help')
        act_about = menu_help.addAction('about...')
        act_about.triggered.connect(self.about)
        act_aboutqt = menu_help.addAction('aboutqt')
        act_aboutqt.triggered.connect(self.aboutqt)

        # 绘制点什么
        self.mywidget = MyWidget(self)
        self.setCentralWidget(self.mywidget)

        self.mysystemTrayIcon = MySystemTrayIcon(self)
        menu1 = QMenu(self)
        menu_systemTrayIcon_open = menu1.addAction('open')
        menu_systemTrayIcon_open.triggered.connect(self.reopen)
        menu1.addSeparator()
        menu_systemTrayIcon_exit = menu1.addAction("exit")
        menu_systemTrayIcon_exit.triggered.connect(self.menu_exit)
        self.mysystemTrayIcon.setContextMenu(menu1)
        self.mysystemTrayIcon.show()

        # 状态栏
        self.statusBar().showMessage('程序已就绪...')
        self.show()

    def menu_exit(self):
        reply = QMessageBox.question(self, '信息',
                                     "你确定要退出吗？",
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
        translator.load(':translations/timer_zh_CN')
        self.app.installTranslator(translator)
        self.retranslateUi()
        self.lang = 'zh'

    def change_lang_english(self):
        self.app.removeTranslator(default_translator)
        translator = QTranslator()
        translator.load('')
        self.app.installTranslator(translator)
        self.retranslateUi()
        self.lang = ''

    def settimer(self, time_sec):
        self.time = time_sec
        self.mywidget.timeViewer.display(self.time)

        time_data = time.gmtime(self.time)
        hour = time_data.tm_hour
        minute = time_data.tm_min
        second = time_data.tm_sec
        if self.lang == 'zh':
            text = f'{hour} 小时 {minute} 分 {second} 秒'
        else:
            text = f'{hour} hour {minute} minute {second} second'

        self.mywidget.timeForHuman.setText(text)

    @Slot()
    def beep(self):
        self.timerDown.stop()
        # make a sound
        self.sound_thread = MakeSoundThread(self)
        self.sound_thread.start()

    def closeEvent(self, event):
        if self.mysystemTrayIcon.isVisible():
            QMessageBox.information(self, '信息', '程序还在后台运行')
            self.hide()
            event.ignore()

    def about(self):
        QMessageBox.about(self, "about this software", """
        a simple timer program
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

    def reset(self):
        self.time = 0
        self.settimer(self.time)
        self.mywidget.timeSpinBox.setValue(0)
        self.timerUp.stop()
        self.timerDown.stop()
        if self.sound_thread:
            self.sound_thread.requestInterruption()


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

    app.installTranslator(default_translator)

    timer = Timer(app)

    timer.show()
    sys.exit(app.exec_())
