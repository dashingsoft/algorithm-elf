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
 * @文件：dsmemory.py
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

import Tkinter
import Tix
import tkFont

import aftype

class MemoryView(Tkinter.Toplevel):
    """内存数据视图，用于显示执行过程中的内存数据。

    Tag 的使用规范：
    
        全局堆  整体内容 tag = '_g_'
                标题样式 tag = '_gt_'
    
        局部堆  整体内容 tag = 堆栈的层数，从 0 开始
                标题样式 tag = '_lt_'
    
        简单变量名称样式使用两个 tag：_ct0_, _ct1_
    
        变量值样式格式也有两个 tag：_v0_, _v1_
    
        用于显示的时候不同行之间交替使用不同样式。
    
        组合数据类型名称样式使用 tag: _r_ _x_
    
        简单变量类型是指数值、字符串、指针等，组合数据类型是
        指主要是数组和结构
    
    
        变量值对应的 tag = id(frame) 下划线 变量名称，这个
        tag 是唯一的。
    
        变量更新之后文本的样式控制 tag: _s_
    
    """
    def __init__(self, master=None):
        Tkinter.Toplevel.__init__(self, master)
        self.withdraw()
        self.title(_("Memory View"))
        self.geometry("+0-0")

        self.__level = 0
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

    def initialize(self, data):
        """初始化全局变量。 """
        self.clear()
        self.__draw_global_node(data)

    def clear(self):
        """清空视图的实体数据和控件. """
        self.__text_canvas.delete("1.0", Tkinter.END)
        self.__level = 0

        # 增加全局堆
        self.__draw_global_node()
        
    def push(self, caller, addr, funcname, data):
        self.__show_time_indicator_at_stack_bottom()        
        self.__draw_heap_node(caller, addr, funcname, data)
        self.__level += 1
        self.__show_time_indicator_at_stack_bottom()
        
    def pop(self):
        self.__show_time_indicator_at_stack_bottom()
        self.__level -= 1
        
        _ranges = list(self.__text_canvas.tag_ranges(str(self.__level)))
        for i in range(0, len(_ranges), 2):
            self.__text_canvas.delete(_ranges[i], _ranges[i + 1])

        self.__show_time_indicator_at_stack_bottom()

    def append_local_var(self, var):
        """用于追加局部变量。"""
        _start = self.__text_canvas.index(Tkinter.END + " -1c")
        _tag = str(self.__level - 1)

        _index = self.__text_canvas.index(Tkinter.END + " -2c")
        _tagnames = self.__text_canvas.tag_names(_index)
        if "_v0_" in _tagnames:
            i = 1
        else:
            i = 0

        varname = var.name
        if issubclass(type(var), aftype.Struct):
            self.__draw_complex_var(varname, var)
        else:
            self.__draw_simple_var(varname, var, i)

        self.__text_canvas.tag_add(_tag, _start, Tkinter.END + " -1c")
        self.__text_canvas.see(Tkinter.END)

    def update(self, var):
        """修改内存变量的值。

        注意可能存在多个变量的值相同，因为存在变量参数的传递；
        """
        _tag = var.tagid
        _range = self.__text_canvas.tag_ranges(_tag)
        if len(_range) == 0:
            raise Exception(_("There is no variable '{0}' found").format(var.name))

        # 更新变量值
        for i in range(0, len(_range), 2):
            _index = self.__text_canvas.index(str(_range[i + 1]) + " -2c")
            self.__text_canvas.insert(_index, u" " + unicode(var))
            self.__text_canvas.delete(_range[i], _index)

            # 标识变化的部分
            self.__text_canvas.tag_remove("_s_", "1.0", Tkinter.END)
            self.__text_canvas.tag_add("_s_", _range[i], _range[i + 1])
            self.__text_canvas.tag_raise("_s_")
            self.__text_canvas.see(_range[i])

            # 显示时间指针
            self.__show_time_indicator(_range[i])
        
    def new(self, obj):
        assert(issubclass(type(obj), aftype.BaseType))
        _index = self.__text_canvas.index("_g_.last -2c")        
        if "_v0_" in self.__text_canvas.tag_names(_index):
            i = 1
        else:
            i = 0
            
        self.__text_canvas.mark_set(Tkinter.INSERT, "_g_.last -1c")
        if issubclass(type(obj), aftype.Struct):
            self.__draw_complex_var(obj.name, obj)
        else:
            self.__draw_simple_var(unicode(id(obj)), obj, tag=i)
        # 显示时间指针
        self.__show_time_indicator(Tkinter.INSERT)

    def dispose(self, obj):
        assert issubclass(type(obj), aftype.BaseType), type(var)
        _tag = obj.tagid
        _range = self.__text_canvas.tag_ranges(_tag)
        if len(_range) < 1:
            raise Exception(_("There is no variable '{0}' found").format(obj.name))
        _start = self.__text_canvas.index(str(_range[0]) + " linestart")
        _end = self.__text_canvas.index(str(_range[1]) + " lineend")

        # 显示时间指针
        self.__show_time_indicator(_start)
        self.__text_canvas.delete(_start, _end)
        self.__text_canvas.tag_delete(_tag)
                                        
    def __show_time_indicator_at_stack_bottom(self):
        _index = self.__text_canvas.index(Tkinter.END + " - 1 lines")
        self.__show_time_indicator(_index)
        
    def __show_time_indicator(self, index):
        self.__text_canvas.see(index)
        _x = self.__text_canvas.winfo_x()
        _y = self.__text_canvas.winfo_y()
        _box = self.__text_canvas.bbox(index)
        if _box:
            self.__player.update_time_indicator(
                self,
                _x + _box[0],
                _y + _box[3],
                )

    def __create_widgets(self):
        _scrolltext = Tix.ScrolledText(
                    self,
                    scrollbar="both",
                    width=295,
                    height=295,
                    )
        self.__text_canvas = _scrolltext.subwidget("text")
        _scrolltext.grid(sticky="nesw")

        self.__font = tkFont.Font(
                    self.__text_canvas,
                    self.__text_canvas["font"]
                    )

        # 配置文本的显示样式
        self.__text_canvas.tag_config(
            "_gt_",
            background="#6495ED",
            borderwidth=2,
            relief="groove",
            lmargin1=10,
            rmargin=10,
            )
        self.__text_canvas.tag_config(
            "_g_",
            )
        
        self.__text_canvas.tag_config(
            "_lt_",
            background="#87CEEB",
            borderwidth=2,
            relief="groove",
            lmargin1=10,
            rmargin=20,
            )
        self.__text_canvas.tag_config(
            "_s_",
            background="#FF4500",
            borderwidth=2,
            relief="flat"
            )

        self.__text_canvas.tag_config(
            "_ct0_",
            background="#D3D3D3",
            borderwidth=2,
            relief="groove",
            justify="left",
            )
        self.__text_canvas.tag_config(
            "_ct1_",
            background="gray",
            borderwidth=2,
            relief="groove",
            justify="left",
            )
        self.__text_canvas.tag_config(
            "_v0_",
            background="#E6E6FA",
            borderwidth=2,
            relief="flat",
            lmargin1=10,
            )
        self.__text_canvas.tag_config(
            "_v1_",
            background="#B0C4DE",
            borderwidth=2,
            relief="flat",
            lmargin1=10,
            )
        self.__text_canvas.tag_config(
            "_r_",
            background="#66CDAA",
            borderwidth=2,
            relief="groove",
            justify="left",
            lmargin1=10,
            )

        self.__text_canvas.tag_config(
            "_x_",
            background="#FAFAD2",
            borderwidth=2,
            relief="flat",
            font="weight 10 bold",
            lmargin1=10,
            )

    def __draw_simple_var(self, name, var, tag=0):
        _title = self.__measure(name, 100)
        self.__text_canvas.insert(
            Tkinter.INSERT,
            _title,
            ("_ct%d_" % tag,)
            )
        self.__text_canvas.insert(
            Tkinter.INSERT,
            u" {0} \n".format(unicode(var)),
            (var.tagid, "_v%d_" % tag),
            )

    def __draw_complex_var(self, name, var):
        if issubclass(type(var), aftype.Array):
            _typename = _(" Array ")
            _prefix = u"{0}[{1}]"
        else:
            _typename = _(" Record ")
            _prefix = u"{0}.{1}"

        self.__text_canvas.insert(
            Tkinter.INSERT,
            _typename,
            ("_r_",)
            )
        self.__text_canvas.insert(
            Tkinter.INSERT,
            " " + name + "\n",
            ("_x_",)
            )

        i = 0
        for (k, v) in var.value.iteritems():
            _name = _prefix.format(name, k)
            assert(issubclass(type(v), aftype.BaseType))                
            if issubclass(type(v), aftype.Struct):
                self.__draw_complex_var(_name, v)
            else:
                self.__draw_simple_var(_name, v, tag=i)
                i = (i + 1) % 2
        self.__text_canvas.insert(Tkinter.INSERT, "\n")
        
    def __draw_global_node(self, data={}):
        """显示全局块。 """
        _start = self.__text_canvas.index(Tkinter.END + " -1c")

        self.__text_canvas.insert(
            Tkinter.END,
            _("Global Heap\n"),
            ("_gt_",)
            )        
        self.__draw_data(data)
        self.__text_canvas.insert(Tkinter.END, "\n")
        self.__text_canvas.tag_add("_g_", _start, Tkinter.END + " -1c")
        self.__text_canvas.see(Tkinter.END)

    def __draw_data(self, data):
        i = 0
        self.__text_canvas.mark_set(Tkinter.INSERT, Tkinter.END)
        for (k, v) in data.iteritems():
            if issubclass(type(v), aftype.Struct):
                self.__draw_complex_var(k, v)
            else:
                self.__draw_simple_var(k, v, tag=i)
                i = (i + 1) % 2

    def __draw_heap_node(self, caller, addr, funcname, data):
        """显示一个堆栈块。 """
        _start = self.__text_canvas.index(Tkinter.END + " -1c")
        _tag = str(self.__level)

        _title = u"{0} : {1} -> {2} ".format(caller, addr, funcname)
        self.__text_canvas.insert(Tkinter.END, _title, ("_lt_",))
        self.__text_canvas.insert(Tkinter.END, "\n")

        self.__draw_data(data)

        self.__text_canvas.tag_add(_tag, _start, Tkinter.END + " -1c")
        self.__text_canvas.see(Tkinter.END)

    def __measure(self, name, width):
        """使用空格填充 name ，使得其长度正好占用 width 个像素。 """
        _spacewidth = self.__font.measure(" ")
        _textwidth = self.__font.measure(name)
        _margin = width  - _textwidth - _spacewidth
        if _margin > 0:
            name = u" " + name + u" " * (_margin / _spacewidth)
        return name


if __name__ == "__main__":
    import gettext
    gettext.NullTranslations().install()

    root = Tix.Tk()
    _view = MemoryView(root)
    _view.initialize({"a":1})
    _view.deiconify()
    root.mainloop()

