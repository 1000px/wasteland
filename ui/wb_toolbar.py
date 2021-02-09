#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget

class WbToolbar(QWidget):
    def __init__(self, parent=None):
        super(WbToolbar, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        # 工具按钮
        btn_close = QPushButton(self)
        btn_close.setObjectName('btn_close') # 关闭
        btn_eye = QPushButton(self)
        btn_eye.setObjectName('btn_eye') # 切换编辑/预览状态
        btn_open = QPushButton(self)
        btn_open.setObjectName('btn_open') # 打开
        btn_video = QPushButton(self)
        btn_video.setObjectName('btn_video') # 设置音乐文件
        btn_full_screen = QPushButton(self)
        btn_full_screen.setObjectName('btn_full_screen') # 全屏
        btn_setting = QPushButton(self)
        btn_setting.setObjectName('btn_setting') # 设置
        btn_help = QPushButton(self)
        btn_help.setObjectName('btn_help') # 帮助
        
        hlayout = QHBoxLayout()
        hlayout.addStretch()
        hlayout.addWidget(btn_help)
        hlayout.addWidget(btn_open)
        hlayout.addWidget(btn_video)
        hlayout.addWidget(btn_eye)
        hlayout.addWidget(btn_full_screen)
        hlayout.addWidget(btn_setting)
        hlayout.addWidget(btn_close)
        hlayout.setSpacing(0)
        hlayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(hlayout)

