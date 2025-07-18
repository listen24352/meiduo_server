#!/usr/bin/env python
import sys
import os
import django

sys.path.insert(0, '../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings")
# django setup
# 相当于 当前的文件 有了django的环境
django.setup()

if __name__ == '__main__':
    from apps.contents.crons import generic_meiduo_index
    generic_meiduo_index()
