#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
path = r'./ui/'
for filename in os.listdir(path):
    if filename.endswith('.ui'):
        file_name_no_ext = os.path.splitext(filename)[0]
        subprocess.Popen(['pyuic5', '-o', './ui/ui_'+file_name_no_ext+'.py', './ui/'+filename])

#subprocess.Popen(['ls', '-l'])
