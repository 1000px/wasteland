#!/usr/bin/env python
# -*- coding: utf-8 -*-

class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def read_qss(style):
        with open(style, 'r') as f:
            return f.read()

    
