#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
import pathlib
from PyQt5.QtWidgets import QTextEdit, QFileDialog, QMessageBox
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QEvent, QTimer, Qt
from xml_ctrl import XMLCtrl
from ui.filename_dialog import FilenameDialog
from convert2 import LConverter

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
        #filename = self.__parent.global_variables['current_file']
        filename = XMLCtrl.get_current_filename()
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
            #self.__parent.global_variables['current_file'] = filename[0]
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
                # self.__parent.global_variables['current_file'] = filename
                XMLCtrl.update_current_filename(filename)
                pathlib.Path(filename).touch()
                self.clear()
                self.setFocus()
            
            #
    def work_directory(self):
        work_directory = self.__parent.global_variables['work_directory']
        work_directory = XMLCtrl.get_current_work_directory()
        if not os.path.isdir(work_directory):
            reply = QMessageBox.warning(self, '警告', '请先设置工作目录！\n荒原将此目录作为文件默认保存路径。',
                                        QMessageBox.Yes, QMessageBox.Yes)
            work_directory = '/home/'
            work_directory = QFileDialog.getExistingDirectory(self, '工作目录', work_directory)
            if work_directory is None:
                return None
                
            #self.__parent.global_variables['work_directory'] = work_directory
            XMLCtrl.update_directory(work_directory)
        return work_directory

    def event(self, event):
        '''快捷键绑定'''
        '''Alt区域'''
        # 全屏、关闭
        if (event.type() == QEvent.KeyPress and event.key() == Qt.Key_F) and \
        (event.modifiers() & Qt.AltModifier):
            '''当用户输入Alt + F时最大化窗口'''
            #self.__parent.showFullScreen()
            self.__parent.qw_wasteland.full_screen()
            return True
        elif (event.type() == QEvent.KeyPress and event.key() == Qt.Key_Q) and \
            (event.modifiers() & Qt.AltModifier):
            '''关闭编辑器之前，提示保存内容'''
            #self.__parent.close()
            self.__parent.qw_wasteland.close_app()
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
