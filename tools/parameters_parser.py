#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : ssh_loop_compare
@Time : 2017/11/6 下午3:17
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : parameters_parser.py
@desc :
"""
import os
import sys
import io
import traceback
import json
import platform
from collections import OrderedDict
import logging
import logging.handlers

__author__ = 'achilles_xushy'

# 记录程序运行中的bug
MY_LOG_NAME = 'run_record'
MY_LOG_FILE_NAME = '{}/{}.log'.format(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), MY_LOG_NAME)

r_log = logging.getLogger(MY_LOG_NAME)
r_log.propagate = False

file_info = logging.handlers.RotatingFileHandler(filename=MY_LOG_FILE_NAME, encoding='utf-8',
                                                 maxBytes=50 * 1024 * 1024, backupCount=5)
file_formatter = logging.Formatter('%(levelname)s－%(asctime)s-%(filename)s-%(funcName)s-[line:%(lineno)d]-%(message)s')
file_info.setFormatter(file_formatter)
r_log.addHandler(file_info)
r_log.setLevel(logging.INFO)


def json_parse(json_dir=''):
    """
    解析目录下的
    :return:
    """
    if len(json_dir) == 0:
        p_dir = os.path.dirname(os.path.abspath(__file__))
        if platform.system() == 'Windows':
            p_dir = p_dir[:p_dir.rfind('\\')]
            json_file = '{}\\{}'.format(p_dir, 'parameters_json.json')
        else:
            p_dir = p_dir[:p_dir.rfind('/')]
            json_file = '{}/{}'.format(p_dir, 'parameters_json.json')
        if os.path.exists(json_file) and os.path.isfile(json_file):
            with io.open(json_file) as pf:
                try:
                    res_dict = json.load(pf, object_pairs_hook=OrderedDict)
                    return res_dict
                except:
                    r_log.error(traceback.format_exc())
                    return None
        else:
            r_log.error('parameters.json dont exist, please check it!')
            return None
    else:
        if os.path.exists(json_dir) and os.path.isfile(json_dir):
            with io.open(json_dir) as pf:
                try:
                    res_dict = json.load(pf, object_pairs_hook=OrderedDict)
                    return res_dict
                except:
                    r_log.error(traceback.format_exc())
                    return None
        else:
            r_log.error('parameters.json dont exist, please check it!')
            return None


para_dict = json_parse('')


def get_para_dict():
    if para_dict is not None:
        return para_dict
    else:
        return None


if __name__ == '__main__':
    if para_dict:
        print(para_dict)
