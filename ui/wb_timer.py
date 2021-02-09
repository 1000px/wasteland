#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QLCDNumber, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer
from datetime import datetime

class WbTimer(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        vlayout = QVBoxLayout()
        self.lcd_timer = QLCDNumber(self)
        vlayout.addWidget(self.lcd_timer)
        self.lcd_timer.setDigitCount(9)
        self.lcd_timer.display('00:00:00')
        self.lcd_timer.setObjectName('wb_timer')
        self.setLayout(vlayout)
        self.set_size()
        timer = QTimer(self)
        timer.timeout.connect(self.clock)
        timer.start(1000)

    def clock(self):
        dt = datetime.utcnow()
        
        self.lcd_timer.display(dt.strftime('%I:%M:%S'))  

    def set_size(self):
        self.setFixedHeight(130)
        self.setContentsMargins(0, 50, 0, 0)

