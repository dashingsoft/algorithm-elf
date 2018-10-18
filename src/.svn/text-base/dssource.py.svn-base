
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
 * @文件：dssource.py
 *
 * @作者：赵俊德(jondy.zhao@gmail.com)
 *
 * @创建日期: 2010/02/24
 *
 * @文件说明：
 *
 *   代码视图，用于显示执行过程中的代码。
 *   以及查看局部变量的值。
"""

import Tkinter
import Tix
import re


class CodeView(Tkinter.Frame):
    """代码视图，用于显示执行过程中的代码。

类内部属性

    data, 字典类型，用于存放当前代码的局部数据

    对data 赋值由 AlgorithmDriver 中控制，在每一次模拟语句执
    行之前该值都会被更新，保证始终是最新的数据。
    
    data 主要用于显示当前局部变量的值。
    
    """
    
    def __init__(self, master=None, player=None):
        Tkinter.Frame.__init__(self, master)
        self.__player = player

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.data = {}
        self.__create_widgets()

    def initialize(self, sourcelist, data={}):
        """初始化源代码视图视图中的数据。

这是主函数被调用时候的初始化方法。

"""
        self.clear()        
        self.data.update(data)

        self.__text_source.config(state='normal')
        i = 1
        for line in sourcelist:
            self.__text_source.insert(
                Tkinter.END,
                "{0:3}: {1}\n".format(i, line)
                )
            i += 1
        self.__text_source.tag_add("b", "1.0", Tkinter.END)
        self.__text_source.tag_config("b", lmargin2=40)
        self.__text_source.config(state='disabled')

    def clear(self):
        """清空视图的实体数据和控件。 """
        self.__text_source.config(state='normal')
        self.__text_source.delete("1.0", Tkinter.END)
        self.__text_source.config(state='disabled')

        self.data.clear()

    def __create_widgets(self):
        self.__scrolltext_source = Tix.ScrolledText(
            self,
            scrollbar="both",
            width=300,
            height=300,
            )
        self.__text_source = self.__scrolltext_source.subwidget("text")
        self.__text_source.config(
            state='disabled',
            spacing1=2,
            )
        self.__scrolltext_source.grid(
            sticky="nesw"
            )

        self.__text_source.tag_config(
                    "a",
                    background="#4169E1",
                    borderwidth=3,
                    relief="raised",
                    rmargin=10,
                    )

        # 下面是两种气球方案，一个是Tix.Balloon，一个是自定义
        self.__balloon = Tix.Balloon(
            self.__text_source,
            state='balloon',
            )
        self.__text_source.bind('<Motion>', self.__show_balloon)

#         self.__balloon1 = Tkinter.Toplevel(
#             self.__text_source,
#             class_="Balloon",
#             borderwidth=2,
#             background="#FFFF00",
#             )
#         self.__balloon1.withdraw()
#         self.__balloon1.minsize(width=100,height=50)
#         self.__balloon1.update_idletasks()
#         self.__balloon1.overrideredirect(True)
#         self.__balloon1.message = Tkinter.Label(self.__balloon1)
#         self.__balloon1.message.grid(sticky="nesw")

#         self.__text_source.bind("<Motion>", lambda e:self.__balloon1.withdraw())
#         self.__text_source.bind("<Button-1>", self.__show_balloon1)

#     def __show_balloon1(self, event):
#         if self.__player is not None:
#             if self.__player.is_playing():
#                 return
#         _msg = self.__get_variable(event.x, event.y)
        
#         if _msg is not None:        
#             self.__balloon1.geometry("+%d+%d" % (event.x_root + 16, event.y_root + 16))
#             self.__balloon1.message["text"] = _msg
#             self.__balloon1.deiconify()
#             self.__balloon1.transient()


    def __get_variable(self, x=0, y=0):
        index = self.__text_source.index(
            "@%s,%s" % (x, y)
            )
        linetext = self.__text_source.get(
            index + ' wordstart',
            index + ' lineend'
            )
        # 得到变量名称
        m = re.match(r"^[a-zA-Z][a-zA-Z0-9_]*", linetext)
        if m is None:
            varname = ""
        else:
            varname = m.group(0)

        # 从当前数据堆栈中得到变量值
        value = self.data.get(varname.lower(), None)
        if value is None:
            return ""
        else:
            return "{0} =\n{1}".format(varname, value)

    def __show_balloon(self, event):
        if self.__player is not None:
            if self.__player.is_playing():
                return
        _msg = self.__get_variable(event.x, event.y)

        if _msg != "":
            self.__balloon.bind_widget(
                self.__text_source,
                balloonmsg=_msg
                )
            # 模拟离开事件，可以使得气球消失重新显示
            if self.__balloon.winfo_viewable():
                self.__text_source.event_generate("<Leave>")
                
    def show_pointer(self, lineno):
        """高亮显示当前正在执行的代码行. """
        self.__text_source.config(state='normal')
        _count = lineno
        _start = self.__text_source.search(
            "^[[:space:]]*" + str(lineno) + ":",
            "1.0",
            regexp=True
            )
        if _start != "":
            _end = self.__text_source.index(_start + " lineend +1c")
            self.hide_pointer()
            self.__text_source.tag_add(
                "a",
                _start,
                _end
                )

            # 显示时间指针
            self.__text_source.see(_start)
            _x = self.__scrolltext_source.winfo_x()
            _y = self.__scrolltext_source.winfo_y()
            _box = self.__text_source.bbox(
                self.__text_source.index(_start + " +3c")
                )
            if _box is not None:
                self.__player.update_time_indicator(
                    self,
                    x=_x + _box[0],
                    y=_y + _box[1] + _box[3]
                    )
        self.__text_source.config(state='disabled')

    def hide_pointer(self):
        self.__text_source.config(state='normal')
        r = self.__text_source.tag_ranges("a")
        if len(r) > 1:
            self.__text_source.tag_remove("a", r[-2], r[-1])          
        self.__text_source.config(state='disabled')

    def __emsg(self, ecode):
        """ 返回错误代码对应的消息格式字符串 """
        # 代码：9000
        # 参数：
        # 描述：
        #
        if ecode == 9000:
            return ""

        # 代码：9001
        # 参数：局部变量名称
        # 描述：没有发现局部变量
        #
        if ecode == 9001:
            return _("There is no variable '{0}' found")

        # 代码：9002
        # 参数：参数，参数类型
        # 描述：初始化实体的时候需要一个 dsStackEntity 的类型
        #
        if ecode == 9002:
            return _("A dsStackEntity is expected when initialize "
                     " the code view, the type of '{0}' is '{1}'")

        # 未知的错误代码
        assert False, "unknown error code %d" % ecode


if __name__ == '__main__':
    import gettext
    gettext.NullTranslations().install()

    root = Tix.Tk()
    _view = CodeView(root)
    _view.grid(sticky="nesw")
    root.mainloop()


