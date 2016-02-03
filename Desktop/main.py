# -*- coding:utf-8 -*-
import os

files = os.walk("./source/")
for f in files:
    print f
print os.getcwd()
print os.chdir(os.getcwd())