#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pathlib
from ui.ledit_text import LTextEdit

class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def read_qss(style):
        with open(style, 'r') as f:
            return f.read()

    
    @staticmethod
    def get_work_tree(dir):
        files = []
        current_dir = dir
        if os.path.isdir(current_dir):
            for file_ in os.listdir(current_dir):
                file_item = {
                    'name': file_,
                    'isleaf': True, # True是文件，False是目录
                    'children': None,
                    'dir': current_dir
                }
                leaf_dir = os.path.join(current_dir, file_)
                if os.path.isdir(leaf_dir):
                    file_item['isleaf'] = False
                    file_item['children'] = CommonHelper.get_work_tree(leaf_dir)
                files.append(file_item)
            return files
        
        return None

    @staticmethod
    def add_file(name, dir, sub):
        cur_dir = os.path.join(dir, sub)
        if os.path.isdir(cur_dir):
            filename = os.path.join(cur_dir, name)
            pathlib.Path(filename).touch()

    @staticmethod
    def add_catalogue(name, dir, sub):
        cur_dir = os.path.join(dir, sub)
        if os.path.isdir(cur_dir):
            filename = os.path.join(cur_dir, name)
            pathlib.Path(filename).mkdir()

    @staticmethod
    def delete_file(name, dir):
        if os.path.isdir(dir):
            filename = os.path.join(dir, name)
            pathlib.Path(filename).unlink()

    @staticmethod
    def delete_catalogue(name, dir):
        if os.path.isdir(dir):
            filename = os.path.join(dir, name)
            pathlib.Path(filename).rmdir()

    @staticmethod
    def rename_file(oldname, newname, dir):
        old = os.path.join(dir, oldname)
        new_ = os.path.join(dir, newname)
        if os.path.isfile(old):
            pathlib.Path(old).rename(new_)

    @staticmethod
    def update_edit(name, dir, editor):
        filename = os.path.join(dir, name)
        if os.path.isfile(filename):
            LTextEdit.update_edit(filename, editor)
 
