# -*- coding: utf-8 -*-
#
#############################################################
#                                                           #
#      版权所有 2009 - 2010 德新软件公司。保留全部权利。    #
#                                                           #
#      数据结构算法助手                                     #
#                                                           #
#      版本区间：1.1.0 -                                    #
#                                                           #
#############################################################

"""
 * @文件：dsstack.py
 *
 * @作者：赵俊德(jondy.zhao@gmail.com)
 *
 * @日期：2010/02/24
 *
 * @文件说明：
 *
 *      堆栈视图，用于显示执行过程中的堆栈状态。
 *
"""

import re
import Tkinter
import Tix


class StackView(Tkinter.Toplevel):
    """调用堆栈视图，用于显示执行过程中的代码执行序列。

    内部属性：

    __level，当前层数。初始值为 0
    __counter, 行计算器。初始值为 0
    __line_context，记录了每一行对应的数据字典
    __list_position，列表，记录每一层调用开始的行号
    __level_indent, 列表，记录每一层的缩进
    __indent，当前缩进的空格数

    Tag 的使用规范：
        每一层的调用框架使用一个整体 tag: t + 层数，例如
            t0, t1, t2
        每一层又分为两部分，第一行是头部，使用 tag: tX_h
        其他部分是主体，使用 tag: tX_b

    """
    def __init__(self, master=None):
        Tkinter.Toplevel.__init__(self, master)
        self.withdraw()
        self.title(_("Stack View"))
        self.geometry("-0-0")

        self.__level = 0
        self.__counter = 0
        self.__line_context = []
        self.__list_position = []
        self.__level_indent = []
        self.__indent = 0

        self.__player = master

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.__create_widgets()

        self.protocol(
            'WM_DELETE_WINDOW',
            lambda :self.hide()
            )

    def toggle(self):
        if self.winfo_viewable():
            self.hide()
        else:
            self.show()

    def show(self):
        self.deiconify()
        self.transient(self.__player)

    def hide(self):
        self.withdraw()

    def clear(self):
        """清空视图的实体数据和控件。"""
        self.__text_stack.delete("1.0", Tkinter.END)

        self.__level = 0
        self.__counter = 0
        self.__indent = 0
        del self.__line_context[:]
        del self.__list_position[:]
        del self.__level_indent[:]

    def push(self, funcname, data):
        self.__level_indent.append(self.__indent)
        self.__counter += 1

        # 搜索当前行的第一个非空字符
        index = self.__text_stack.search(
            "[^[:space:]]",
            "%d.0" % self.__counter,
            regexp=True,
            )
        if index == "":
            self.__indent = 4 * self.__level
        else:
            self.__indent = int(index.split(".")[1]) + 1 + 2


        paras = [u"%s=%s" % (k, v) for (k, v) in data.iteritems()]
        _tag = "t%d_h" % self.__level
        _title = u"\n{0:>{1}} {2}{3}".format(
            "|->",
            self.__indent,
            funcname,
            paras
            )
        self.__text_stack.insert(Tkinter.END, _title, (_tag,))

        _data = dict([ [k, unicode(v)] for (k, v) in data.iteritems()])
        self.__line_context.append(_data)
        self.__list_position.append(self.__counter)
        self.__level += 1
        self.__text_stack.see(Tkinter.END)

    def pop(self):
        _start = self.__list_position.pop()
        _end = self.__text_stack.index(Tkinter.END)
        self.__text_stack.tag_add(
            "t%d" % self.__level,
            "%d.0" % _start,
            _end
            )
        self.__text_stack.tag_add(
            "t%d_b" % self.__level,
            "%d.0" % (_start + 1),
            _end
            )
        self.__level -= 1
        self.__indent = self.__level_indent.pop()

    def append(self, code, data):
        """在视图中追加一行。

主要进行的操作：

   1. 递增行号，也可能是多行

   2. 根据调用层数计算缩进，显示代码

   3. 追加数据到行数据字典中。这个数据主要用于显示变量的数据。

        """
        _indent = self.__indent

        if isinstance(code, basestring):
            _lines = code.split("\n")
        else:
            _lines = code

        self.__counter += 1
        self.__text_stack.insert(
            Tkinter.END,
            u"\n{0:>{1}}{2}".format(" ", _indent, _lines[0])
            )

        _data = dict([ [k, unicode(v)] for (k, v) in data.iteritems()])
        self.__line_context.append(_data)

        for _rest in _lines[1:]:
            self.__counter += 1
            self.__text_stack.insert(
                Tkinter.END,
                u"\n{0:>{1}}{2}".format("|", _indent, _rest)
                )
            self.__line_context.append(None)
        self.__text_stack.see(Tkinter.END)

    def __create_widgets(self):
        _scrolltext = Tix.ScrolledText(
                    self,
                    scrollbar="both",
                    width=600,
                    height=400,
                    )
        self.__text_stack = _scrolltext.subwidget("text")
        self.__text_stack.configure(
            wrap="none",
            spacing1=2,
            )
        _scrolltext.grid(sticky="nesw")

        self.__balloon = Tix.Balloon(
            self.__text_stack,
            state='balloon',
            )
        self.__text_stack.bind(
            '<Motion>',
            self.__show_variable
            )

    def __get_variable(self, x, y):
        index = self.__text_stack.index(
            "@%s,%s" % (x, y)
            )
        linetext = self.__text_stack.get(
            index + ' wordstart',
            index + ' lineend'
            )
        # 得到变量名称
        m = re.match(r"^[a-zA-Z][a-zA-Z0-9_]*", linetext)
        if m is None:
            return ""
        else:
            name = m.group(0)

        # 查找当前行的数据字典
        try:
            i = int(index.split(".")[0])
            _data = self.__line_context[i]
            while len(_data) == 0:
                i -= 1
                _data = self.__line_context[i]
        except Exception:
            _data = {}

        # 从当前行的数据字典中得到变量值
        value = _data.get(name.lower(), "")
        return u"{0} =\n{1}".format(name, value)

    def __show_variable(self, event):
        if self.__player is not None:
            if self.__player.is_playing():
                return

        _msg = self.__get_variable(event.x, event.y)

        if _msg != "":
            self.__balloon.bind_widget(
                self.__text_stack,
                balloonmsg=_msg
                )
            # 模拟离开事件，可以使得气球消失重新显示
            if self.__balloon.winfo_viewable():
                self.__text_stack.event_generate("<Leave>")


if __name__ == "__main__":
    pass
