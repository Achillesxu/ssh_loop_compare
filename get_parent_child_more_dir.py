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
from tools.tool_functions import get_cmd_str, file_name_yield, file_key_name_yield, write_record_to_file
from tools.tool_functions import find_cmd_dir_str, find_cmd_str, find_diff_item_in_lists


PARENT_MORE_FIR = 'parent_more_child_dir.txt'
EXCEPT_LIST = ['adok', ]


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
        tianhua_m_list = []
        m_p_dir_list_cmd = get_cmd_str(parameters_parser.para_dict['parent_node']['media_root_dir'])
        o_in_th, o_out_th, o_err_th = ssh_con_th.exec_command(m_p_dir_list_cmd)
        if o_in_th is not None:
            top_dir_name_list = [i for i in file_name_yield(o_out_th) if i not in EXCEPT_LIST]
            for i_d in top_dir_name_list:
                m_p_sub_dir_list_cmd = get_cmd_str(parameters_parser.para_dict['parent_node']['media_root_dir'], i_d)
                o_in_th1, o_out_th1, o_err_th1 = ssh_con_th.exec_command(m_p_sub_dir_list_cmd)
                if o_out_th1 is not None:
                    sub_dir_name_list = [i for i in file_name_yield(o_out_th1)]
                    tianhua_m_list.extend(sub_dir_name_list)
                else:
                    print('command <{}> get file list failed'.format(m_p_sub_dir_list_cmd))
                    sys.exit(-1)

            m_file_list_cmd = get_cmd_str(parameters_parser.para_dict['child_node']['media_root_dir'])
            o_stdin, o_stdout, o_stderr = ssh_con_gs.exec_command(m_file_list_cmd)
            if o_stdout is not None:
                m_sub_name_list = [i for i in file_name_yield(o_stdout)]
            else:
                print('command <{}> get file list failed'.format(m_file_list_cmd))
                sys.exit(-1)
            for i_name in tianhua_m_list:
                if i_name not in m_sub_name_list:
                    write_record_to_file(PARENT_MORE_FIR, i_name)
        else:
            print('command <{}> get file list failed'.format(m_p_dir_list_cmd))

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
