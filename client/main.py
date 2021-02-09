#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, datetime, os
import pathlib
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ui.filename_dialog import FilenameDialog
from markdown2 import Markdown
from xml_ctrl import XMLCtrl
from common_helper import CommonHelper
from bs4 import BeautifulSoup
from convert2 import LConverter
from datetime import datetime

from ui.ledit_text import LTextEdit

class Editor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.global_variables = {
            'current_file': None, # 当前编辑的文件名称
            'work_directory': None, # 工作目录
            'current_directory': None # 当前目录，与工作目录的区别是，工作目录中会存在子目录，
            # 如果此时用户在目录树中选择了某个子目录，则当前目录为子目录，否则，当前目录与工作目录一样。
        }
        self.init_settings()
        self.init_ui()
        self.sync_content()

    def init_ui(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.set_win_size()
        self.setObjectName('editor')
        self.setStyleSheet(CommonHelper.read_qss('./resource/style/brief.qss'))
        
        hlayout = QHBoxLayout()
        # 左侧编辑区域
        editor_left = LTextEdit(self)
        editor_left.setObjectName('editor_left')
        editor_left.init_text(self.global_variables['current_file'])
        # 右侧预览区域
        editor_right = QTextEdit()
        editor_right.setObjectName('editor_right')
        editor_right.verticalScrollBar().hide()
        editor_right.setReadOnly(True)
        hlayout.addWidget(editor_left)
        hlayout.addWidget(editor_right)
        hlayout.setSpacing(0)
        hlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hlayout)
        
        # 工具按钮
        btn_close = QPushButton(self)
        btn_close.setObjectName('btn_close')
        btn_eye = QPushButton(self)
        btn_eye.setObjectName('btn_eye')
        btn_open = QPushButton(self)
        btn_open.setObjectName('btn_open')
        btn_video = QPushButton(self)
        btn_video.setObjectName('btn_video')
        btn_full_screen = QPushButton(self)
        btn_full_screen.setObjectName('btn_full_screen')
        btn_setting = QPushButton(self)
        btn_setting.setObjectName('btn_setting')
        btn_help = QPushButton(self)
        btn_help.setObjectName('btn_help')

        # 顶部工具栏
        widget_top = QWidget(self)
        self.set_top_size(widget_top)
        self.top_widget = widget_top
        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)

        hbox.addStretch()
        hbox.addWidget(btn_full_screen)
        hbox.addWidget(btn_eye)
        hbox.addWidget(btn_open)
        hbox.addWidget(btn_video)
        hbox.addWidget(btn_setting)
        hbox.addWidget(btn_help)
        hbox.addWidget(btn_close)
        widget_top.setLayout(hbox)

        # 底部状态栏，显示当前编辑文件
        widget_bottom = QWidget(self)
        self.set_bottom_size(widget_bottom)
        self.bottom_widget = widget_bottom
        status_label = QLabel('当前文件:')
        status_label.setAlignment(Qt.AlignRight)
        hb = QHBoxLayout()
        hb.addWidget(status_label)
        widget_bottom.setLayout(hb)
        
        
        self.btn_close = btn_close
        self.btn_eye = btn_eye
        self.btn_open = btn_open
        self.btn_video = btn_video
        self.btn_full_screen = btn_full_screen
        self.btn_help = btn_help
        self.btn_setting = btn_setting

        self.__editor = editor_left
        self.__previewer = editor_right
        self.signal_connected()

    # 初始化设置
    def init_settings(self):
        self.global_variables['work_directory'] = XMLCtrl.get_current_work_directory()
        self.global_variables['current_file'] = XMLCtrl.get_current_filename()
        
    # 信号绑定
    def signal_connected(self):
        self.btn_close.clicked.connect(self.close)
        self.btn_full_screen.clicked.connect(self.toggle_full_screen)
        #self.__editor.textChanged.connect(self.sync_content)
        #self.__editor.textChanged.connect(self.ppr)
        self.btn_eye.clicked.connect(self.change_screen)
        self.__editor.verticalScrollBar().actionTriggered.connect(self.change_scroll)

    # 同步滚动编辑区和预览区
    def change_scroll(self):
        self.__previewer.verticalScrollBar().setValue(self.__editor.verticalScrollBar().value())

    # 改变显示位置（在不同的显示器之间切换）
    def change_screen(self):
        desktop = QApplication.desktop()
        count = desktop.screenCount()
        current_screen = self.current_screen_num+1 if self.current_screen_num+1<count else 0
        self.set_win_size(current_screen)

    # 设置主窗口显示尺寸和位置
    def set_win_size(self, current_screen=0):
        desktop = QApplication.desktop()
        desktop_rect = desktop.availableGeometry(current_screen)
        
        self.normal_screen = {'width': int(desktop_rect.width()*.8), 'height': int(desktop_rect.height()*.8)}
        
        w = int(desktop_rect.width()*.8)
        h = int(desktop_rect.height()*.8)
        a = int(desktop_rect.x() + desktop_rect.width()*.1)
        b = int(desktop_rect.y() + desktop_rect.height()*.1)

        self.setGeometry(a, b, w, h)
        self.current_screen_num = current_screen

    # 设置顶部工具栏尺寸
    def set_top_size(self, widget):
        size = self.geometry()
        widget.setGeometry(size.width()/2, 0, size.width()/2, 40)

    # 设置底部状态栏显示尺寸
    def set_bottom_size(self, widget):
        size = self.geometry()
        widget.setGeometry(size.width()/2, size.height()-40, size.width()/2, 40)

    # 同步更新预览区内容
    def sync_content(self):
        converter = LConverter(self.__editor.toHtml())
        self.__previewer.setHtml(converter.to_previewer())
        self.change_scroll()

    # 切换窗口显示状态，全屏或正常
    def toggle_full_screen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
    def resizeEvent(self, event):
        self.set_top_size(self.top_widget)
        self.set_bottom_size(self.bottom_widget)
     
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F:
            if event.modifiers() & Qt.AltModifier:
                self.showFullScreen()
        elif event.key() == Qt.Key_Escape:
            self.showNormal()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_drag_position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_drag_position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
        

