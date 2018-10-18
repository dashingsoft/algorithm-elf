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

"""
 * @文件：dsentity.py
 *
 * @作者：赵俊德(jondy.zhao@gmail.com)
 *
 * @创建日期: 2010/02/25
 *
 * @文件说明：
 *
 *   定义代码和堆栈实体，用于存储算法执行过程中的堆栈状态。
 *
"""

import os
import aftype
import codecs


class CodeEntity(object):
    """代码实体类，存放算法的源代码和代码执行的状态。

属性：
    current         当前执行的代码行数，第一行为 1
    name            代码段函数名称
    __source_list   列表，源代码的每一行对应其中一个元素

    __filename      算法文件名称
    __original      文件的原始内容

    """

    def __init__(self):
        self.__source_list = []
        self.clear()

    def clear(self):
        self.name = ""
        self.current = 0
        del self.__source_list[:]
        self.__original = ""

    def load_from_file(self, filename):
        """使用文件初始化代码实体. """
        self.__filename = filename
        # 默认文件为 utf-8 编码
        f = codecs.open(filename, 'r', encoding='utf-8')
        self.__original = f.read()
        f.close()

        self.__source_list = self.__original.split("\n")
        self.current = 0
        _basename = os.path.basename(filename)
        self.name = os.path.splitext(_basename)[0]

    def get_source_list(self, first=None, last=None):
        """根据传入的行号返回对应的源代码.

        first 表示开始行号，从 1 开始计算。
        last 表示结束行号，默认值和 first 相同。
        如果两者都是 None，那么返回全部代码。

        """
        if last is None:
            last = first
        if first is not None:
            first -= 1
        return self.__source_list[first:last]

    def get_statement(self, lineno):
        """得到指定行对应的一条语句. """
        try:
            value = self.__source_list[lineno - 1]
        except IndexError:
            return ""
        else:
            return value


class StackEntity(object):
    """调用堆栈实体，存放函数的调用序列。

调用堆栈实体存储的数据包括：全局变量，调用堆栈。

调用堆栈是由一系列的调用帧组成，每一帧又由两部分组成：

    地址信息：父函数名称, 返回指针，当前函数名称，开始行号

    数据信息：当前函数的局部变量和传入的参数

在算法演示开始的时候，对全局变量进行初始化；在算法演示过程中，
对全局变量进行修改；另外最主要的是函数调用产生的堆块的出栈和
入栈，以及对局部变量的修改。

调用堆栈的最顶层是一个虚拟的主函数入口：

    addr = [ 'program', 0, 'main', 0 ]
    data = {}

算法初始化完成之后是算法函数入口：

    code = [ 'main', 0, 算法名称, 开始行号 ]
    data = 传入的参数

全局变量和局部变量使用字典来保存。

全局变量和局部变量必须是 aftype 或者 dstype 中定义的数据类。


    """

    def __init__(self):
        self.__global_data = {}
        self.__stack_data = []

        self.clear()

    def clear(self):
        """清空堆栈. """
        self.__global_data.clear()
        del self.__stack_data[:]

    def __getattr__(self, name):
        if name == "top_level":
            value = len(self.__stack_data)
            return value

    def get_function_name(self):
        _data = self.__stack_data[-1]
        _value = _data[0][2]
        return _value

    def get_caller_addr(self):
        _data = self.__stack_data[-1]
        _value = _data[0][1]
        return _value

    def append_local_var(self, var):
        """增加一个局部变量。 """
        _data = self.__stack_data[-1][1]
        _data[var.name] = var

#     def get_global_var(self, name):
#         try:
#             value = self.__global_data[name].forward()
#         except KeyError:
#             raise KeyError(self.__emsg(8001).format(name))
#         else:
#             return value

    def filter_variable_dict(self, data):
        """对变量字典进行过滤和转换，返回符合要求的变量和值。

        过滤条件如下：
        
          所有以下划线开头的变量会被过滤；
        
          所有类型不是 aftype 内定义的变量也会被过滤；
        
          所有的变量名称都转换成为小写。
        
        """
        assert(isinstance(data, dict))
        _new = {}
        for (k, v) in data.iteritems():
            if (isinstance(k, basestring)
                and (k[0] != '_')
                and (k != 'self')
                and issubclass(type(v), aftype.BaseType)
                ):
                _new[k] = v
        return _new

    def set_global_data(self, data):
        """使用传入的参数替换全部的全局变量。 """
        self.__global_data.clear()
        self.__global_data.update(self.filter_variable_dict(data))

    def get_global_data(self):
        return self.__global_data

    def push(self, parent, addr, name, start, data):
        _code = [parent, addr, name, start]
        _data = self.filter_variable_dict(data)
        self.__stack_data.append([_code, _data])

    def pop(self):
        """出栈. """
        try:
            value = self.__stack_data.pop()
        except IndexError:
            raise IndexError(self.__emsg(8002))
        else:
            return value

    def set_local_data(self, data):
        """设置栈顶的局部变量. """
        try:
            _local_data = self.__stack_data[-1][1]
        except IndexError:
            raise IndexError(self.__emsg(8003).format(-1))
        else:
            _local_data.clear()
            _local_data.update(self.filter_variable_dict(data))

    def get_local_data(self, level=-1):
        try:
            return self.__stack_data[level][1]
        except IndexError:
            raise IndexError(self.__emsg(8003).format(level))

    def __emsg(self, ecode):
        """返回错误代码对应的消息格式字符串 """
        # 代码：8000
        # 参数：
        # 描述：保留
        #
        if ecode == 8000:
            return ""

        # 代码：8001
        # 参数：（变量名称）
        # 描述：不存在的全局变量的名称
        #
        if ecode == 8001:
            return _("There is no '{0}' in the global data")

        # 代码：8002
        # 参数：
        # 描述：不能对空栈进行弹出操作
        #
        if ecode == 8002:
            return _("can not pop on an empty stack")

        # 代码：8003
        # 参数：堆栈层数
        # 描述：堆栈溢出
        #
        if ecode == 8003:
            return _("stack overflows in the level of '{0}'")

        # 代码：8004
        # 参数：堆栈层数，变量名称
        # 描述：不存在的局部变量的名称
        #
        if ecode == 8004:
            return _("There is no '{1}' in the stack data of level '{0}'")


        # 未知的错误代码
        assert False, "unknown error code %d" % ecode


if __name__ == "__main__":
    import gettext
    gettext.NullTranslations().install()

    _obj = CodeEntity()
    _obj.load_from_file("data/test.paf")
    _paraxml = _obj.get_configure_string()
    _ua = unicode("中国".decode('gb2312'))
    print _ua.encode('gb2312')

    if _ua == "x" or "x" == _ua:
        print "OK"

