#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout

class WbStatus(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        lbl_filename = QLabel(self)
        lbl_filename.setText('当前文件：')

        hlayout = QHBoxLayout()
        hlayout.addStretch()
        hlayout.addWidget(lbl_filename)

        self.setLayout(hlayout)
        self.setStyleSheet('background-color:red;')
