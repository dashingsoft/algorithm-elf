# -*- coding: utf-8 -*-
#
#############################################################
#                                                           #
#      版权所有 2009 - 2010 德新软件公司。保留全部权利。    #
#                                                           #
#      数据结构算法助手                                     #
#                                                           #
#      版本区间：1.2.1 -                                    #
#                                                           #
#############################################################
#
#
# @文件：dscore.py
#
# @作者：赵俊德(jondy.zhao@gmail.com)
#
# @创建日期: 2010/02/25
#
# @文件说明：
#
# 算法演示的主驱动程序，由算法演示程序调用，提供操作视图
# 和实体的功能。
#
#     用于演示类的功能
#         pause
#         step
#         abort
#         resume
#
#     内部函数
#         __check
#
#  断点实体：
#      [ 是否可用，函数名称，行号，表达式，命中次数，表达式的当前值 ]
#
#      是否可用为 0 或者 1, 标志当前断点是否可用；
#
#      函数名称，可以为空；
#
#      行号，当前行号；可以为 0， 表示匹配任何行号；
#
#      条件表达式，合法的 Python 表达式，数据环境为：
#
#          断点所在的执行框架中的局部变量，全局变量，以及特殊变量：
#
#              hits, 表示当前断点的命中次数，例如 hits == 1
#              可以使得当前断点命中一次之后永不在停下来
#
#              var 是一个字典，列出当前读写的变量,
#                  var = {'r' : (变量名称列表,...),
#                         'w' : (变量名称列表,...),
#                         }
#                         
#              例如表达式 'x' in var['r']，表示如果读变量 x
#              的时候断点成立
#
#      命中次数，到目前为止断点命中的次数；
#
#      表达式的当前值，适用于监控表达式，可以为 None；
#      
# 驱动实体属性说明
#
#     options, 全部的选项字典
#     
#     player, 演示实体，指向各个视图；
#     
#     data_item, 数据池数据字典
#     
#     algorithm_name, 算法名称
#     
#     m_algorithm，算法类实例
#     
#     m_datapool, 算法中使用的数据池数据，已经转换成为 aftype 的类型
#     
#     co_name, 算法当前执行的代码块名称
#     
#     co_lineno, 算法执行的当前行
#     
# 驱动实体行为说明：
#
#     创建算法实体，
#
#         在可见视图上创建全局堆框架，用来存放全局变量和使用 new 产生的变量
#         
#         根据数据池数据创建算法使用的数据实体
#
#     算法入口模拟，
#
#         在可见视图上创建顶层算法框架
#         初始化算法数据实体
#         初始化堆栈列表
#         初始化当前执行的代码块名称和代码行
#
#     过程调用模拟，
#         在可见视图上增加一个过程框架
#         当前代码行和代码块名称推入堆栈，
#         设置当前执行的代码块名称和代码行
#         初始化变参、值参和局部变量
#         
#     过程返回模拟，
#         在可见视图上删除当前过程框架
#         从调用堆栈中弹出调用者的代码行和名称
#         将函数返回值传递给调用者
#         
#     语句执行模拟，
#         设定当前执行的代码行
#         
#     变量声明模拟，
#         在可见视图的当前堆栈中添加一个变量，变量是一个 aftype 的类型
#         
#     变量删除模拟，
#         在可见视图上删除一个变量，变量是一个 aftype 的类型
#
#     变量修改模拟，
#     
#         简单变量修改，传入参数：var，value
#
#             前者是一个 aftype，后者是一个具体的值，如果为
#             None 则不显示简单变量的内容，但是所占区域不变；
#         
#         结构变量修改，传入参数：var，size
#         
#             结构体内部元素的修改等价于简单变量的修改，这里
#             的修改主要是指数组的大小发生变化等；
#         
#         指针变量修改，传入参数：var，value
#         
#             前者是一个 aftype.Pointer，后者是一个 aftype 的
#             变量，如果为空指针，则显示在过程框架的第一行；
#             
#         树型变量修改，传入参数：var，index，value
#         
#             树变量结点内容的修改等价于简单变量的修改，这里
#             的修改指的是对孩子的修改；
#             
#             var 是一个 aftype.Tree 的变量，index 是孩子的位
#             置，从 0 开始； value 也是一个 aftype.Tree 的变
#             量，可以为 None，说明孩子为空。
#         
#     变量显示模拟，
#         用来显示隐藏的变量；
#     
#     变量隐藏模拟，
#     
#         隐藏一个变量，可以是过程框架隐藏变量，也可以是结构、
#         树隐藏其子结点；也可以是指针变量隐藏；
#     
#     变量高亮模拟，
#     
#         高亮显示一个变量，取消其他变量的高亮显示；
#         
#         变量可以是简单、结构、树或者指针，甚至是过程框架；
#

import os
import sys
import threading
import shutil
from traceback import format_exc
from time import sleep

import aftype


class AlgorithmDriver(object):
    """给算法程序使用的公共接口类。

    用于初始化视图和实体，并且在实体发生变化之后在视图中动态
    显示出来。

    提供的功能包括：

        变量赋值，对全局变量、局部变量和参数的赋值；

        代码执行；

        函数调用；

        函数返回；

    /**     __exit_code
    算法线程的退出代码，含义如下：
        0，算法正常结束
        1，算法自身的错误，譬如不正确的赋值。
        2，表示算法没有正常执行完成，而是用户点击终止
           按钮终止了算法执行
        3，表示算法过程中出现了未知的异常
    */

    """

    def __init__(self, player, options={}):
        """初始化驱动类。"""

        self.options = options
        self.player = player
        self.algorithm_name = ""
        self.m_algorithm = None
        self.m_datapool = {}

        self.co_name = "program"
        self.co_lineno = 0

        self.__playback_status = "run"
        self.__step_mode = 0

        self.stack_list = []
        self.source_list = []
        self.bp_list = []
        self.bp_lineno = 0

        aftype.DRIVER = self
        aftype.VOPTIONS.update(player.options["vision"])
        aftype.DATAPOOL = player.data_pool.items
        
    def load(self, filename):
        """装载算法文件。

        主要操作：

        检查算法文件是否已经被编译成 Python 脚本，其创建时间是否晚于
        算法文件本身。

        初始化代码实体。

        """
        name = os.path.splitext(os.path.basename(filename))[0]
        self.algorithm_name = str(name)

        script = os.path.splitext(filename)[0] + ".py"
        if not os.path.exists(script):
            raise Exception(
                _("There is no compiled algorithm file of '{0}'"
                  ).format(filename)
                )
        shutil.copy(script, "publish")
        self.reset()
        
        self.player.code_view.load(filename)
        f = open(filename)
        for line in f:
            self.source_list.append(line)
        f.close()

        # 装载算法类模块
        name = self.algorithm_name
        m = __import__("publish." + name)
        self.m_algorithm = m.__dict__[name]
        self.m_algorithm.DRIVER = self

        # 显示算法参数
        self.player.para_view.add_paras(self.m_algorithm.var_list)

    def reset(self):
        del self.stack_list[:]
        self.co_lineno = 0

        self.player.stack_view.clear()
        self.player.console_view.clear()        
        self.player.data_view.reset()
        
        self.__playback_status = "open"
        self.__step_mode = 0

    def start(self):
        self.player.data_view.options.update(
            self.player.options["vision"]
            )
        self.reset()
        aftype.VOPTIONS.update(self.player.options["vision"])

        # 设定算法所有的外部参数
        self.m_datapool.clear()
        reload(self.m_algorithm)
        for name in dict(self.m_algorithm.var_list).keys():
            if name not in self.player.data_pool.items:
                raise Exception(
                    _("Algorithm parameter of {0} isn't defined "
                      "in the data pool").format(name)
                    )
            self.m_datapool[name] = self.m_algorithm.__dict__[name]
        self.__playback_status = "pause"
        t = threading.Thread(target=self.__thread_func)
        t.start()

    def __thread_func(self):
        """启动演示算法的线程。"""
        try:
            self.player.console_view.fprint(_("Start %s ...") % self.algorithm_name)
            obj = self.m_algorithm.AlgorithmInstance()
            obj.run()

            # 算法正常完成
            self.player.console_view.fprint(
                _("End algorithm %s.") % self.algorithm_name
                )
            self.__exit_code = 0

        # 算法本身的错误
        except aftype.AlgorithmError, inst:
            self.__exit_code = 1
            self.player.console_view.fprint(str(inst))
            # 调试语句
            # raise

        # 算法被用户终止之后的处理
        except SystemExit:
            self.__exit_code = 2
            self.player.console_view.fprint(
                _("Algorithm is terminated by user")
                )

        except Exception, inst:
            self.__exit_code = 3
            self.player.console_view.fprint(
                _("Playing algorithm failed:")
                )
            self.player.console_view.fprint_err(str(inst))
            self.player.console_view.fprint_err(format_exc())

        # 算法演示完成之后的清理
        finally:
            self.player.var_status.set("finish")

    def simulate_program_entry(self, coname, lineno):
        """模拟算法入口语句，在算法类的 run 方法的第一条语句之前执行。

        传入的参数含义：

           name, 算法名称；

           lineno，主过程 begin 所在的行号；

        """
        self.stack_list.append(["program", lineno, sys._getframe(1)])
        self.co_name = coname
        self.co_lineno = lineno

        self.player.code_view.highlight_line(lineno)
        self.player.stack_view.push(self.stack_list[-1])
        self.player.data_view.push("program", lineno)

        self.__check()

    def simulate_statement(self, lineno, frame, log=False):
        """模拟语句执行。

        算法执行代码的每一条有效语句之前，需要调用本函数。

        主要实现的功能：

             检查回放过程中用户交换信息，是单步还是模拟，还是暂停，还
             是停止，并进行相应的操作;

             高亮显示当前代码行，表示当前已经执行到这里;

             可以显示当前代码行中所包含的变量值，赋值符号左边的变量值
             不显示。

        参数说明：

            lineno，当前执行语句的行号；

            log，是否显示语句到输出窗口。

        """
        self.co_lineno = lineno
        self.bp_lineno = 0
        self.player.code_view.highlight_line(lineno)

        if self.check_breakpoint(frame):
            self.player.var_status.set("pause")
            
        self.__check()

    def simulate_function_call(self, coname, lineno, frame):
        """函数调用模拟实现 ，必须是类方法的第一条语句。

        主要实现的功能：

            新函数的参数和局部变量入栈，并更新到堆栈视图；

            设置代码指针到被调用函数的第一条语句；

        参数说明：

            name,  被调用的函数名称；

            lineno，函数定义所在的行号，就是 begin 语句所在的行；

            data，当前函数的局部变量字典；

        """
        self.stack_list.append([self.co_name, self.co_lineno, frame])

        self.co_name = coname
        self.co_lineno = lineno
        self.bp_lineno = 0

        self.player.data_view.push(coname, lineno)
        self.player.stack_view.push(self.stack_list[-1])
        self.player.code_view.highlight_line(lineno)
        
        if self.check_breakpoint(frame):
            self.player.var_status.set("pause")        
        self.__check()

    def simulate_function_return(self):
        """函数返回模拟，插入到函数调用完成之后的语句后面。

        主要实现的功能：

            堆栈块出栈；

        """
        self.co_name, self.co_lineno, frame = self.stack_list.pop()
        self.player.data_view.pop()
        self.player.stack_view.pop()
        self.player.code_view.highlight_line(self.co_lineno)
        
    def monitor_variable(self, frame, name, mode="r"):
        v = { "r" : [], "w" : [], "v" : [name] }
        v[mode].append(name)
        if self.check_breakpoint(frame, v):
            self.player.var_status.set("pause")
            self.__check()

    def simulate_declare_var(self, var):
        """模拟变量生成语句。

        主要用于变量声明，设定一个局部变量成为可见对象

        参数说明：

            var，新声明的变量，该变量必须在 var 中声明，并且
            必须是 aftype 中定义的类实例。

            对于结构体内部的变量，应该随着结构自动添加到内存
            和堆栈中。

            使用 new 生成的变量，需要使用其他方式处理。

        """
        self.player.data_view.add_variable(var)
        
    def simulate_output(self, msg):
        self.player.view_output.message(msg)

    def simulate_memory_update(self, var):
        """模拟内存数据发生改变。"""
        pass

    def simulate_new_variable(self, var):
        """模拟使用 new 申请堆空间，var 是堆变量。"""
        self.player.data_view.new_heap_variable(var)

    def simulate_dispose_variable(self, var):
        """模拟使用 dispose 释放堆变量，var 是堆变量。"""
        self.player.data_view.dispose_heap_variable(var)

    def simulate_select_variable(self, var):
        """选中局部变量对应的可见对象. """
        self.player.data_view.select_variable(var)

    def simulate_active_variable(self, var):
        """激活局部变量对应的可见对象. """
        self.player.data_view.active_variable(var)

    def simulate_deactive_variable(self, var):
        """取消局部变量对应的可见对象的激活状态. """
        self.player.data_view.deactive_variable(var)

    def simulate_show_variable(self, var):
        """显示局部变量的内容. """
        self.player.data_view.show_variable(var)

    def simulate_hide_variable(self, var):
        """隐藏局部变量的显示内容. """
        self.player.data_view.hide_variable(var)

    def simulate_update_variable(self, var, value):
        """更新 var 对应的对象的值. """
        self.player.data_view.update_variable(var, value)

    def simulate_copy_variable(self, source, dest):
        """复制 source 对应的可见对象到 dest , 两者数据类型必须一致。"""
        self.player.data_view.copy_variable(source, dest)

    def simulate_remove_variable(self, var):
        self.player.data_view.remove_variable(var)

    def check_breakpoint(self, frame, visit={"r":[], "w":[]}):
        """检查监控断点是否成立。 """
        
        if self.co_lineno == self.bp_lineno:
            return None
        
        data = frame.f_locals.copy()
        data.update(self.m_datapool)
        data["hits"] = 0
        data["var"] = visit
        co_name = frame.f_code.co_name

        bpstate = False
        for bp in self.bp_list:
            if not bp[0]:
                continue
            if ((bp[1] == "" or bp[1] == co_name)
                and (bp[2] == 0 or bp[2] == self.co_lineno)):
                try:
                    data["hits"] = bp[4]
                    if bp[3]:
                        value = eval(bp[3], frame.f_globals, data)
                        x = not (value == bp[6])
                        bp[6] = value
                    else:
                        x = True
                    if x:
                        bp[4] += 1
                        bpstate = True
                        break
                except Exception:
                    continue
        if bpstate:
            self.__playback_status = "pause"
            self.bp_lineno = self.co_lineno
            return True

    def __check(self):
        t = self.player.var_interval.get()
        if t:
            sleep(float(t) / 1000)
        while self.__playback_status == 'pause':
            self.bp_lineno = self.co_lineno
            if self.__playback_status == 'abort':
                exit()

        if self.__step_mode == 1:
            if self.__playback_status == 'run':
                self.__playback_status = 'pause'

        if self.__playback_status == 'abort':
            exit()

    def run(self):
        self.__step_mode = 0
        self.__playback_status = 'run'

    def pause(self):
        """用于暂停执行. """
        self.__step_mode = 0
        self.__playback_status = 'pause'

    def step(self):
        """用于单步执行. """
        self.__step_mode = 1
        self.__playback_status = 'run'

    def abort(self):
        self.__step_mode = 0
        self.__playback_status = 'abort'

    def resume(self):
        self.__step_mode = 0
        self.__playback_status = 'run'


if __name__ == '__main__':
    import gettext
    gettext.NullTranslations().install()