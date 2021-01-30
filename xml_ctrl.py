#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.etree import ElementTree as ET

setting_file = 'help/setting.xml'
tree = ET.parse(setting_file)
root = tree.getroot()
settings = root.find('settings')

class XMLCtrl():
    def __init__(self):
        pass

    @staticmethod
    def update_directory(dir):
        directory = settings.find('directory')
        directory.text = dir
        tree.write(setting_file)

    @staticmethod
    def get_current_work_directory():
        directory = settings.find('directory')
        return directory.text if directory is not None else None

    @staticmethod
    def update_current_filename(filename):
        current_file = settings.find('current_file')
        current_file.text = filename
        tree.write(setting_file)

    @staticmethod
    def get_current_filename():
        current_filename = settings.find('current_file')
        return current_filename.text if current_filename is not None else None
