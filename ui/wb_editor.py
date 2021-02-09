#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
from PyQt5.QtWidgets import QTextEdit, QFileDialog, QMessageBox, QVBoxLayout, QApplication, QWidget
from PyQt5.QtCore import QEvent, QTimer, Qt
from ui.ledit_text import LTextEdit
from xml_ctrl import XMLCtrl

class WbEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.qw_wasteland = parent
        self.global_variables = {
            'current_file': None, # 当前编辑的文件名称
            'work_directory': None, # 工作目录
            'current_directory': None # 当前目录，与工作目录的区别是，工作目录中会存在子目录，
            # 如果此时用户在目录树中选择了某个子目录，则当前目录为子目录，否则，当前目录与工作目录一样。
        }
        self.ltextedit = LTextEdit(self)
        self.init_settings()
        self.init_ui()

    def init_ui(self):
        vboxlayout = QVBoxLayout()
        vboxlayout.setSpacing(0)
        vboxlayout.setContentsMargins(0, 0, 0, 0)
        # ltext_edit = LTextEdit(self)
        vboxlayout.addWidget(self.ltextedit)
        self.setLayout(vboxlayout)
        self.set_size_range()

    def set_size_range(self):
        self.setMaximumWidth(1200)
        self.setMinimumWidth(400)

    def sync_content(self):
        pass

    def init_settings(self):
        self.global_variables['work_directory'] = XMLCtrl.get_current_work_directory()
        self.global_variables['current_file'] = XMLCtrl.get_current_filename()
     
