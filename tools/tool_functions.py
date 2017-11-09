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


def find_cmd_str(in_dir_root, in_sear_str):
    return 'find {} -name \"{}\" | xargs -r ls -Al'.format(in_dir_root, in_sear_str.replace('[', '?'))


def find_cmd_dir_str(in_dir_root, in_sear_str):
    return 'find {} -name \"{}\" -type d'.format(in_dir_root, in_sear_str.replace('[', '?'))


def file_name_yield(in_file_object, in_size=0):
    for i in in_file_object:
        file_rec_list = StrParser.ls_dir_file_split(i)
        if file_rec_list is not None and len(file_rec_list) == 6:
            if in_size:
                yield (file_rec_list[4], file_rec_list[6])
            else:
                yield file_rec_list[6]


def file_key_name_yield(in_file_object, in_key):
    for i in in_file_object:
        if in_key and in_key in i:
            file_rec_list = StrParser.ls_dir_file_split(i)
            if file_rec_list is not None and len(file_rec_list) == 6:
                yield (file_rec_list[4], file_rec_list[6])


def write_record_to_file(in_file_name, in_str):
    with open(in_file_name, 'at', encoding='utf-8', newline='\n') as pf:
        pf.write(in_str+'\n')


def list_str_end_yield(in_list, in_end_with):
    for ii in in_list:
        if ii and ii.endswith(in_end_with):
            yield ii


def find_diff_item_in_lists(in_list1, in_list2):
    """
    :param in_list1:
    :param in_list2:
    :return: list
    """
    return list(set(in_list1) ^ set(in_list2))


if __name__ == '__main__':
    # test_str = ['我擦.git', '我擦.ifo', '三国.git', '水浒.ifo', '西游.git']
    # git_str = [i for i in list_str_end_yield(test_str, '.git')]
    # print(git_str)
    # ifo_str = [i for i in list_str_end_yield(test_str, '.ifo')]
    # print(ifo_str)
    # test_str = ['0018.乐视网-005秘密行动之阿布杰哈德杀戮_1280x720_2500k.ts',
    #             '[52waha]10-01_西甲第7轮_格拉纳达-莱加内斯[Young_Andy]-2_1280x720_1500k.ifo',
    #             '12星魂系列绘本09：乐于分享的天秤座（童伴）_[国网ott-1920x1080-4000k-mp2].ts',
    #             '2013全国高考状元（新课标1）文综_[国网ott-1280x720-1500k].ifo']
    #
    # for i in test_str:
    #     print(find_cmd_dir_str('/storage/block2/media/tianhua', i))

    t_t_1 = [(223, '大海'), (224, '中的相同元素'), (226, '如果使用表理解')]
    t_t_2 = [(223, '大海'), (225, '中的相同元素')]
    diff_l1 = find_diff_item_in_lists(t_t_1, t_t_2)
    print(diff_l1)



