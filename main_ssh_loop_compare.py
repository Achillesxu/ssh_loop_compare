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
import os
import sys
import logging
import time

from tools import parameters_parser

from tools.ssh_connection import SSHConnect
from tools.tool_functions import get_cmd_str, file_name_yield, file_key_name_yield, write_record_to_file
from tools.tool_functions import find_cmd_dir_str, find_cmd_str, find_diff_item_in_lists
SPEC_KEY = '国网ott'
DIFF_AND_LOSE = 'diff_and_lose.txt'
DIR_PROBLEM = 'child_more_than_parent_dir.txt'
DIR_SERIAL_PROBLEM = 'child_parent_serial.txt'


r_log = logging.getLogger(parameters_parser.MY_LOG_NAME)


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
        m_file_list_cmd = get_cmd_str(parameters_parser.para_dict['child_node']['media_root_dir'])
        o_stdin, o_stdout, o_stderr = ssh_con_gs.exec_command(m_file_list_cmd)
        if o_stdin is not None:
            m_file_list = [i for i in file_name_yield(o_stdout)]
            for i_f in m_file_list:
                if ' ' in i_f:
                    i_f = i_f.replace(' ', '\ ')
                m_p_dir_str = find_cmd_dir_str(parameters_parser.para_dict['parent_node']['media_root_dir'], i_f)
                o_in_th, o_out_th, o_err_th = ssh_con_th.exec_command(m_p_dir_str)
                if o_in_th is not None:
                    o_dir_th_list = [i for i in o_out_th]
                    if len(o_dir_th_list) == 0:
                        write_record_to_file(DIR_PROBLEM, '<{}> in child and not in parent'.format(i_f))
                        continue
                else:
                    print('command <{}> get file list failed'.format(m_p_dir_str))
                    sys.exit(-1)
                m_f_serial_str = get_cmd_str(parameters_parser.para_dict['child_node']['media_root_dir'],
                                             i_f, 'media')
                o_stdin_1, o_stdout_1, o_stderr_1 = ssh_con_gs.exec_command(m_f_serial_str)
                m_p_serial_str = get_cmd_str(o_dir_th_list[0], 'media')
                o_in_th1, o_out_th1, o_err_th1 = ssh_con_th.exec_command(m_p_serial_str)
                if o_stdin_1 is not None and o_in_th1 is not None:
                    m_serial_list = [i for i in file_name_yield(o_stdout_1)]
                    m_p_serial_list = [i for i in file_name_yield(o_out_th1)]
                    diff_list = find_diff_item_in_lists(m_p_serial_list, m_serial_list)
                    if diff_list:
                        write_record_to_file(DIR_SERIAL_PROBLEM, i_f)
                        write_record_to_file(DIR_SERIAL_PROBLEM, '总平台剧集：')
                        write_record_to_file(DIR_SERIAL_PROBLEM, '\t' + '\t'.join(sorted(m_p_serial_list)))
                        write_record_to_file(DIR_SERIAL_PROBLEM, '甘肃平台剧集：')
                        write_record_to_file(DIR_SERIAL_PROBLEM, '\t' + '\t'.join(sorted(m_serial_list)))
                        write_record_to_file(DIR_SERIAL_PROBLEM, '总平台与甘肃平台不同的剧集：')
                        write_record_to_file(DIR_SERIAL_PROBLEM, '\t' + '\t'.join(sorted(diff_list)))

                    m_serial_list = sorted(m_serial_list)
                    for i_s in m_serial_list:
                        file_name_count = 0
                        if i_s in m_p_serial_list:
                            m_ts_ifo_list_cmd = get_cmd_str(
                                parameters_parser.para_dict['child_node']['media_root_dir'],
                                i_f, 'media', i_s, 'video')
                            o_stdin_2, o_stdout_2, o_stderr_2 = ssh_con_gs.exec_command(m_ts_ifo_list_cmd)

                            m_p_ts_ifo_list_cmd = get_cmd_str(o_dir_th_list[0], 'media', i_s, 'video')
                            o_in_th2, o_out_th2, o_err_th2 = ssh_con_th.exec_command(m_p_ts_ifo_list_cmd)

                            if o_stdin_2 is not None and o_in_th2 is not None:
                                m_ts_info_list = [i for i in file_key_name_yield(o_stdout_2, SPEC_KEY)]
                                m_p_ts_ifo_list = [i for i in file_key_name_yield(o_out_th2, SPEC_KEY)]
                                diff_list_1 = find_diff_item_in_lists(m_p_ts_ifo_list, m_ts_info_list)
                                diff_name_list = list(set([i[1] for i in diff_list_1]))
                                if file_name_count == 0:
                                    write_record_to_file(DIFF_AND_LOSE, i_f)
                                write_record_to_file(DIFF_AND_LOSE, '\t' + i_s)
                                for i_df in diff_name_list:
                                    write_record_to_file(DIFF_AND_LOSE, '\t\t' + i_df)

                            else:
                                if o_stdin_2 is None and o_in_th2 is None:
                                    print(
                                        'command <{}---{}> get file list failed'.format(m_ts_ifo_list_cmd,
                                                                                        m_p_ts_ifo_list_cmd))
                                elif o_stdin_2 is None:
                                    print('command <{}> get file list failed'.format(m_ts_ifo_list_cmd))
                                elif o_in_th2 is None:
                                    print('command <{}> get file list failed'.format(m_p_ts_ifo_list_cmd))
                        file_name_count += 1
                else:
                    if o_stdin_1 is None and o_in_th1 is None:
                        print('command <{}---{}> get file list failed'.format(m_f_serial_str, m_p_serial_str))
                    elif o_stdin_1 is None:
                        print('command <{}> get file list failed'.format(m_f_serial_str))
                    elif o_in_th1 is None:
                        print('command <{}> get file list failed'.format(m_p_serial_str))
                    ssh_con_gs.disconnect_server()
                    ssh_con_th.disconnect_server()
                    sys.exit(-1)

        else:
            print('command <{}> failed, program exit'.format(m_file_list_cmd))
            ssh_con_gs.disconnect_server()
            ssh_con_th.disconnect_server()
            sys.exit(-1)

    else:
        if is_ok_gs is not True:
            print('10.255.56.19 ssh connect <{}>'.format(parameters_parser.para_dict['child_node']['ip']))
        if is_ok_th is not True:
            print('10.255.56.19 ssh connect <{}>'.format(parameters_parser.para_dict['parent_node']['ip']))

    ssh_con_gs.disconnect_server()
    ssh_con_th.disconnect_server()


if __name__ == '__main__':
    print("let's roll, bro!!!")
    print("Dont touch this!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    start_t = time.time()
    main()
    end_t = time.time()
    print('<{}> using time <{}>'.format(__file__, end_t - start_t))
