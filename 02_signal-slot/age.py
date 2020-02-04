#!/usr/bin/env python3
# -*-coding:utf-8-*-

import sys
from PySide2.QtWidgets import QHBoxLayout, QSlider, QSpinBox, QApplication, \
    QWidget
from PySide2.QtCore import Qt

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("enter your age")
spinBox = QSpinBox()
slider = QSlider(Qt.Horizontal)
spinBox.setRange(0, 130)
slider.setRange(0, 130)

spinBox.valueChanged.connect(slider.setValue)
slider.valueChanged.connect(spinBox.setValue)

spinBox.setValue(35)

layout = QHBoxLayout()
layout.addWidget(spinBox)
layout.addWidget(slider)

window.setLayout(layout)
window.show()

sys.exit(app.exec_())

