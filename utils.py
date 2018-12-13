# -*- coding:utf-8 -*-
import os.path

main_dir = os.path.split(os.path.abspath(__file__))[0]


# 返回icon中文件的系统文件路径
def load_image(file):
    filePath = os.path.join(main_dir, 'icon', file)
    return filePath
