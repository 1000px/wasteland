#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, datetime, os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from markdown2 import Markdown
from ui.ui_main_win import Ui_MainWindow
from ui.ui_preferences import PreferencesDialog
from convert import LConvert
from xml_ctrl import XMLCtrl

class Editor(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self) 
        self.editor = LTextEdit(self)
        self.editor.setMaximumWidth(1400)
        self.editor.setMinimumWidth(720)

        self.previewer = QTextEdit()
        self.previewer.setMaximumWidth(1400)
        self.previewer.setMinimumWidth(720)
        self.previewer.setReadOnly(True)

        '''编辑器设置'''
        vlayout = QVBoxLayout()

        hlayout = QHBoxLayout()
        hlayout.addStretch()
        hlayout.addWidget(self.editor)
        hlayout.addWidget(self.previewer)
        hlayout.addStretch()
        hlayout.setSpacing(0)

        _widget = QWidget()
        _widget.setLayout(hlayout)
        self.setCentralWidget(_widget)

        '''初始化数据'''
        self.init_data()

        self.editor.textChanged.connect(self.sync_contents)

        # 窗口工具栏设置
        ## 文件相关
        self.__ui.new_file_action.triggered.connect(self.new_file) # 新建文件
        self.__ui.open_file_action.triggered.connect(self.open_file) # 打开文件
        self.__ui.save_file_action.triggered.connect(self.save_file) # 保存文件
        self.__ui.save_as_action.triggered.connect(self.save_as) # 另存为
        #self.__ui.recent_action.triggered.connect(self.recent)

        self.__ui.quit_action.triggered.connect(self.quit_app) # 退出应用

        ## 设置
        self.__ui.preferences_set.triggered.connect(self.set_preferences) # 设置首选项
        self.__ui.theme_set.triggered.connect(self.set_theme) # 主题设置
        self.__ui.background_set.triggered.connect(self.set_background) # 设置背景图
        self.__ui.music_set.triggered.connect(self.set_music) # 设置背景音乐

        ## 账户
        self.__ui.website_account.triggered.connect(self.set_website_account) # 网站设置
        self.__ui.wechat_account.triggered.connect(self.set_wechat_account) # 公众号设置

        ## 帮助
        self.__ui.markdown_help.triggered.connect(self.markdown_help) # markdown语法帮助
        self.__ui.short_key_help.triggered.connect(self.short_key_help) # 快捷键图谱
        self.__ui.about_help.triggered.connect(self.about_help) # 关于
        

    def sync_contents(self):
        '''同步编辑内容'''
        '''
        # 编辑器需要同步三个数据，markdown原始文本、编辑器中显示的文本（包含html标签）、markdown转义成html之后的文本。 
        # 以上三个数据，原始数据存于磁盘文件或数据库中，编辑中显示的是markdown未转义过的内容，但为了让原始文本看起来比较舒服，添加了一些样式。
        # 第三个数据是markdown转义之后html数据，也就是预览窗口需要展示的内容。
        '''
        markdowner = Markdown() 
        # self.previewer.setHtml(markdowner.convert(self.origin_data))
        #self.editor.setHtml(self.css_origin_data)
        self.previewer.clear() 
        for line in self.editor.toPlainText().splitlines():
            self.previewer.append(markdowner.convert(line))

    def init_data(self):
        '''初始化编辑器数据，记载上次未完成的文档'''
        lines = [
            '# 一级标题',
            '## 二级标题',
            '### 三级标题'
        ]
        for line in lines:
            self.editor.append(LConvert().setSheet(line))
            markdowner = Markdown()
            self.previewer.append(markdowner.convert(line))

    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, 'open file', '/home/lucio/')
        self.editor.clear()
        self.previewer.clear()
        self.__current_file = filename[0]
        with open(self.__current_file, 'r') as f:
            for line in f.readlines():
                self.editor.append(LConvert().setSheet(line))
                self.previewer.append(Markdown().convert(line))

    def new_file(self):
        # 添加保存当前编辑文件逻辑

        self.editor.clear()
        self.previewer.clear()
        timestr = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.__current_file = 'default_' + timestr + '.md'
        

    def save_file(self):
        current_file = self.__current_file
        if os.path.isfile(current_file):
            with open(self.__current_file, 'w') as f:
                f.write(self.editor.toPlainText())
        elif XMLCtrl().get_current_work_directory() != 'None':
            dir = XMLCtrl().get_current_work_directory()
            current_file = os.path.join(dir, self.__current_file)
            with open(current_file, 'w') as f:
                f.write(self.editor.toPlainText())
        else: 
            reply = QMessageBox.warning(self, '工作目录', '请先设置工作目录，荒原会将新建的markdown文件保存至该目录!',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                dir = QFileDialog.getExistingDirectory(self, '获取工作目录', '/home/lucio')
                if dir is not None:
                    XMLCtrl().update_directory(dir)
                    with open(os.path.join(dir, current_file), 'w') as f:
                        f.write(self.editor.toPlainText())


        
    
    def save_as(self):
        print('save as')

    def recent(self):
        pass

    def quit_app(self):
        self.close()

    def set_preferences(self):
        dialog = PreferencesDialog()
        dialog.exec_()
        print('preferences set')

    def set_theme(self):
        print('theme set')

    def set_background(self):
        print('background set')

    def set_music(self):
        print('music set')

    def set_website_account(self):
        print('set website account')

    def set_wechat_account(self):
        print('set wechat account')

    def markdown_help(self):
        print('markdown help')

    def short_key_help(self):
        print('short key help')

    def about_help(self):
        print('about help')

class LTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__parent = parent


    def keyReleaseEvent(self, event):
        if event.key() != Qt.Key_Return:
            cursor = self.textCursor()
            pos = cursor.position()
            block = cursor.block()
            block_txt = block.text()
            cursor.beginEditBlock()
            cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
            cursor.removeSelectedText() 
            cursor.insertHtml(LConvert().setSheet(block_txt))
            cursor.endEditBlock()
            cursor.setPosition(pos, QTextCursor.KeepAnchor)
            cursor.setPosition(pos, QTextCursor.MoveAnchor)
            self.setTextCursor(cursor)
