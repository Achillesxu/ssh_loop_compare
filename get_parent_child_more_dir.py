#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : ssh_loop_compare
@Time : 2017/11/9 下午5:21
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : get_parent_child_more_dir
@desc :
"""
import sys
import logging
import time

from tools import parameters_parser

from tools.ssh_connection import SSHConnect

PARENT_MORE_FIR = 'parent_more_child.txt'


def main():
    in_ip1, in_port1, in_user1, in_code1 = parameters_parser.para_dict['child_node']['ip'],\
                                           parameters_parser.para_dict['child_node']['port'],\
                                           parameters_parser.para_dict['child_node']['user'],\
                                           parameters_parser.para_dict['child_node']['secret']
    ssh_con_gs = SSHConnect(in_ip1, in_port1, in_user1, in_code1)

    in_ip2, in_port2, in_user2, in_code2 = parameters_parser.para_dict['parent_node']['ip'], \
                                           parameters_parser.para_dict['parent_node']['port'],\
                                           parameters_parser.para_dict['parent_node']['user'],\
                                           parameters_parser.para_dict['parent_node']['secret']
    ssh_con_th = SSHConnect(in_ip2, in_port2, in_user2, in_code2)

    is_ok_gs = ssh_con_gs.connect_server()
    is_ok_th = ssh_con_th.connect_server()

    if is_ok_gs and is_ok_th:
        both_con = 1
    else:
        both_con = 0

    if both_con:
        pass

    else:
        if is_ok_gs is not True:
            print('10.255.56.19 ssh connect <{}>'.format(parameters_parser.para_dict['child_node']['ip']))
        if is_ok_th is not True:
            print('10.255.56.19 ssh connect <{}>'.format(parameters_parser.para_dict['parent_node']['ip']))

    ssh_con_gs.disconnect_server()
    ssh_con_th.disconnect_server()


if __name__ == '__main__':
    print("let's roll, bro!!!")
    start_t = time.time()
    main()
    end_t = time.time()
    print('<{}> using time <{}>'.format(__file__, end_t - start_t))