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
#
# @文件：dssetting.py
#
# @作者：赵俊德(jondy.zhao@gmail.com)
#
# @创建日期: 2010/03/04
#
# @文件说明：
#
#     算法参数设置对话框。
#

import os
import Tkinter
import Tix

class SettingDialog(object):
    """算法参数设置对话框。

    参数基本信息：名称，类型，值。

    只有值可以被修改，名称和类型和算法主函数一致，不能在这里修改。

    每一个参数都有其选项值，控制其显示方式：

        visible,  Fasle

        width,    0 表示自动设定合适宽度

        height,   0 表示自动设定合适高度

        shape,    oval

        watch,

    和结构体相关的有：

        orientation，孩子是水平还是垂直放置 horizontal

        padx,pady 水平和垂直填充像素 2

        xincrement, yincrement, 水平或者垂直填充增量 0

        anchor, 孩子的锚点；nw

        size，针对数组结构，说明数组的大小。这个选项只是用于
        生成数组时候自动生成指定大小的数组，在其他地方可以直
        接根据值得到数组的大小，不需要使用这个值；

        anonymous，匿名孩子结点，也就是说不会显示孩子标题。False

    内部属性说明：

        self.widget,  Toplevel 类型，顶层窗口。

        self.configure, 指向 AlgorithmDriver 中的 algorithm_configure

        self.__frame, 复合结构命令工具栏，譬如树的新增左孩子、右孩子等按钮

        self.__canvas, 显示可见对象的画布

        self.var_values，以变量名称为关键字的字典，使用 StringVar 跟踪变量值的变化

        self.var_options, 以变量名称为关键字的字典，是变量配置信息的一份拷贝

        self.__apply 标识是否进行了保存

    """
    def __init__(self, master, configure):
        """初始化参数。

        参数 configure 的格式：

        {'vars': [...], 'options: {...}}
        
        """
        self.master = master
        self.widget = Tkinter.Toplevel(master)
        self.widget.title(_("Parameter Setting"))
        self.widget.resizable(False, False)
        self.widget.geometry("+100+50")

        self.configure = configure
        self.vars = self.configure["vars"][:]

        self.__create_widgets()
        self.widget.protocol('WM_DELETE_WINDOW', self.widget.quit)
        self.__apply = False

    def __create_widgets(self):
        self.__paraframe = Tkinter.Frame(
            self.widget,
            borderwidth=2,
            relief="groove",
            )
        self.__paraframe.grid(sticky="nsw")
        _label = Tkinter.Label(
            self.__paraframe,
            text=_("Parameters"),
            anchor="nw",
            width=50,
            )
        _label.grid(sticky="wen")
        self.__initialize_paras()

        _frame = Tkinter.Frame(
            self.widget,
            borderwidth=2,
            relief="groove",
            )
        _frame.grid(row=0, column=1, sticky="nesw")
        self.__frame = Tkinter.Frame(_frame)
        self.__canvas = Tkinter.Canvas(
            _frame,
            width=400,
            height=550,
            highlightthickness=0,
            )
        self.__canvas.grid(row=1, column=0, sticky="nesw")

        # 命令栏
        _frame = Tkinter.Frame(
            self.widget,
            padx=30,
            pady=10,
            borderwidth=0,
            relief="groove",
            )
        _frame.grid(row=1, column=0, columnspan=2, )

        _button = Tkinter.Button(
            _frame,
            text=_("Add"),
            overrelief="groove",
            command=self.__action_add,
            width=8,
            )
        _button.grid(row=0, column=0, padx=20, sticky="e")

        _button = Tkinter.Button(
            _frame,
            text=_("Remove"),
            overrelief="groove",
            command=self.__action_remove,
            width=8,
            )
        _button.grid(row=0, column=1, padx=20, sticky="e")

        _button = Tkinter.Button(
            _frame,
            text=_("Apply"),
            overrelief="groove",
            command=self.__action_apply,
            width=8,
            )
        _button.grid(row=0, column=2, padx=20, sticky="e")

        _button = Tkinter.Button(
            _frame,
            text=_("Cancel"),
            overrelief="groove",
            command=self.widget.quit,
            width=8,
            )
        _button.grid(row=0, column=3, padx=20, sticky="e")
        self.__create_property_window()

        self.__control_index["max"] = len(self.vars) - 1
        
        self.__var_visible.trace_variable("w", self.__change_option_value)
        self.__var_width.trace_variable("w", self.__change_option_value)
        self.__var_height.trace_variable("w", self.__change_option_value)
        self.__var_orientation.trace_variable("w", self.__change_option_value)
        self.__var_padx.trace_variable("w", self.__change_option_value)
        self.__var_xincrement.trace_variable("w", self.__change_option_value)
        self.__var_pady.trace_variable("w", self.__change_option_value)
        self.__var_yincrement.trace_variable("w", self.__change_option_value)
        self.__var_shape.trace_variable("w", self.__change_option_value)
        self.__var_anchor.trace_variable("w", self.__change_option_value)
        self.__var_watch.trace_variable("w", self.__change_option_value)
        self.__var_anonymous.trace_variable("w", self.__change_option_value)

        self.__var_size.trace_variable("w", self.__change_array_size)
        self.__var_index.trace_variable("w", self.__change_var_index)

    def __create_property_window(self):
        self.__property = Tkinter.Toplevel(self.widget)
        self.__property.title(_("Properties"))
        self.__property.resizable(False, False)
        self.__property.protocol('WM_DELETE_WINDOW', False)
        _frame = Tkinter.Frame(self.__property)
        _frame.grid(pady=2)

        _soptions = ("label.width 15 label.anchor e "
                     "menubutton.width 15 menubutton.relief groove ")
        _coptions = ("label.width 16 label.anchor e "
                     "entry.width 20 entry.relief groove "
                     "decr.relief flat incr.relief flat ")
        _eoptions = ("label.width 16 label.anchor e "
                     "entry.width 20 entry.relief groove ")

        self.__var_index = Tkinter.IntVar()
        _w = Tix.Control(
            _frame,
            label=_("Index") + " : ",
            integer=1,
            variable=self.__var_index,
            min=0,
            max=100,
            options=_coptions,
            )
        _w.grid(sticky="wen")
        self.__control_index = _w

        self.__var_name = Tkinter.StringVar()
        _w = Tix.LabelEntry(
            _frame,
            label=_("Name") + " : ",
            options=_eoptions,
            )
        _w.subwidget("entry").config(
            textvariable=self.__var_name,
            state="disabled",
            )
        self.__var_name.set("")
        _w.grid(ipady=2, sticky="wen")

        self.__var_type = Tkinter.StringVar()
        _w = Tix.LabelEntry(
            _frame,
            label=_("Type") + " : ",
            options=_eoptions,
            )
        _w.subwidget("entry").config(
            textvariable=self.__var_type,
            state="disabled",
            )
        _w.grid(ipady=2, sticky="wen")

        _option_list = ("True", "False")
        self.__var_visible = Tkinter.StringVar()
        _w = Tix.OptionMenu(
            _frame,
            label=_("Visible") + " :",
            variable=self.__var_visible,
            options=_soptions,
            )
        for _opt in _option_list:
            _w.add_command(_opt, label=_opt)
        self.__var_visible.set(_option_list[0])
        _w.grid(sticky="wen")

        self.__var_width = Tkinter.IntVar()
        self.__var_width.set(40)
        _w = Tix.Control(
            _frame,
            label=_("Width") + " : ",
            integer=1,
            variable=self.__var_width,
            min=40,
            max=1024,
            options=_coptions,
            )
        _w.grid(sticky="wen")

        self.__var_height = Tkinter.IntVar()
        self.__var_height.set(40)
        _w = Tix.Control(
            _frame,
            label=_("Heigth") + " : ",
            integer=1,
            variable=self.__var_height,
            min=40,
            max=1024,
            options=_coptions,
            )
        _w.grid(sticky="wen")

        _option_list = ("oval", "renctangle")
        self.__var_shape = Tkinter.StringVar()
        _w = Tix.OptionMenu(
            _frame,
            label=_("Shape") + " :",
            variable=self.__var_shape,
            options=_soptions,
            )
        for _opt in _option_list:
            _w.add_command(_opt, label=_opt)
        self.__var_shape.set(_option_list[0])
        _w.grid(sticky="wen")

        _option_list = self.__available_var_list(-1)
        self.__var_watch = Tkinter.StringVar()
        _w = Tix.OptionMenu(
            _frame,
            label=_("Watch") + " :",
            variable=self.__var_watch,
            options=_soptions,
            )
        for _opt in _option_list:
            _w.add_command(_opt, label=_opt)
        self.__var_watch.set(_option_list[0])
        _w.grid(sticky="wen")

        _option_list = ("horizontal", "vertical")
        self.__var_orientation = Tkinter.StringVar()
        _w = Tix.OptionMenu(
            _frame,
            label=_("Orientation") + " :",
            variable=self.__var_orientation,
            options=_soptions,
            )
        for _opt in _option_list:
            _w.add_command(_opt, label=_opt)
        self.__var_orientation.set(_option_list[0])
        _w.grid(sticky="wen")

        _option_list = ("n", "ne", "e", "se", "s", "sw", "w", "nw", "center")
        self.__var_anchor = Tkinter.StringVar()
        _w = Tix.OptionMenu(
            _frame,
            label=_("Anchor") + " :",
            variable=self.__var_anchor,
            options=_soptions,
            )
        for _opt in _option_list:
            _w.add_command(_opt, label=_opt)
        self.__var_anchor.set(_option_list[0])
        _w.grid(sticky="wen")

        self.__var_padx = Tkinter.IntVar()
        _w = Tix.Control(
            _frame,
            label=_("Padx") + " : ",
            integer=1,
            variable=self.__var_padx,
            min=0,
            max=100,
            options=_coptions,
            )
        _w.grid(sticky="wen")

        self.__var_pady = Tkinter.IntVar()
        _w = Tix.Control(
            _frame,
            label=_("Pady") + " : ",
            integer=1,
            variable=self.__var_pady,
            min=0,
            max=100,
            options=_coptions,
            )
        _w.grid(sticky="wen")

        self.__var_xincrement = Tkinter.IntVar()
        _w = Tix.Control(
            _frame,
            label=_("Xincrement") + " : ",
            integer=1,
            variable=self.__var_xincrement,
            min=-100,
            max=100,
            options=_coptions,
            )
        _w.grid(sticky="wen")

        self.__var_yincrement = Tkinter.IntVar()
        _w = Tix.Control(
            _frame,
            label=_("Yincrement") + " : ",
            integer=1,
            variable=self.__var_yincrement,
            min=-100,
            max=100,
            options=_coptions,
            )
        _w.grid(sticky="wen")

        self.__var_size = Tkinter.IntVar()
        _w = Tix.Control(
            _frame,
            label=_("Size") + " : ",
            integer=1,
            variable=self.__var_size,
            min=0,
            max=100,
            options=_coptions,
            )
        _w.grid(sticky="wen")

        _option_list = ("True", "False")
        self.__var_anonymous = Tkinter.StringVar()
        _w = Tix.OptionMenu(
            _frame,
            label=_("Anonymous") + " :",
            variable=self.__var_anonymous,
            options=_soptions,
            )
        for _opt in _option_list:
            _w.add_command(_opt, label=_opt)
        self.__var_anonymous.set(_option_list[0])
        _w.grid(sticky="wen")

        self.widget.update_idletasks()
        x = self.widget.winfo_rootx() + 550
        y = self.widget.winfo_rooty() + 100
        self.__property.geometry("+%d+%d" % (x, y))
        self.widget.update_idletasks()
        self.__property.transient(self.widget)

    def __initialize_paras(self):
        self.var_values = []
        self.var_options = {}

        for (name, v) in self.vars:
            self.__append_paras(name, v)
        
    def __append_paras(self, name, v):

        self.var_options[name] = v[2].copy()
        _var = Tkinter.StringVar()
        self.var_values.append(_var)
        _type = v[0]

        _w = self.__show_paras(name, _type, _var)

        _var.set(v[1])
        _var.trace("w", self.__change_parameter_value)
        _w.bind("<FocusIn>", self.__enter_parameter)
        _w.focus_set()

    def __show_paras(self, name, typename, var):
        _soptions = ("label.width 15 label.anchor w "
                     "menubutton.width 15 menubutton.relief groove ")
        _coptions = ("label.width 16 label.anchor w "
                     "entry.width 20 entry.relief groove "
                     "decr.relief flat incr.relief flat ")
        _eoptions = ("label.width 16 label.anchor w "
                     "entry.width 20 entry.relief groove ")        
        _type = typename
        if _type == "Integer":
            _w = Tix.Control(
                self.__paraframe,
                name=name.lower(),
                label=name,
                variable=var,
                options=_coptions,
                )
            _w.grid(sticky="wen")

        elif _type == "Boolean":
            _w = Tix.OptionMenu(
                self.__paraframe,
                name=name.lower(),
                label=name,
                variable=var,
                options=_soptions,
                )
            _w.add_command("True", label="True")
            _w.add_command("False", label="False")
            _w.grid(sticky="wen")

        elif _type == "Pointer":
            _w = Tix.OptionMenu(
                self.__paraframe,
                name=name.lower(),
                label=name,                
                options=_soptions,
                )
            _index = self.__index_of_var(name)
            _option_list = self.__available_var_list(_index)
            for _opt in _option_list:
                _w.add_command(_opt, label=_opt)
            _w.configure(variable=var)
            _w.grid(sticky="wen")

        else:
            _w = Tix.LabelEntry(
                self.__paraframe,
                name=name.lower(),
                label=name,
                options=_eoptions,
                )
            _entry = _w.subwidget("entry")
            _entry.configure(textvariable=var)
            if _type in ("Array", "Record", "Tree"):
                _entry.config(
                    state="readonly",
                    )
            _w.grid(ipady=2, sticky="wen")
        return _w
        
    def __change_option_value(self, v, i, m):
        _name = self.__var_name.get()
        if _name == "": return

        self.__save_options()
        self.__show_variable()

    def __change_parameter_value(self, v, i, m):
        _name = self.__var_name.get()
        if _name == "":
            return

        _type = self.__var_type.get()
        if _type in ("Array", "Record", "Tree"):
            return

        self.__show_variable()
        
    def __change_var_index(self, v, i, m):
        _name = self.__var_name.get()
        if _name == "": return

        _index = self.__index_of_var(_name)
        _newindex = self.__var_index.get()
        if _index == _newindex: return

        assert(_newindex < len(self.vars))
        if _index < _newindex:
            self.vars.insert(_newindex + 1, self.vars[_index])
            self.var_values.insert(_newindex + 1, self.var_values[_index])
            del self.vars[_index]
            del self.var_values[_index]
        else:
            self.vars.insert(_newindex, self.vars[_index])
            self.var_values.insert(_newindex, self.var_values[_index])
            del self.vars[_index + 1]
            del self.var_values[_index + 1]

        for i in range(len(self.vars)):
            k = self.vars[i][0]
            v = self.vars[i][1]
            _w = self.__paraframe.nametowidget(k)
            if _w:
                _w.grid(row=i, column=0)
            
    def __change_array_size(self, v, i, m):
        _name = self.__var_name.get()
        if _name == "": return
        _type = self.__var_type.get()
        if _type == "Array":
            _index = self.__index_of_var(_name)
            _data = eval(self.var_values[_index].get(), {}, {})
            assert(isinstance(_data, dict))
            _size = self.__var_size.get()
            _x = dict([ (str(i), "None") for i in range(_size)])
            for i in range(_size, len(_data)):
                del _data[str(i)]
            _x.update(_data)
            self.var_values[_index].set(str(_x))
            self.__show_variable()

    def __enter_parameter(self, event):
        """参数获得输入焦点之后，初始化其各个属性。"""
        _name = event.widget.cget("label")
        self.__var_name.set("")

        _index = self.__index_of_var(_name)
        self.__var_index.set(_index)
        _type = dict(self.vars)[_name][0]
        self.__var_type.set(_type)
        if _type == "Array":            
            _data = eval(self.var_values[_index].get(), self.__variable_context())
            assert(isinstance(_data, dict))
            _size = len(_data)
        else:
            _size = 0
        self.__var_size.set(_size)

        _options = self.var_options[_name]
        self.__var_visible.set(str(_options.get("visible", False)))
        self.__var_width.set(_options.get("width", 40))
        self.__var_height.set(_options.get("height", 40))
        self.__var_shape.set(_options.get("shape", "oval"))
        self.__var_anchor.set(_options.get("anchor", "nw"))
        self.__var_orientation.set(_options.get("orientation", "horizontal"))
        self.__var_padx.set(_options.get("padx", 2))
        self.__var_xincrement.set(_options.get("xincrement", 0))
        self.__var_pady.set(_options.get("pady", 2))
        self.__var_yincrement.set(_options.get("yincrement", 0))
        self.__var_watch.set(_options.get("watch", "None"))
        self.__var_anonymous.set(str(_options.get("anonymous", False)))

        self.__var_name.set(_name)
        self.__show_variable()

    def __index_of_var(self, varname):
         _names = [ k for (k, v) in self.vars]
         return _names.index(varname)

    def __save_options(self):
        """保存当前变量的选项设置。"""
        _name = self.__var_name.get()
        if _name == "": return

        _options = self.var_options[_name]
        _options["visible"] = bool(eval(self.__var_visible.get()))
        _options["width"] = self.__var_width.get()
        _options["height"] = self.__var_height.get()
        _options["shape"] = self.__var_shape.get()
        _options["anchor"] = self.__var_anchor.get()
        _options["orientation"] = self.__var_orientation.get()
        _options["padx"] = self.__var_padx.get()
        _options["xincrement"] = self.__var_xincrement.get()
        _options["pady"] = self.__var_pady.get()
        _options["yincrement"] = self.__var_yincrement.get()
        _options["watch"] = self.__var_watch.get()
        _options["anonymous"] = bool(eval(self.__var_anonymous.get()))

    def __action_add(self):
        _dialog = NewVarDialog(
            self.widget,
            childflag=False,
            namelist=self.__available_var_list(-1)
            )
        _dialog.deiconify()
        _dialog.wait_visibility()
        _dialog.grab_set()
        _dialog.focus_set()
        _dialog.mainloop()
        _name = _dialog.var_name.get()
        _type = _dialog.var_type.get()
        _value = _dialog.var_value.get()
        _dialog.destroy()
        if _type and _name and (_name not in dict(self.vars).keys()):
            _v = [_type, _value, {}]
            self.vars.append([_name, _v])
            self.__append_paras(_name, _v)
            self.__control_index["max"] = len(self.vars) - 1

    def __action_remove(self):
        _name = self.__var_name.get()
        if _name == "": return        
        _index = self.__index_of_var(_name)
        _options = self.vars[_index][1][2]
        if _options.get("fix", False):
            return
        del self.vars[_index]
        del self.var_values[_index]
        del self.var_options[_name]
        self.__control_index["max"] = len(self.vars) - 1
        _w = self.__paraframe.nametowidget(_name.lower())
        if _w:
            _w.destroy()
            for obj in self.__canvas.find_all():
                self.__canvas.delete(obj)
            self.__var_name.set("")

    def __show_variable(self):
        _type = self.__var_type.get()
        _name = self.__var_name.get()
        _index = self.__index_of_var(_name)
        _args = self.var_options[_name].copy()

        for obj in self.__canvas.find_all():
            self.__canvas.delete(obj)

        if _type == "Tree":
            _frame = Tkinter.Frame(self.__canvas)
            _w = Tkinter.Button(
                _frame,
                text=_("Add left child"),
                overrelief="groove",
                command=self.__add_left_child,
                )
            _w.grid(row=0, column=0, padx=10, pady=2)
            _w = Tkinter.Button(
                _frame,
                text=_("Add right child"),
                overrelief="groove",
                command=self.__add_right_child,
                )
            _w.grid(row=0, column=2, padx=10, pady=2)
            _w = Tkinter.Button(
                _frame,
                text=_("Remove child"),
                overrelief="groove",
                command=self.__remove_tree_child,
                )
            _w.grid(row=0, column=1, padx=10, pady=2)
            self.__canvas.create_window(2, 2, window=_frame, anchor="nw")
            self.__draw_tree_var(
                self.__canvas,
                _index,
                x=0,
                y=30,
                **_args
                )

        elif (_type == "Array") or (_type == "Record"):
            _frame = Tkinter.Frame(self.__canvas)
            _w = Tkinter.Button(
                _frame,
                text=_("Add child"),
                overrelief="groove",
                command=self.__add_child,
                )
            _w.grid(row=0, column=0, padx=10, pady=2)
            _w = Tkinter.Button(
                _frame,
                text=_("Remove child"),
                overrelief="groove",
                command=self.__remove_child,
                )
            _w.grid(row=0, column=1, padx=10, pady=2)
            self.__canvas.create_window(0, 0, window=_frame, anchor="nw")
            self.__draw_complex_var(
                self.__canvas,
                _index,
                x=0,
                y=30,
                **_args
                )

        else:
            _localdata = self.__variable_context()
            _text = self.var_values[_index].get()
            _args["anchor"] = "nw"
            self.__draw_simple_var(
                self.__canvas,
                "",
                title=_name,
                text=_text,
                x=10,
                y=10,
                **_args
                )

    def __add_left_child(self):
        self.__add_tree_child("lchild")

    def __add_right_child(self):
        self.__add_tree_child("rchild")

    def __add_tree_child(self, childname):
        _tag = self.__current_node_tag()
        _varname = self.__var_name.get()
        _index = self.__index_of_var(_varname)
        if _tag:
            _data = eval(self.var_values[_index].get(), {}, {})
            assert(isinstance(_data, dict))

            _child = {"value": "", "lchild":{}, "rchild":{}}
            _expr = "%s.update({'%s':%s})" % (_tag, childname, _child)
            eval(_expr)
            self.var_values[_index].set(str(_data))
            self.__show_variable()
        else:
            if self.var_values[_index].get() == "{}":
                self.var_values[_index].set("{'value':''}")
                self.__show_variable()

    def __current_node_tag(self):
        _tags = self.__current_node_tag_list()
        if _tags is None or len(_tags) == 0:
            return ""
        else:
            return _tags[0]

    def __current_node_tag_list(self):
        _w = self.__canvas.focus_get()
        if _w is None:
            return
        _x = _w.winfo_x()
        _y = _w.winfo_y()
        _objs = self.__canvas.find_overlapping(_x, _y, _x, _y)
        if len(_objs) == 0:
            return
        _tags = self.__canvas.gettags(_objs[0])
        return _tags

    def __remove_tree_child(self):
        _tag = self.__current_node_tag()
        if _tag:
            _varname = self.__var_name.get()
            _index = self.__index_of_var(_varname)
            _data = eval(self.var_values[_index].get(), {}, {})
            assert(isinstance(_data, dict))
            _expr = "%s.clear()" % _tag
            eval(_expr)
            self.var_values[_index].set(str(_data))
            self.__show_variable()

    def __add_child(self):
        _varname = self.__var_name.get()
        if _varname == "":
            return
        _index = self.__index_of_var(_varname)
        _namelist = self.__available_var_list(_index)

        _data = eval(self.var_values[_index].get(), {}, {})
        assert(isinstance(_data, dict))
        _dialog = NewVarDialog(self.widget, namelist=_namelist)
        if self.__var_type.get() == "Array":
            _dialog.var_name.set(str(len(_data)))
        _dialog.deiconify()
        _dialog.wait_visibility()
        _dialog.grab_set()
        _dialog.focus_set()
        _dialog.mainloop()
        _name = _dialog.var_name.get()
        _type = _dialog.var_type.get()
        _value = _dialog.var_value.get()
        _dialog.destroy()
        if _type:
            if _type in ("Pointer", "Reference"):
                _data[_name] = [ _value ]
            else:
                _data[_name] = _value
            self.var_values[_index].set(str(_data))
            self.__show_variable()

    def __remove_child(self):
        _tag = self.__current_node_tag()
        if _tag:
            _type = self.__var_type.get()
            _varname = self.__var_name.get()
            _index = self.__index_of_var(_varname)
            _data = eval(self.var_values[_index].get(), {}, {})
            assert(isinstance(_data, dict))
            del _data[_tag]
            self.var_values[_index].set(str(_data))
            self.__show_variable()

    def __draw_simple_var(self, canvas, tags, **args):
        _x = args.get("x", 0)
        _y = args.get("y", 0)
        _width = args.get("width", 40)
        _height = args.get("height",40)
        _title = args.get("title", None)
        _text = args.get("text", None)
        _shape = args.get("shape", "oval")
        _anchor = args.get("anchor", "nw")
        _ipadx = 2
        _ipady = 2

        _title_height = 20

        _fill = args.get("fill", "#6495ED")
        _activefill = args.get("activefill", "#0000FF")

        if _width < 40: _width = 40
        if _height < 40: _height = 40

        assert(_anchor in ("nw", "ne", "sw", "se"))
        if _anchor == "ne": _x -= - _width
        elif _anchor == "sw": _y -= _height
        elif _anchor == "se":
            _x -= _width
            _y -= _height
        if _shape == "oval":
            _func = canvas.create_oval
        else:
            _func = canvas.create_rectangle
        _func(
            _x + _ipadx,
            _y + _ipady,
            _x + _width - _ipadx,
            _y + _height - _ipady,
            fill=_fill,
            activefill=_activefill,
            tags=tags,
            )

        if _text is not None:
            _entry = Tkinter.Entry(
                canvas,
                width=5,
                relief="flat",
                borderwidth=0,
                justify="center",
                bg=_fill,
                )
            _entry.insert(Tkinter.END, _text)
            _entry.bind("<KeyRelease>", self.__change_node)
            _id = canvas.create_window(
                _x + _width / 2,
                _y + _height / 2,
                window=_entry,
                tags=tags,
                )
        if _title is not None:
            canvas.create_text(
                _x + _width / 2,
                _y + _height,
                text=_title,
                anchor="n",
                tags=tags,
                )
            _height += _title_height
        return (_x, _y, _width, _height)

    def __change_node(self, event):
        _type = self.__var_type.get()
        if _type == "Tree":
            self.__change_tree_node()
        elif _type in ("Array", "Record"):
            self.__change_struct_node()
        else:
            _varname = self.__var_name.get()
            _index = self.__index_of_var(_varname)
            _w = self.__canvas.focus_get()
            _text = _w.get()
            self.__var_name.set("")
            self.var_values[_index].set(_text)
            self.__var_name.set(_varname)

    def __change_struct_node(self):
        _tags = self.__current_node_tag_list()
        try:
            _varname = _tags[1]
        except IndexError:
            return
        _index = self.__index_of_var(_varname)
        _data = eval(self.var_values[_index].get(), {}, {})
        assert(isinstance(_data, dict))
        _w = self.__canvas.focus_get()
        _text = _w.get()
        _tag = _tags[0]
        _data[_tag] = _text
        self.var_values[_index].set(str(_data))

    def __change_tree_node(self):
        _tag = self.__current_node_tag()
        _varname = self.__var_name.get()
        _index = self.__index_of_var(_varname)
        if _tag:
            _data = eval(self.var_values[_index].get(), {}, {})
            assert(isinstance(_data, dict))

            _w = self.__canvas.focus_get()
            _title = _w.get()
            _expr = "%s.update({'value':'%s'})" % (_tag, _title)
            eval(_expr)
            self.var_values[_index].set(str(_data))

    def __draw_tree_node(self, canvas, data, tag, x, y, width):
        """画树结点.

        空字典表示树为空。

        """
        if len(data) == 0: return

        _title = data.get("title", None)
        _text = data.get("value", None)
        assert(isinstance(_title, (type(None), basestring)))
        assert(isinstance(_text, (type(None), basestring)))

        _x = x + width / 2
        _y = y
        self.__draw_simple_var(
            canvas,
            tag,
            x=_x - 20,
            y=_y,
            width=40,
            height=40,
            text=_text,
            title=_title,
            )

        _y += 40
        _child = data.get("lchild", {})
        assert(isinstance(_child, dict))
        if _child:
            canvas.create_line(
                _x,
                _y,
                _x - width / 4,
                _y + 40,
                arrow=Tkinter.LAST,
                )
            self.__draw_tree_node(
                canvas,
                _child,
                tag + "['lchild']",
                x,
                y + 80,
                width / 2
                )
        _child = data.get("rchild", {})
        assert(isinstance(_child, dict))
        if _child:
            canvas.create_line(
                _x,
                _y,
                _x + width / 4,
                _y + 40,
                arrow=Tkinter.LAST,
                )
            self.__draw_tree_node(
                canvas,
                _child,
                tag + "['rchild']",
                _x,
                _y + 40,
                width / 2
                )

    def __draw_tree_var(self, canvas, index, **args):
        _locals = self.__variable_context()
        _text = self.var_values[index].get()
        assert(isinstance(_text, basestring) and _text)
        _data = eval(_text, _locals)
        assert(isinstance(_data, dict))
        if len(_data) == 0:
            canvas.create_text(
                2,
                40,
                anchor="nw",
                text=_("Add root node, click Add left child"),
                )

        _anonymous = args.get("anonymous", False)
        _width = args.get("width", 40)
        _height = args.get("height", 40)
        _shape = args.get("shape", "oval")
        _x = args.get("x", 0)
        _y = args.get("y", 0)

        if canvas.winfo_viewable():
            _canvas_width = canvas.winfo_width()
            _canvas_height = canvas.winfo_height()
        else:
            _canvas_width = canvas.winfo_reqwidth()
            _canvas_height = canvas.winfo_reqheight()
        _width = _canvas_width - _x
        _height = _canvas_height - _y
        _region = (_x, _y, _width, _height)
        self.__draw_tree_node(canvas, _data, "_data", _x, _y, _width)
        return _region

    def __draw_complex_var(self, canvas, index, **args):
        """显示一个结构体或者数组。

        结构体的孩子有两种类型：

        一是简单变量，一是结构体。

        两种类型都需要增加下列标签：

        tags = ( key, varname, 'tag_%s' % key)

        其中前面两个用来修改变量的值，后面用来定位和移动孩子结点。

        """
        _locals = self.__variable_context()
        _text = self.var_values[index].get()
        _name = self.vars[index][0]
        _type = self.vars[index][1][0]
        assert(_type in ("Array", "Record"))
        assert(isinstance(_text, basestring) and _text)
        _data = eval(_text, _locals)
        assert(isinstance(_data, dict))
        if len(_data) == 0: return

        _anonymous = args.get("anonymous", False)
        _orientation = args.get("orientation", "horizontal")
        _width = args.get("width", 40)
        _height = args.get("height", 40)
        _shape = args.get("shape", "oval")
        _x = args.get("x", 0)
        _y = args.get("y", 0)
        _padx = args.get("padx", 2)
        _pady = args.get("pady", 2)
        _xincrement = args.get("xincrement", 0)
        _yincrement = args.get("yincrement", 0)
        _anchor = args.get("anchor", "nw")

        # 计算开始的填充宽度

        _title_height = 20
        # 内置填充宽度
        _ipadx = 2
        _ipady = 2

        # 排序孩子元素
        _keys = list(_data.iterkeys())
        if _type == "Array":
            _keys.sort(lambda x,y: cmp(int(x), int(y)))
        else:
            _keys.sort()
        n = len(_keys)

        # 计算自身范围: x1, y1, x2, y2
        if canvas.winfo_viewable():
            _canvas_width = canvas.winfo_width()
            _canvas_height = canvas.winfo_height()
        else:
            _canvas_width = canvas.winfo_reqwidth()
            _canvas_height = canvas.winfo_reqheight()

        if _orientation == "horizontal":
            _x1 = _x
            _y1 = _y
            _x2 = _canvas_width - _x
            if _height:
                _y2 = _y + _height
            else:
                _y2 = _canvas_height - _y

        else:
            _x1 = _x
            _y1 = _y
            if _width:
                _x2 = _x + _width
            else:
                _x2 = _canvas_width - _x
            _y2 = _canvas_height - _y
        _y2 -= _title_height
        assert(_x1 >= 0 and _x2 >= 0 and _y1 >= 0 and _y2 >= 0)
        assert(_x1 < _x2 and _y1 < _y2)

        _x = _x1 + _ipadx + _padx
        _y = _y1 + _ipady + _pady
        if _width < 40: _width = 40
        if _height < 40: _height = 40

        _offset = 0
        _xoffset = 0
        _yoffset = 0
        for i in range(n):
            k = _keys[i]
            v = _data[k]
            if v is None:
                continue

            if _orientation == "horizontal":
                if _yincrement > 0:
                    _yoffset = (n - i - 1) * _yincrement
                else:
                    _yoffset = - i * _yincrement
            else:
                if _xincrement > 0:
                    _xoffset = (n - i - 1) * _xincrement
                else:
                    _xoffset = - i * _xincrement

            assert(isinstance(v, (basestring, list)))
            # list 类型表示是另外一个变量
            if isinstance(v, list):
                _varname = v[0]
                _child_index = _index = self.__index_of_var(_varname)
                _child_frame = Tkinter.Frame(canvas)
                _child_options = self.var_options[_varname]
                _child_canvas = Tkinter.Canvas(
                    _child_frame,
                    highlightthickness=0,
                    width=_width,
                    height=_height,
                    )
                _child_canvas.grid(sticky="nesw")
                canvas.create_window(
                    _x + _xoffset,
                    _y + _yoffset,
                    window=_child_frame,
                    anchor="nw",
                    tags=(k, _name, "tag_%s" % k),
                    )
                # 还需要判断是否是树还是结构体
                _r = self.__draw_complex_var(
                    _child_canvas,
                    _child_index,
                    x=0,
                    y=0,
                    **_child_options
                    )
                # 重新设置宽度和高度
                _child_canvas.configure(
                    width=_r[2],
                    height=_r[3],
                    )

            else:
                if _anonymous:
                    _title = None
                else:
                    _title = k
                _text = v
                _r = self.__draw_simple_var(
                    canvas,
                    tags=(k, _name, "tag_%s" % k),
                    title=_title,
                    text=_text,
                    x=_x + _xoffset,
                    y=_y + _yoffset,
                    width=_width,
                    height=_height,
                    shape=_shape,
                    )
            if _orientation == "horizontal":
                _x += _r[2]
                if _offset < _r[3]: _offset = _r[3]
            else:
                _y += _r[3]
                if _offset < _r[2]: _offset = _r[2]
            _width += 2 * _xincrement
            _height += 2 * _yincrement


        # 根据孩子的实际尺寸调整自身的尺寸
        # 计算尺寸：_x1, _y1, _x2, _y2
        # 实际坐标，_x, _y
        if _orientation == "horizontal":
            _xr = _x
            _yr = _y + _offset
        else:
            _xr = _x + _offset
            _yr = _y
            
        # 修改终点值
        _x2 = _xr + _ipadx + _padx 
        _y2 = _yr + _ipady + _pady
        _xmount, _ymount = self.__get_child_offset(
            _anchor,
            (_xr, _yr),
            (_x1, _y1, _x2, _y2),
            (_ipadx + _padx, _ipady + _pady),
            )
        if _xmount or _ymount:
            for k in _keys:
                canvas.move("tag_%s" % k, _xmount, _ymount)

        canvas.create_rectangle(
            _x1 + _ipadx,
            _y1 + _ipady,
            _x2 - _ipadx,
            _y2 - _ipady,
            )
        canvas.create_text(
            (_x1 + _x2) / 2,
            _y2 + _ipady,
            anchor="n",
            text=_name,
            )
        return (_x1, _y1, _x2 - _x1, _y2 - _y1 + _title_height)

    def __get_child_offset(self, anchor, point, region, ipad):
        if anchor == "center":
            anchor = ""
        x, y = point
        x1, y1, x2, y2 = region
        ipadx, ipady = ipad

        if x >= x2 - ipadx:
            xamount = 0
        else:
            if "w" in anchor:
                xamount = 0
            elif "e" in anchor:
                xamount = x2 - ipadx - x
            else:
                xamount = (x2 - ipadx - x) / 2

        if y > y2 - ipady:
            yamount = 0
        else:
            if "n" in anchor:
                yamount = 0
            elif "s" in anchor:
                yamount = y2 - ipady - y
            else:
                yamount = (y2 - ipady - y) / 2

        return (xamount, yamount)

    def __action_apply(self):
        for i in range(len(self.vars)):
            self.vars[i][1][1] = self.var_values[i].get()
            name = self.vars[i][0]
            self.vars[i][1][2].update(self.var_options[name])
        self.configure["vars"][:] = self.vars[:]
        self.__apply = True
        self.widget.quit()

    def __variable_context(self, index=0):
        """得到当前的局部数据环境. """
        return dict(self.vars)

    def __available_var_list(self, index):
        """得到 index 之前的变量名称的无序列表。 """
        return ["None"] + dict(self.vars[0:index]).keys()

    def go(self):
        self.widget.transient()
        self.widget.wait_visibility()
        self.widget.grab_set()
        self.widget.focus_set()
        self.widget.mainloop()
        self.widget.destroy()
        return self.__apply

class NewVarDialog(Tkinter.Toplevel):
    def __init__(self, master, childflag=True, namelist=("",)):
        Tkinter.Toplevel.__init__(self, master)
        self.withdraw()
        self.title(_("New Variable"))
        self.childflag = childflag
        self.var_name = Tkinter.StringVar()
        self.var_type = Tkinter.StringVar()
        self.var_value = Tkinter.StringVar()

        if childflag:
            self.__type_list = {
                "Boolean":"False",
                "Char":"",
                "Integer":"0",
                "Pointer":namelist,
                "Real":"0.0",
                "String":"",
                "Reference":namelist,
                }
        else:
            self.__type_list = {
                "Array":"{}",
                "Boolean":"False",
                "Char":"",
                "Integer":"0",
                "Pointer":namelist,
                "Real":"0.0",
                "Record":"{}",
                "String":"",
                "Tree":"{}"
                }

        self.__create_widgets(namelist)
        self.protocol('WM_DELETE_WINDOW', self.quit)
        self.var_type.trace("w", self.__change_var_type)
        self.var_type.set("Integer")

    def __change_var_type(self, v, i, m):
        _type = self.var_type.get()
        if _type in ("Pointer", "Reference"):
            self.__optionmenu_boolean.grid_remove()
            self.__optionmenu_boolean.config(variable="")
            self.__labelentry_value.grid_remove()

            assert(isinstance(self.__type_list[_type], list))
            self.var_value.set(self.__type_list[_type][0])
            self.__optionmenu_pointer.grid()
            self.__optionmenu_pointer.config(variable=self.var_value)

        elif _type == "Boolean":
            self.__optionmenu_pointer.grid_remove()
            self.__optionmenu_pointer.config(variable="")
            self.__labelentry_value.grid_remove()

            self.var_value.set(self.__type_list[_type])
            self.__optionmenu_boolean.grid()
            self.__optionmenu_boolean.config(variable=self.var_value)

        elif _type in ("Record", "Array", "Tree"):
            self.__optionmenu_pointer.grid_remove()
            self.__optionmenu_pointer.config(variable="")
            self.__optionmenu_boolean.grid_remove()
            self.__optionmenu_boolean.config(variable="")

            self.var_value.set(self.__type_list[_type])
            self.__labelentry_value.grid()
            self.__labelentry_value.subwidget("entry")["state"] = "disabled"

        else:
            self.__optionmenu_pointer.grid_remove()
            self.__optionmenu_pointer.config(variable="")
            self.__optionmenu_boolean.grid_remove()
            self.__optionmenu_boolean.config(variable="")
            self.__labelentry_value.grid()
            self.__labelentry_value.subwidget("entry")["state"] = "normal"
            self.var_value.set(self.__type_list.get(_type, ""))
            
    def __create_widgets(self, namelist):
        _soptions = ("label.width 20 label.anchor w "
                     "menubutton.width 15 menubutton.relief groove "
                     "menubutton.borderwidth 1 ")
        _eoptions = ("entry.width 20 entry.borderwidth 1 entry.relief groove "
                     "label.width 20 label.anchor w label.padx 0 ")

        _frame = Tkinter.Frame(self, borderwidth=2, relief="groove")
        _frame.grid(padx=2, pady=2, ipady=2, sticky="nesw")

        _w = Tix.OptionMenu(
            _frame,
            label=_("Type"),
            variable=self.var_type,
            options=_soptions,
            )
        for opt in self.__type_list:
            _w.add_command(opt, label=opt)
        _w.grid(padx=2)

        _w = Tix.LabelEntry(
            _frame,
            label=_("Name"),
            options=_eoptions,
            )
        _w.subwidget("entry").configure(textvariable=self.var_name)
        _w.grid(padx=0, ipady=2)

        _w = Tix.LabelEntry(
            _frame,
            label=_("Value"),
            options=_eoptions,
            )
        _w.subwidget("entry").configure(textvariable=self.var_value)
        _w.grid(row=2, column=0, ipady=2)
        self.__labelentry_value = _w

        _w = Tix.OptionMenu(
            _frame,
            label=_("Value"),
            options=_soptions,
            )
        for opt in namelist:
            _w.add_command(opt, label=opt)
        _w.grid(row=2, column=0, padx=2)
        self.__optionmenu_pointer = _w

        _w = Tix.OptionMenu(
            _frame,
            label=_("Value"),
            options=_soptions,
            )
        for opt in ("True", "False"):
            _w.add_command(opt, label=opt)
        _w.grid(row=2, column=0, padx=2)
        self.__optionmenu_boolean = _w

        _frame = Tkinter.Frame(self)
        _frame.grid()

        _w = Tkinter.Button(
            _frame,
            text=_("OK"),
            overrelief="groove",
            width=8,
            command=self.quit
            )
        _w.grid(row=0, column=0, padx=10, pady=4)

        _w = Tkinter.Button(
            _frame,
            text=_("Cancel"),
            overrelief="groove",
            command=lambda:(self.var_type.set("") or self.quit()),
            width=8,
            )
        _w.grid(row=0, column=1, padx=10, pady=10)

if __name__ == "__main__":
    import gettext
    gettext.NullTranslations().install()

    v1 = ["name", ["String", "Jondy", {}]]
    v2 = ["tree", ["Tree", '{"value": "a", "lchild":{"value":"b"}, "rchild":{"value":"c"}}', {}]]
    v3 = ["a1", ["Array", "{}", {}]]
    v4 = ["r1", ["Record", "{'name':'jondy', 'phone':'1399180625'}", {}]]
    v5 = ["a2", ["Array", "{'1': '3', '0': '0', '3': '2', '2': '2'}", {'orientation':'vertical'}]]
    v6 = ["a3", ["Array", "{'0': ['a2'], '1':['a2']}", {}]]
    v7 = ["p1", ["Pointer", "None", {}]]
    data = {"vars":[v1, v2, v3, v4, v5, v6, v7]}

    root = Tix.Tk()

    _dialog = SettingDialog(root, data)

    print _dialog.go()

#     _dialog = NewVarDialog(root)
#     _dialog.deiconify()
#     _dialog.wait_visibility()
#     _dialog.grab_set()
#     _dialog.focus_set()
#     _dialog.mainloop()
#     print _dialog.var_name.get()
#     _dialog.destroy()
