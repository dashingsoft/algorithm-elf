# -*- coding: utf-8 -*-
#
# @文件：buildprocess.py
#
# @作者：赵俊德(jondy.zhao@gmail.com)
#
# @创建日期: 2010/01/13
#
# @文件说明：
#
#

import sys
import os
import threading
import subprocess

class BuildProcess:
    """启动一个进程，同时将进程的信息输出."""

    def __init__(self, args, output=None, clean=None):
        try:
            self.__p = subprocess.Popen(
                args,                
                bufsize=1,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                )
        except OSError, inst:
            raise
        except ValueError, inst:
            raise

        try:
            self.__t = threading.Thread(
                target=self.__output,
                args=(self.__p, output, clean)
                )
            self.__t.start()
        except RuntimeError, inst:
            raise

    def kill(self):
        """终止进程和输出线程."""

        if self.__p.returncode is None:
            # 杀掉进程，有可能出现 WindowsError 的异常
            try:
                self.__p.kill()
            except Exception, inst:
                print str(inst)

            # 等待进程退出
            self.__p.wait()

        # 等待线程退出，超时时间为 0.1 秒
        self.__t.join(0.1)

        # 线程是否已经退出
        if self.__t.is_alive():
            print _("Warning: thread is alive")

    def wait(self):
        self.__p.wait()
        self.__t.join(0.1)

    def __printf(self, message):
        print message

    def __output(self, p, output, clean):
        if not callable(output):
            output = self.__printf

        # 循环读取进程信息
        while p.returncode is None:
            s = p.stdout.readline()
            if s == "":
                break
            output(s)

        # 读取进程的最后输出
        # (stdoutdata, stderrdata) = self.__p.communicate()
        # output(stderrdata)

        # 调用清理函数
        if callable(clean):
            clean()