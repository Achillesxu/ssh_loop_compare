#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : ssh_loop_compare
@Time : 2017/11/7 上午10:46
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : get_dir_all_file_list.py
@desc :
"""
import os
import sys
import time
import logging

from tools import parameters_parser

from tools.ssh_connection import SSHConnect
from tools.string_parser import StrParser

r_log = logging.getLogger(parameters_parser.MY_LOG_NAME)
TREE_FILE_REC = 'media_ts_ifo.txt'


def get_cmd_str(in_dir_root, *in_child):
    cd_path = os.path.join(in_dir_root, *in_child)
    return 'ls -Al ' + cd_path


def file_name_yield(in_file_object):
    for i in in_file_object:
        file_rec_list = StrParser.ls_dir_file_split(i)
        if file_rec_list is not None:
            yield file_rec_list[6]


def write_record_to_file(in_str):
    with open(TREE_FILE_REC, 'at', encoding='utf-8', newline='\n') as pf:
        pf.write(in_str+'\n')


def main():
    in_ip1, in_port1, in_user1, in_code1 = parameters_parser.para_dict['child_node']['ip'],\
                                           parameters_parser.para_dict['child_node']['port'],\
                                           parameters_parser.para_dict['child_node']['user'],\
                                           parameters_parser.para_dict['child_node']['secret']
    ssh_con = SSHConnect(in_ip1, in_port1, in_user1, in_code1)
    is_ok = ssh_con.connect_server()
    if is_ok:
        # get all media names
        m_file_list_cmd = get_cmd_str(parameters_parser.para_dict['child_node']['media_root_dir'])
        o_stdin, o_stdout, o_stderr = ssh_con.exec_command(m_file_list_cmd)
        if o_stdin is not None and o_stdout is not None and o_stderr is not None:
            try:
                m_file_list = [i for i in file_name_yield(o_stdout)]
                print(m_file_list)
            except Exception as e:
                print('command <{}> get file list failed, error <{}> program exit'.format(m_file_list_cmd, e))
                sys.exit(-1)
            for i_f in m_file_list:
                write_record_to_file(i_f)
                m_f_serial_str = get_cmd_str(parameters_parser.para_dict['child_node']['media_root_dir'],
                                             i_f, 'media')
                o_stdin_1, o_stdout_1, o_stderr_1 = ssh_con.exec_command(m_f_serial_str)
                if o_stdin_1 is not None and o_stdout_1 is not None and o_stderr_1 is not None:
                    try:
                        m_serial_list = [i for i in file_name_yield(o_stdout_1)]
                        if m_serial_list:
                            m_serial_list = sorted(m_serial_list)
                            for i_s in m_serial_list:
                                write_record_to_file('\t' + i_s)
                                m_ts_ifo_list_cmd = get_cmd_str(
                                    parameters_parser.para_dict['child_node']['media_root_dir'],
                                    i_f, 'media', i_s, 'video')
                                o_stdin_2, o_stdout_2, o_stderr_2 = ssh_con.exec_command(m_ts_ifo_list_cmd)
                                if o_stdin_2 is not None and o_stdout_2 is not None and o_stderr_2 is not None:
                                    try:
                                        m_ts_info_list = [i for i in file_name_yield(o_stdout_2)]
                                        if m_ts_info_list:
                                            for i_t in m_ts_info_list:
                                                write_record_to_file('\t\t' + i_t)
                                        else:
                                            pass
                                    except Exception as e:
                                        print('command <{}> get file list failed, error <{}> program exit'.format(
                                            m_ts_ifo_list_cmd, e))
                        else:
                            pass
                    except Exception as e:
                        print('command <{}> get file list failed, error <{}> program exit'.format(m_f_serial_str, e))

        else:
            print('command <{}> failed, program exit'.format(m_file_list_cmd))
            sys.exit(-1)
    else:
        print('ssh connection failed, please check parameters_json.json')


if __name__ == '__main__':
    print("let's roll, bro!!!")
    start_t = time.clock()
    main()
    end_t = time.clock()
    print('<{}> using time <{}>'.format(__file__, end_t - start_t))
