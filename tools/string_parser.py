#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : ssh_loop_compare
@Time : 2017/11/6 下午5:41
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : string_parser.py
@desc :
"""
import logging
from pyparsing import Word, nums, alphas, alphanums, printables, Regex, OneOrMore, Combine, ParseException

from tools import parameters_parser

r_log = logging.getLogger(parameters_parser.MY_LOG_NAME)


class StrParser(object):
    def __init__(self):
        pass

    @staticmethod
    def ls_dir_file_split(in_str):

        f_type = Word('-dlcbpsrwx.+', min=10)
        f_links = Word(nums, min=1)
        f_user = f_group = Word(alphanums, min=1)
        f_size = Word(nums, min=1)
        f_time = Regex(r'(?<=\d )\d{1,2}\w +\d{1,2} [0-9\:]{4,5}(?= )')
        f_name = Regex(r'(?<=\d ).+(?=\n)')

        f_in_str = f_type + f_links + f_user + f_group + f_size + f_time + f_name
        try:
            res_list = f_in_str.parseString(in_str)
        except ParseException as e:
            r_log.warning('in_str <{}> pattern cant match, Exception <{}>'.format(in_str, e))
            return None
        except Exception as e:
            r_log.warning('in_str <{}>, Exception error <{}>'.format(in_str, e))
            return None
        return res_list


if __name__ == '__main__':
    fp = open('/Users/achilles_xushy/Desktop/python2/ssh_loop_compare/media_name_list.txt', mode='rt')
    for ii in fp:
        res_token = StrParser.ls_dir_file_split(ii)
        print(res_token)
    fp.close()
