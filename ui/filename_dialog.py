#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QLineEdit

class FilenameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        #self.exec_()

    def init_ui(self):
        self.setWindowTitle('新建文件')
        self.resize(480, 160)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.move(270, 110)

        label = QLabel('请输入文件名：', self)
        label.move(40, 30)
        input_ = QLineEdit(self)
        input_.move(40, 60)
        input_.resize(400, 28)
        input_.setFocus()

        self.editor = input_
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def get_text(self):
        return self.editor.text()
