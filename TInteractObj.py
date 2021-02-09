#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QTextEdit
from common_helper import CommonHelper
from convert2 import LConverter
from xml_ctrl import XMLCtrl
import json
import os

class TInteractObj(QObject):
    SigSendMessageToJS = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.workbench = parent

    def emit_slot(self):
        work_root = XMLCtrl.get_current_work_directory()
        str_parameter = json.dumps(CommonHelper.get_work_tree(work_root))
        self.SigSendMessageToJS.emit(str_parameter)

    @pyqtSlot(result=str)
    def get_tree(self):
        self.emit_slot()
        return 'get tree from js'

    @pyqtSlot(str, str, str)
    def add_file(self, name, dir, sub):
        CommonHelper.add_file(name, dir, sub)
        self.emit_slot() 
        return 'add file from js'
    
    @pyqtSlot(str, str, str)
    def add_catalogue(self, name, dir, sub):
        CommonHelper.add_catalogue(name, dir, sub)
        self.emit_slot()
        return 'add catalogue from js'

    @pyqtSlot(str, str)
    def delete_file(self, name, dir):
        CommonHelper.delete_file(name, dir)
        self.emit_slot()
        return 'delete file from js'

    @pyqtSlot(str, str)
    def delete_catalogue(self, name, dir):
        CommonHelper.delete_catalogue(name, dir)
        self.emit_slot()
        return 'delete catalogue from js'

    @pyqtSlot(str, str)
    def update_edit(self, name, dir):
        filename = os.path.join(dir, name)
        if os.path.isfile(filename):
            XMLCtrl.update_current_filename(filename)
            with open(filename, 'r') as f:
                article_html = LConverter(f.read(), source='markdown').to_editor()
                ltexteidt = self.workbench.editor.ltextedit
                ltexteidt.clear()
                ltexteidt.setHtml(article_html)
                ltexteidt.setFocus()
        return 'update edit by new file link from js'

    @pyqtSlot(str, str, str)
    def rename_file(self, oldname, newname, dir):
        CommonHelper.rename_file(oldname, newname, dir)
        self.emit_slot()
        return 'rename filename from js'
