#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication
from client.main import Editor 
from client.workbench import WorkBench

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #editor = Editor()
    editor = WorkBench()
    editor.show()
    sys.exit(app.exec_())
