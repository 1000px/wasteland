#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QTextEdit, QTreeWidget, QTreeWidgetItem, QPushButton
from PyQt5.QtCore import Qt, QUrl, pyqtProperty, QObject
from PyQt5.QtGui import QBrush
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from TInteractObj import TInteractObj
from xml_ctrl import XMLCtrl
import os

class WbLeft(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        #self.work_root()

    def init_ui(self):
        vlayout = QVBoxLayout()
        self.browser = QWebEngineView()
        current_dir = os.getcwd()

        btn_fresh = QPushButton(self)
        btn_fresh.setText('刷新页面')
        btn_js = QPushButton(self)
        btn_js.setText('执行js')

        url = str(current_dir) + r'/resource/html/catalogue/web.html'
        self.browser.load(QUrl('file:///' + url))
        self.browser.setObjectName('wb_left')
        vlayout.addWidget(btn_fresh)
        vlayout.addWidget(btn_js)
        vlayout.addWidget(self.browser)
        vlayout.setSpacing(0)
        vlayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(vlayout)

        btn_fresh.clicked.connect(self.url_reload)

    def url_reload(self):
        self.browser.reload()

    def work_root(self):
        # 获取当前工作目录下目录+文件结构
        # 判断是否已经设置工作目录
        work_root = XMLCtrl.get_current_work_directory()
        root_tree = self.get_files(work_root)

    def get_files(self, dir):
        files = []
        current_dir = dir
        if os.path.isdir(current_dir):
            for file_ in os.listdir(current_dir):
                file_item = {
                    'name': file_,
                    'isleaf': True, # True是文件，False是目录
                    'children': None
                }
                leaf_dir = os.path.join(current_dir, file_)
                if os.path.isdir(leaf_dir):
                    file_item['isleaf'] = False
                    file_item['children'] = self.get_files(leaf_dir)
                files.append(file_item)
            return files
        
        return None
            
