#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@license : (C) Copyright 2013-2017, Easy doesnt enter into grown-up life.
@Software: PyCharm
@Project : ssh_loop_compare
@Time : 2017/11/6 下午3:04
@Author : achilles_xushy
@contact : yuqingxushiyin@gmail.com
@Site : 
@File : ssh_connection.py
@desc :
"""
import socket
import paramiko
import logging

from tools import parameters_parser

r_log = logging.getLogger(parameters_parser.MY_LOG_NAME)


class SSHConnect(object):
    def __init__(self, in_ip, in_port, in_user, in_code):
        self.ip = in_ip
        self.port = in_port
        self.user = in_user
        self.s_code = in_code
        self.ssh_connect = paramiko.SSHClient()

    def connect_server(self):
        self.ssh_connect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh_connect.connect(self.ip, port=int(self.port), username=self.user, password=self.s_code, timeout=30)
            return True
        except paramiko.BadHostKeyException as e:
            r_log.error('except info: <{}>'.format(e))
            return False
        except paramiko.AuthenticationException as e:
            r_log.error('except info: <{}>'.format(e))
            return False
        except paramiko.SSHException as e:
            r_log.error('except info: <{}>'.format(e))
            return False
        except socket.error as e:
            r_log.error('except info: <{}>'.format(e))
            return False
        except Exception as e:
            r_log.error('except info: <{}>'.format(e))
            return False

    def exec_command(self, in_cmd_str):
        try:
            r_stdin, r_stdout, r_stderr = self.ssh_connect.exec_command(in_cmd_str)
        except paramiko.SSHException as e:
            r_log.error('except info: <{}>'.format(e))
            return None, None, None
        return r_stdin, r_stdout, r_stderr

    def disconnect_server(self):
        try:
            self.ssh_connect.close()
            return True
        except Exception as e:
            r_log.error('except info: <{}>'.format(e))
            return False


if __name__ == '__main__':
    cmd_list = ['ls -l', 'cd /home/git;pwd;ls -Al']
    in_ip1, in_port1, in_user1, in_code1 = '118.190.113.100', '22', 'root', 'QPmeixun@#2017'
    ssh_con = SSHConnect(in_ip1, in_port1, in_user1, in_code1)
    is_ok = ssh_con.connect_server()
    if is_ok:
        for ci in cmd_list:
            o_stdin, o_stdout, o_stderr = ssh_con.exec_command(ci)
            if o_stdin is not None and o_stdout is not None and o_stderr is not None:
                out1 = o_stdout.readlines()
                for oi in out1:
                    print(oi.split())
            else:
                print('command <{}> failed'.format(ci))
    ssh_con.disconnect_server()






