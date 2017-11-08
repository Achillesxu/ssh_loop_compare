#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : ssh_loop_compare
@Time : 2017/11/8 上午11:07
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : tool_functions.py
@desc :
"""

import os

from tools.string_parser import StrParser


def get_cmd_str(in_dir_root, *in_child):
    cd_path = os.path.join(in_dir_root, *in_child)
    return 'ls -Al ' + cd_path


def file_name_yield(in_file_object, in_size=0):
    for i in in_file_object:
        file_rec_list = StrParser.ls_dir_file_split(i)
        if file_rec_list is not None:
            if in_size:
                yield (file_rec_list[4], file_rec_list[6])
            else:
                yield file_rec_list[6]


def write_record_to_file(in_file_name, in_str):
    with open(in_file_name, 'at', encoding='utf-8', newline='\n') as pf:
        pf.write(in_str+'\n')


def list_str_end_yield(in_list, in_end_with):
    for ii in in_list:
        if ii and ii.endswith(in_end_with):
            yield ii


if __name__ == '__main__':
    test_str = ['我擦.git', '我擦.ifo', '三国.git', '水浒.ifo', '西游.git']
    git_str = [i for i in list_str_end_yield(test_str, '.git')]
    print(git_str)
    ifo_str = [i for i in list_str_end_yield(test_str, '.ifo')]
    print(ifo_str)

