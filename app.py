#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication
from client.main_v2 import Editor 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = Editor()
    editor.show()
    sys.exit(app.exec_())
