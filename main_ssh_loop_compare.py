#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : ssh_loop_compare
@Time : 2017/11/6 下午2:59
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : main_ssh_loop_compare.py
@desc :
"""

import logging

from tools import parameters_parser

from tools.ssh_connection import SSHConnect
from tools.string_parser import StrParser

r_log = logging.getLogger(parameters_parser.MY_LOG_NAME)


def main():
    cmd_list = ['ls -al /home/git/mss', ]
    in_ip1, in_port1, in_user1, in_code1 = '118.190.113.100', '22', 'root', 'QPmeixun@#2017'
    ssh_con = SSHConnect(in_ip1, in_port1, in_user1, in_code1)
    is_ok = ssh_con.connect_server()
    if is_ok:
        for ci in cmd_list:
            o_stdin, o_stdout, o_stderr = ssh_con.exec_command(ci)
            if o_stdin is not None and o_stdout is not None and o_stderr is not None:
                out1 = o_stdout.readlines()
                for oi in out1:
                    print(StrParser.ls_dir_file_split(oi))
            else:
                print('command <{}> failed'.format(ci))
    ssh_con.disconnect_server()


if __name__ == '__main__':
    main()
