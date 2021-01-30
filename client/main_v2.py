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
        
class LTextEdit(QTextEdit): 
    def __init__(self, parent=None):
        super(LTextEdit, self).__init__(parent)
        self.__parent = parent
        self.verticalScrollBar().hide()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.save_file)
        self.timer.start(30000) # 每隔30秒保存一次文件

    def init_text(self, filename):
        _filename = filename if filename is not None else ''
        if os.path.isfile(_filename):
            with open(_filename, 'r') as f:
                self.setHtml(LConverter(f.read(), source='markdown').to_editor())
        else: 
            self.setHtml('<p style="height:24px;line-height:24px;"></p>')

    def save_file(self):
        '''保存文件'''
        filename = self.__parent.global_variables['current_file']
        if os.path.isfile(filename):
            with open(filename, 'w') as f:
                pure_text = LConverter(self.toHtml()).to_text()
                f.write(pure_text)
                
    def open_file(self):
        '''打开文件''' 
        # 先判断是否已经设置工作目录
        work_directory = self.work_directory()
        if work_directory is not None:
            # 打开文件时默认打开当前工作目录
            filename = QFileDialog.getOpenFileName(self, '打开文件', work_directory) 

            if filename[0] == '': 
                return
            self.__parent.global_variables['current_file'] = filename[0]
            XMLCtrl.update_current_filename(filename[0])
            with open(filename[0], 'r') as f:
                article = f.read()
                converter = LConverter(article, source='markdown')
                self.setHtml(converter.to_editor())

    def new_file(self):
        # 先判断是否已经设置工作目录
        work_directory = self.work_directory()
        if work_directory is not None:
            #time_str = datetime.now().strftime('%Y%m%d%H%M%S')
            #filename = os.path.join(work_directory, 'default_' + time_str + '.md')
            # 此处需要添加文件名称验证逻辑
            dialog = FilenameDialog()
            if dialog.exec_():
                text = dialog.get_text()
                if not text.endswith('.md'):
                    text += '.md'

                filename = os.path.join(work_directory, text)
                self.__parent.global_variables['current_file'] = filename
                XMLCtrl.update_current_filename(filename)
                pathlib.Path(filename).touch()
                self.clear()
                self.setFocus()
            
            #
    def work_directory(self):
        work_directory = self.__parent.global_variables['work_directory']
        if work_directory is None:
            reply = QMessageBox.warning(self, '警告', '请先设置工作目录！\n荒原将此目录作为文件默认保存路径。',
                                        QMessageBox.Yes, QMessageBox.Yes)
            work_directory = '/home/'
            work_directory = QFileDialog.getExistingDirectory(self, '工作目录', work_directory)
            if work_directory is None:
                return None
                
            self.__parent.global_variables['work_directory'] = work_directory
            XMLCtrl.update_directory(work_directory)
        return work_directory


    def event(self, event):
        '''快捷键绑定'''
        '''Alt区域'''
        # 全屏、关闭
        if (event.type() == QEvent.KeyPress and event.key() == Qt.Key_F) and \
        (event.modifiers() & Qt.AltModifier):
            '''当用户输入Alt + F时最大化窗口'''
            self.__parent.showFullScreen()
            return True
        elif (event.type() == QEvent.KeyPress and event.key() == Qt.Key_Q) and \
            (event.modifiers() & Qt.AltModifier):
            '''关闭编辑器之前，提示保存内容'''
            self.__parent.close()
            return True
        elif (event.type() == QEvent.KeyPress and event.key() == Qt.Key_P) and \
            (event.modifiers() & Qt.AltModifier):
            work_directory = self.__parent.global_variables['work_directory']
            if work_directory is None:
                work_directory = '/home/'
            dir = QFileDialog.getExistingDirectory(self, '工作目录', work_directory)
            if dir is not None:
                XMLCtrl.update_directory(dir)
                self.__parent.global_variables['work_directory'] = dir
            return True
        # 新建、打开、关闭
        elif (event.type() == QEvent.KeyPress and event.key() == Qt.Key_N) and \
            (event.modifiers() & Qt.ControlModifier):
            '''新建一个暂存的文件，待保存'''
            # 1 保存当前正在编辑的文件
            self.save_file()
            # 2 清空编辑区域，设置新文件默认名称
            self.new_file()
            # 3 更新全局参数
            return True
        elif (event.type() == QEvent.KeyPress and event.key() == Qt.Key_F) and \
            (event.modifiers() & Qt.ControlModifier):
            '''打开一个本地markdown文件'''
            self.open_file()
            return True
        elif (event.type() == QEvent.KeyPress and event.key() == Qt.Key_S) and \
            (event.modifiers() & Qt.ControlModifier):
            '''保存当前正在编辑的文件'''
            self.save_file()
            return True
        else:
            return super().event(event)

    def keyReleaseEvent(self, event):
        cursor = self.textCursor()
        pos = cursor.position()
        
        scroll_pos = self.verticalScrollBar().value()
        article = self.toHtml()
        cursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor)
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        converter = LConverter(article)
        self.setHtml(converter.to_editor())
        
        #pos = pos if pos <= QTextCursor.End else QTextCursor.End
        cursor.setPosition(pos, QTextCursor.KeepAnchor)
        cursor.setPosition(pos, QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)
        self.verticalScrollBar().setValue(scroll_pos)

        self.__parent.sync_content()
