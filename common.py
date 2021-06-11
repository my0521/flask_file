# -*- coding=utf-8 -*-
# @Author:ming yong
# @DATE 2021/6/11 9:30
import os
import zipfile


def find_file(path, filename):
    for root, lists, files in os.walk(path):
        for file in files:
            if filename in file:
                return root
    return None


def zip_dir(dir_path, ignore=[]):
    """
    :param ignore: 忽略压缩文件列表 绝对路径
    :param dir_path: 待压缩目录
    :return:
    """
    zip_file = dir_path + '.zip'
    z = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(dir_path):
        fpath = dirpath.replace(dir_path, '')
        fpath = fpath and fpath + os.sep or ''
        print(fpath)
        if fpath in ignore:
            print("ignore dir :" + fpath)
            continue
        for filename in filenames:
            if filename in ignore:
                print("ignore dir :" + filename)
                continue
            z.write(os.path.join(dirpath, filename), fpath + filename)
    z.close()
