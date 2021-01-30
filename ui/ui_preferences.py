#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from xml_ctrl import XMLCtrl

class PreferencesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(1000, 680)
        self.center()
        self.setFixedSize(self.width(),self.height())
        self.setWindowTitle('Preference')
        self.setWindowModality(Qt.ApplicationModal)
        layout = QGridLayout()
        lb00 = QLabel('工作目录：')
        self.lb01 = QLabel(XMLCtrl().get_current_work_directory())
        btn02 = QPushButton('设置')
        layout.addWidget(lb00, 0, 0)
        layout.addWidget(self.lb01, 0, 1, 0, 8)
        layout.addWidget(btn02, 0, 9)
        self.setLayout(layout)

        btn02.clicked.connect(self.set_directory)

    def set_directory(self):
        direcotry = QFileDialog.getExistingDirectory(self, '获取工作目录', '/home/lucio/')
        XMLCtrl().update_directory(direcotry)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())/2, (screen.height() - size.height())/2)
