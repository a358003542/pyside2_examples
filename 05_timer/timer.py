#!/usr/bin/env python3

import os
import time
import sys
from hashlib import md5
from uuid import uuid1
import json

from PySide2.QtGui import QIcon, QFont
from PySide2.QtWidgets import QVBoxLayout, QPushButton, QWidget, \
    QLCDNumber, QMainWindow, QApplication, QMessageBox, \
    QSystemTrayIcon, QMenu, QHBoxLayout, QComboBox, QDialog, QTextEdit, \
    QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem
from PySide2.QtCore import QTimer, Slot, Signal, QTranslator, QThread, \
    QLocale

import timer_rc

VERSION = '1.2.0'

LOG_INTERVAL = 10  # s
RECORD_SAVE_NUM = 1000  # 保存的运行记录
AUTOSAVE_INTERVAL = 60  # s


def str_md5(key):
    return md5(key.encode()).hexdigest()


def write_json(file, data):
    with open(file, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_json_file(json_filename):
    """
    :return:
    """
    if not os.path.exists(json_filename):
        data = {}
        write_json(json_filename, data)

    return json_filename


def get_json_data(json_filename):
    """
    获取json文件存储的值
    :return:
    """
    with open(get_json_file(json_filename), encoding='utf8') as f:
        res = json.load(f)
        return res


def get_json_value(json_filename, k):
    res = get_json_data(json_filename)
    return res.get(k)


def set_json_value(json_filename, k, v):
    """
    对json文件的某个k设置某个值v
    """
    res = get_json_data(json_filename)
    res[k] = v
    write_json(get_json_file(json_filename), res)


def normal_format_now():
    """
    标准格式 now

    '2018-12-21 15:39:20'
    :return:
    """
    from datetime import datetime
    return datetime.now().__format__('%Y-%m-%d %H:%M:%S')


def random_md5(limit=None):
    """
    输出基于uuid1产生的md5标识
    limit 截取最前面的几个
    """
    key = str(uuid1())
    text = str_md5(key)
    if limit:
        assert isinstance(limit, int)
        assert limit > 0
        return text[:limit]
    else:
        return text


class MyWidget(QWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__()
        self.parent = parent

        self.countdown_edit_font = QFont('微软雅黑', 15)

        self.initUI()

        self.buttonStart.clicked.connect(self.parent.start_count)
        self.buttonPause.clicked.connect(self.parent.timerUp.stop)
        self.buttonReset.clicked.connect(self.parent.reset)
        self.buttonCountDown.clicked.connect(self.parent.start_countdown)
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


class RecordTable(QDialog):
    def __init__(self, running_record, parent=None):
        super().__init__()
        self.setupUi(running_record)

    def setupUi(self, running_record):
        self.resize(670, 670)
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        self.table = QTableWidget(self)
        mainLayout.addWidget(self.table)

        row_count = len(running_record)
        if row_count < 3:
            row_count = 3
        self.table.setRowCount(row_count)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ['task_name', 'start_time', 'last_time', 'end_time', 'status'])

        head_font = QFont('微软雅黑', 11)
        head_font.setBold(True)
        self.table.horizontalHeader().setFont(head_font)
        self.table.setColumnWidth(0, 120)
        self.table.setColumnWidth(1, 160)
        self.table.setColumnWidth(2, 90)
        self.table.setColumnWidth(3, 160)
        self.table.setColumnWidth(4, 90)

        for index, item in enumerate(running_record[::-1]):
            task_name = item.get('task_name', '')
            last_time = item.get('current_time', '')
            status = item.get('status', '')
            start_time = item.get('start_time', '')
            end_time = item.get('end_time', '')

            self.table.setItem(index, 0, QTableWidgetItem(task_name))
            self.table.setItem(index, 1, QTableWidgetItem(start_time))
            self.table.setItem(index, 2, QTableWidgetItem(last_time))
            self.table.setItem(index, 3, QTableWidgetItem(end_time))
            self.table.setItem(index, 4, QTableWidgetItem(status))


class Loginfo(QDialog):
    def __init__(self, running_info, parent=None):
        super().__init__()

        self.setupUi()

        for log in running_info:
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


class Timer(QMainWindow):
    timeout = Signal()

    def __init__(self, app=None):
        super().__init__()
        self.app = app
        self.lang = QLocale.system().name()

        self.sound_thread = None
        self.running_log = []
        self.running_task_info = []  # 更完备的任务信息数据
        self.current_count_task_name = ''
        self.current_countdown_task_name = ''

        self.time = 0
        self.timeInterval = 1000  # = 1s

        self.timerUp = QTimer()
        self.timerUp.setInterval(self.timeInterval)
        self.timerUp.timeout.connect(self.updateUptime)

        self.timerDown = QTimer()
        self.timerDown.setInterval(self.timeInterval)
        self.timerDown.timeout.connect(self.updateDowntime)

        self.timerAutoSave = QTimer()
        self.timerAutoSave.setInterval(AUTOSAVE_INTERVAL * 1000)
        self.timerAutoSave.timeout.connect(self.auto_save_running_log)
        self.timerAutoSave.start()

        self.initUi()

        self.timeout.connect(self.beep)

    def add_log(self, info):
        self.running_log.append(f'{normal_format_now()}: {info}')

    @Slot()
    def auto_save_running_log(self):
        """
        自动保存运行日志
        :return:
        """
        running_record = get_json_value('timer.json', 'running_record')
        if not running_record:
            running_record = []

        all_record = running_record.copy()

        for item_index, item in enumerate(self.running_task_info):
            self.upsert_task_info(item, target=all_record)

        if len(all_record) > RECORD_SAVE_NUM:
            all_record = all_record[-RECORD_SAVE_NUM:]

        set_json_value('timer.json', 'running_record', all_record)

    def upsert_task_info(self, task_info, target=None):
        if target is None:
            target = self.running_task_info
        task_name = task_info['task_name']
        for index, task_info_item in enumerate(target):
            if task_name == task_info_item['task_name']:
                target[index] = {**task_info_item, **task_info}
                break
        else:
            target.append(task_info)

    @Slot()
    def start_count(self):
        if not self.current_count_task_name:
            self.current_count_task_name = f'count_{random_md5(6)}'
            self.add_log(f'start task {self.current_count_task_name}')

            self.upsert_task_info({
                'task_name': self.current_count_task_name,
                'start_time': normal_format_now()
            })

        self.timerUp.start()

    @Slot()
    def start_countdown(self):
        if not self.current_countdown_task_name:
            self.current_countdown_task_name = f'countdown_{random_md5(6)}'

            self.add_log(f'start task {self.current_countdown_task_name}')

            self.upsert_task_info({
                'task_name': self.current_countdown_task_name,
                'start_time': normal_format_now()
            })
        self.timerDown.start()

    def updateUptime(self):
        self.time += 1
        self.settimer(self.time)

        if self.time % LOG_INTERVAL == 0:
            self.add_log(
                f'{self.current_count_task_name} running... all seem good. '
                f'current time is: {self.format_time_sec(self.time)}'
            )

            self.upsert_task_info({
                'task_name': self.current_count_task_name,
                'current_time': self.format_time_sec(self.time)
            })

    def updateDowntime(self):
        self.time = self.time - 1
        self.settimer(self.time)

        if self.time % LOG_INTERVAL == 0:
            self.add_log(
                f'{self.current_countdown_task_name} running... all seem good. '
                f'current time is: {self.format_time_sec(self.time)}'
            )

            self.upsert_task_info({
                'task_name': self.current_countdown_task_name,
                'current_time': self.format_time_sec(self.time)
            })

        if self.time <= 0:
            self.add_log(f'{self.current_countdown_task_name} completed.')

            self.upsert_task_info({
                'task_name': self.current_countdown_task_name,
                'status': 'completed',
                'end_time': normal_format_now()
            })

            self.timeout.emit()

    def format_time_sec(self, time_sec):
        """
        input time in second output time like that format 00:00:00

        :param time_sec:
        :return:
        """
        time_data = time.gmtime(time_sec)
        hour = time_data.tm_hour
        minute = time_data.tm_min
        second = time_data.tm_sec

        text_time = f'{hour:0>2}:{minute:0>2}:{second:0>2}'
        return text_time

    def settimer(self, time_sec):
        self.time = time_sec
        text_time = self.format_time_sec(self.time)
        self.mywidget.timeViewer.display(text_time)

    def reset(self):
        self.time = 0
        self.settimer(self.time)
        self.mywidget.reset_countdown_edit()

        self.timerUp.stop()
        self.timerDown.stop()
        if self.sound_thread:
            self.sound_thread.requestInterruption()

        self.current_count_task_name = ''
        self.current_countdown_task_name = ''

    def show_running_log(self):
        loginfo = Loginfo(self.running_log)
        loginfo.exec()

    def show_running_record(self):
        running_record = get_json_value('timer.json', 'running_record')
        recordTable = RecordTable(running_record)
        recordTable.exec()

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
        act_show_running_log = menu_help.addAction(self.tr('running log'))
        act_show_running_record = menu_help.addAction(
            self.tr("running record"))
        act_show_running_log.triggered.connect(self.show_running_log)
        act_show_running_record.triggered.connect(self.show_running_record)

        menu_help.addSeparator()
        act_about = menu_help.addAction(self.tr('about this program'))
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
            self.add_log('program quit normally...')
            self.app.exit()
        else:
            # 如果主窗口不显示qt事件循环会终止
            self.showMinimized()

    def reopen(self):
        self.show()

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

    @Slot()
    def beep(self):
        self.timerDown.stop()
        # make a sound
        self.sound_thread = MakeSoundThread(self)
        self.sound_thread.start()

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
