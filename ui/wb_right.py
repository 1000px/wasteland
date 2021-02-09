#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from ui.wb_timer import WbTimer

class WbRight(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        vlayout = QVBoxLayout()
        vlayout.setSpacing(0)
        vlayout.setContentsMargins(0, 0, 0, 0)
        
        wb_timer = WbTimer(self)
        vlayout.addWidget(wb_timer)
        vlayout.addStretch()
        self.setLayout(vlayout)
        self.setStyleSheet('background-color: #e9e9e9')        
        self.set_size_range()

    def set_size_range(self):
        #self.setFixedWidth(480)
        pass
        
