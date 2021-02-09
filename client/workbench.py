#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
新版工作台
三栏显示：左侧为工作目录，即所有markdown文件结构
            中间为编辑区
            右侧为工作台：时钟，可配置定时器，音乐加载，当前天气，其它可配置内容
'''
import sys, os
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QApplication, QPushButton
from PyQt5.QtCore import Qt
from ui.wb_left import WbLeft
from ui.wb_editor import WbEditor
from ui.wb_right import WbRight
from ui.wb_toolbar import WbToolbar
from ui.wb_status import WbStatus
from common_helper import CommonHelper
from TInteractObj import TInteractObj
from PyQt5.QtWebChannel import QWebChannel

'''
工作台，WorkBench
缩写为wb，比如
wb_left 工作台左栏
wb_editor 工作台编辑区
wb_right 工作台右栏
'''
class WorkBench(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        #self.current_screen = 0

    def init_ui(self): 
        hlayout_bench = QHBoxLayout() 
        # 左侧目录
        self.left = WbLeft()
        # 中间编辑区域
        self.editor = WbEditor(self)
        # 右侧工作台
        self.right = WbRight()

        hlayout_bench.addStretch()
        hlayout_bench.addWidget(self.left)
        hlayout_bench.addWidget(self.editor)
        hlayout_bench.addWidget(self.right)
        hlayout_bench.addStretch()
        
        self.setLayout(hlayout_bench)
        self.setWindowFlag(Qt.FramelessWindowHint)
        # 全屏展示
        hlayout_bench.setSpacing(0)
        hlayout_bench.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet(CommonHelper.read_qss('./resource/style/workbench.qss'))
        self.set_win_size(0)

        self.webChannel = QWebChannel(self.left.browser.page())
        self.webInteractObj = TInteractObj(self)
        self.webChannel.registerObject('interactObj', self.webInteractObj)

        self.left.browser.page().setWebChannel(self.webChannel) 

     # 设置主窗口显示尺寸和位置
    def set_win_size(self, current_screen=0):
        desktop = QApplication.desktop()
        geo = desktop.availableGeometry(current_screen)
        # 如果显示器的宽度< 1440，那么，全屏显示编辑器
        if geo.width() <= 1440:
            w = geo.width()
            h = geo.height()
            a = geo.x()
            b = geo.y()
            s = 300
        else: # 当显示器的宽度> 1440，可以显示80%尺寸
            
            w = int(geo.width()*.8)
            h = int(geo.height()*.8)
            a = int(geo.x() + geo.width()*.1)
            b = int(geo.y() + geo.height()*.1)
            s = 480


        self.left.setFixedWidth(s)
        self.right.setFixedWidth(s)
        self.editor.setFixedWidth(w-2*s)
 
        self.normal_screen = {'width': w, 'height': h}

        self.setGeometry(a, b, w, h)
        self.setFixedWidth(w)
        self.current_screen = current_screen
        #self.add_toolbar() 
        #self.add_status()

    def resizeEvent(self, event):
        self.add_toolbar()
        self.add_status()

    def toggle_screen(self):
        desktop = QApplication.desktop()
        count = desktop.screenCount()
        current_screen = self.current_screen + 1 if self.current_screen + 1 < count else 0
        self.set_win_size(current_screen)

    def add_toolbar(self):
        toolbar = WbToolbar(self) 
        if self.isFullScreen():
            desktop = QApplication.desktop()
            geo = desktop.availableGeometry(desktop.screenNumber())
        else:
            geo = self.geometry()
        toolbar.setGeometry(int(geo.width()/2), 0, int(geo.width()/2), 40)

    def add_status(self):
        statusbar = WbStatus(self)
        if self.isFullScreen():
            desktop = QApplication.desktop()
            geo = desktop.availableGeometry(desktop.screenNumber())
        else:
            geo = self.geometry()
        statusbar.setGeometry(int(geo.width()/2), geo.height()-40, int(geo.width()/2), 40)

    def full_screen(self):
        self.showFullScreen()

    def close_app(self):
        self.close()

    @classmethod
    def get_current_editor(cls):
        return g_editor
