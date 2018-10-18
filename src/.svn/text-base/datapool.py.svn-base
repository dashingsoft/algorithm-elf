#! /usr/bin/env python
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
#: 文档说明
# 
# @文件：datapool.py
#
# @作者：赵俊德(jondy.zhao@gmail.com)
#
# @创建日期: 2010/09/01
#
# @文件说明：
#
#     数据池维护模块，用于可视化编辑数据池数据，
#
#     或者将数据池数据转换成为一个数据字典。
#
# 数据池实体数据定义：
#
#     数据池是一个字典，经过 repr 转换成为字符串；
#
#     每一个数据项格式：'name' : { 数据属性 }
# 
#     数据属性定义：
#         type,
#         value,
# 
#     根据类型的不同，值的格式也不一样：
# 
#         Integer: int
#         Boolean: bool
#         Real: float
#         String: str
#         Char: str
#         Pointer: list, 包括一个字符串元素，字符串可以为空
#         Array: {} 其中键值为整数
#         Record: {} 其中键值为字符串
#         Tree: {} 固定键值，lchild, rchild, value,
# 
#     在数据池存储的 value 要经过 repr 转换成为字符串；
#     如果数据池中 value 为空字符串，表示对应的变量为 None；
# 
#     Array 和 Record 字典的值有两种情况：
#         如果是字符串，则是 int, bool, float, str 的 repr 结果；
#         如果是字典，则是一个数据项定义；
#    
#     Pointer 对应的值必定是包含一个字符串的列表，表示其指向的变量名称；
# 
#     Tree 的 lchild, rchild 可以为空，或者字典，指向子树数据项定义；
#          value 的含义和 Array 和 Record 中的字典值相同；
# 
#: 导入模块列表
import os
import Tix
import random

# 内置的数据类型和缺省值
TYPE_LIST = {
    "Array" : "{}",
    "Boolean" : "False",
    "Char" : "''",
    "Integer" : "0",
    "Pointer" : "['']",
    "Real" : "0.0",
    "Record" : "{}",
    "String" : "",
    "Tree" : "{}"
    }

class DataPoolFrame(Tix.Frame):
    """算法数据池维护窗口。

    参数基本信息：名称，类型，值，显示属性。

    每一个参数都有其显示属性，控制其显示方式：

        visible,  数值，0 或者 1

        width,    0 表示自动设定合适宽度

        height,   0 表示自动设定合适高度

        shape,    oval

    和结构体相关的有：

        orientation，孩子是水平还是垂直放置 horizontal

        xincrement, yincrement, 水平或者垂直填充增量 0

        anonymous，使用数值 0 和 1 表示是否匿名，匿名也就是说
                   不会显示孩子结点的标题。

        padx,pady 水平和垂直填充像素 2

        anchor, 孩子锚点；nw

        size，针对数组结构，说明数组的大小。这个选项只是用于
        生成数组时候自动生成指定大小的数组，在其他地方可以直
        接根据值得到数组的大小，不需要使用这个值；


    内部属性说明：

        self.__canvas, 显示可见对象的画布

    """
    #: 类公共属性
    empty_item = {
        "type" : "Integer",
        "value" : "0",
        "visible" : 1,
        "width" : 40,
        "height" : 40,
        "shape" : "oval",
        "anchor" : "nw",
        "orientation" : "horizontal",
        "padx" : 2,
        "pady" : 2,
        "xincrement" : 0,
        "yincrement" : 0,
        "anonymous" : 0,
        "size" : 0,
        }

    def __init__(self, master, filename=None):
        """初始化参数。 """
        Tix.Frame.__init__(self, master)
        self.filename = filename
        self.items = { "" : self.empty_item.copy() }
        self.var_itemname = Tix.StringVar(master)

        self.__refresh_flag = True
        self.var_list = {}
        self.__create_widgets()
        
        self.newitem_dialog = NewVarDialog(self)
        if self.filename:
            self.load(filename)

    def insert(self, name, tname="Integer"):
        if tname not in TYPE_LIST:
            raise Exception(_("Unknown data type:") + tname)
        if name in self.items:
            raise Exception(_("Item {0} has been existed").foramt(name))
        x = self.empty_item.copy()
        x["type"] = tname
        x["value"] = TYPE_LIST[tname]
        self.items[name] = x
        self.itemlist_menu.add_command(name, label=name)

    def load(self, filename):
        f = open(filename, "r")
        data = f.read()
        f.close()
        self.items = eval(data, {}, {})
        if "" not in self.items:
            self.items[""] = self.empty_item.copy()
        self.filename = filename
        entries = self.tk.call(self.itemlist_menu, "entries")
        self.itemlist_menu.config(disablecallback=True)
        for name in entries.split():
            self.itemlist_menu.delete(name)
        for k in self.items.keys():
            self.itemlist_menu.add_command(k, label=k)
        self.itemlist_menu.config(disablecallback=False)

    def save(self):
        filename = self.filename
        if filename:
            m = self.var_itemname.get()
            if m:
                x = self.items[m]
                self.__refresh_flag = False
                for k, v in self.var_list.iteritems():
                    x[k] = v.get()
                self.__refresh_flag = True
            f = open(filename, "w")
            f.write(repr(self.items))
            f.close()
        else:
            raise Exception(_("Missing filename of data pool"))

    def __create_widgets(self):
        frame = Tix.Frame(
            self,
            class_="Toolbar",
            borderwidth=2,
            padx=2,
            pady=2,
            relief="groove",
            )
        self.cmdbar = frame
        frame.grid(sticky="we")        
        self.itemlist_menu = Tix.OptionMenu(
            frame,
            label=_("Select Item:"),
            variable=self.var_itemname,
            command=self.select_item,
            options="label.relief flat label.anchor w "
                    "menubutton.width 32 menubutton.relief groove"
            )
        self.itemlist_menu.grid(sticky="we")
        b = Tix.Button(
            frame,
            text=_("Remove"),
            command=self.__action_remove,
            width=8,
            )
        b.grid(row=0, column=1, padx=20)
        
        w = Tix.Label(frame, text=_("New item:"))
        w.grid(row=0, column=2, padx=2, sticky='e')
        w = Tix.Entry(frame, width=30)
        w.grid(row=0, column=3, padx=2, sticky='e')
        self.item_entry = w
        b = Tix.Button(
            frame,
            text=_("Add"),
            command=self.__action_add,
            width=8,
            )
        b.grid(row=0, column=4, padx=4, sticky='e')
        
        b = Tix.Button(
            frame,
            text=_("Clone"),
            command=self.__action_clone,
            width=8,
            )
        b.grid(row=0, column=5, padx=4)


        frame = Tix.Frame(self)
        frame.grid(sticky="nesw")
        frame.columnconfigure(1, weight=1)
        w = Tix.Frame(
            frame,
            borderwidth=2,
            padx=2,
            pady=2,
            relief="groove",
            )
        w.grid(row=0, column=0, sticky="nesw")
        w.columnconfigure(0, weight=1)
        self.__create_property_window(w)

        self.item_canvas = VisualItem(self)
        self.item_canvas.grid(in_=frame, row=0, column=1, sticky="nesw")
        
        frame = Tix.Frame(
            self, 
            class_="Toolbar", 
            pady=10, 
            )
        frame.grid(row=2, column=0)
        # 命令栏
        b = Tix.Button(
            frame,
            text=_("Random Data"),
            command=self.__action_random_data,
            width=12,
            )
        b.grid(row=0, column=0, padx=20)
        
        b = Tix.Button(
            frame,
            text=_("Apply"),
            command=self.__action_apply,
            width=8,
            )
        b.grid(row=0, column=10, padx=20)
        
        b = Tix.Button(
            frame,
            text=_("Close"),
            command=lambda : self.winfo_toplevel().withdraw(),
            width=8,
            )
        b.grid(row=0, column=11, padx=20)

    def __create_property_window(self, frame):
        _soptions = ("label.width 15 label.anchor e label.relief flat "
                     "menubutton.width 15 menubutton.relief groove")
        _coptions = ("label.width 16 label.anchor e "
                     "entry.width 20 relief groove "
                     "decr.relief flat incr.relief flat ")
        _eoptions = ("label.width 16 label.anchor e "
                     "entry.width 20 relief groove")

        boolean_list = ("False", "True")

        v = Tix.StringVar()
        self.var_list["type"] = v

        v = Tix.StringVar()
        self.var_list["value"] = v

        v = Tix.IntVar()
        self.var_list["visible"] = v

        v = Tix.IntVar()
        self.var_list["width"] = v

        v = Tix.IntVar()
        self.var_list["height"] = v

        v = Tix.StringVar()
        self.var_list["orientation"] = v

        v = Tix.IntVar()
        self.var_list["padx"] = v

        v = Tix.IntVar()
        self.var_list["pady"] = v

        v = Tix.IntVar()
        self.var_list["xincrement"] = v

        v = Tix.IntVar()
        self.var_list["yincrement"] = v

        v = Tix.StringVar()
        self.var_list["shape"] = v

        v = Tix.StringVar()
        self.var_list["anchor"] = v

        v = Tix.IntVar()
        self.var_list["anonymous"] = v

        v = Tix.IntVar()
        self.var_list["size"] = v

        w = Tix.OptionMenu(
            frame,
            label=_("Type:"),
            options=_soptions,
            )
        for opt in TYPE_LIST:
            w.add_command(opt, label=opt)
        w.configure(variable=self.var_list["type"])
        w.grid(sticky="wen")

        w = Tix.LabelEntry(
            frame,
            label=_("Value:"),
            options=_eoptions,
            )
        w.entry.config(
            textvariable=self.var_list["value"],
            )
        # w.grid(sticky="wen")

        w = Tix.Text(
            frame,
            width=40,
            height=10,
            state="disabled",
            )
        # w.grid(pady=2, sticky="nesw")
        self.value_text = w

        w = Tix.OptionMenu(
            frame,
            label=_("Visible:"),
            options=_soptions,
            )
        for i in (0, 1):
            w.add_command(str(i), label=boolean_list[i])
        w.configure(variable=self.var_list["visible"])
        w.grid(sticky="wen")

        _option_list = ("oval", "renctangle")
        _w = Tix.OptionMenu(
            frame,
            label=_("Shape:"),
            variable=self.var_list["shape"],
            options=_soptions,
            )
        for _opt in _option_list:
            _w.add_command(_opt, label=_opt)
        _w.grid(sticky="wen")

        _w = Tix.Control(
            frame,
            label=_("Width:"),
            integer=1,
            variable=self.var_list["width"],
            min=40,
            max=1024,
            options=_coptions,
            )
        _w.grid(sticky="wen")

        _w = Tix.Control(
            frame,
            label=_("Heigth:"),
            integer=1,
            variable=self.var_list["height"],
            min=40,
            max=1024,
            options=_coptions,
            )
        _w.grid(sticky="wen")

        _w = Tix.Control(
            frame,
            label=_("Array Size:"),
            integer=1,
            variable=self.var_list["size"],
            min=0,
            max=100,
            options=_coptions,
            )
        _w.grid(sticky="wen")

        _w = Tix.Control(
            frame,
            label=_("Padx:"),
            integer=1,
            variable=self.var_list["padx"],
            min=0,
            max=100,
            options=_coptions,
            )
        _w.grid(sticky="wen")

        _w = Tix.Control(
            frame,
            label=_("Pady:"),
            integer=1,
            variable=self.var_list["pady"],
            min=0,
            max=100,
            options=_coptions,
            )
        _w.grid(sticky="wen")

        _w = Tix.Control(
            frame,
            label=_("Xincrement:"),
            integer=1,
            variable=self.var_list["xincrement"],
            min=-100,
            max=100,
            options=_coptions,
            )
        _w.grid(sticky="wen")

        _w = Tix.Control(
            frame,
            label=_("Yincrement:"),
            integer=1,
            variable=self.var_list["yincrement"],
            min=-100,
            max=100,
            options=_coptions,
            )
        _w.grid(sticky="wen")

        w = Tix.OptionMenu(
            frame,
            label=_("Anonymous:"),
            options=_soptions,
            )
        for i in (0, 1):
            w.add_command(str(i), label=boolean_list[i])
        w.configure(variable=self.var_list["anonymous"])
        w.grid(sticky="wen")
        
        _option_list = ("horizontal", "vertical")
        _w = Tix.OptionMenu(
            frame,
            label=_("Orientation:"),
            variable=self.var_list["orientation"],
            options=_soptions,
            )
        for _opt in _option_list:
            _w.add_command(_opt, label=_opt)
        _w.grid(sticky="wen")

        _option_list = ("n", "ne", "e", "se", "s", "sw", "w", "nw", "center")
        _w = Tix.OptionMenu(
            frame,
            label=_("Anchor:"),
            variable=self.var_list["anchor"],
            options=_soptions,
            )
        for _opt in _option_list:
            _w.add_command(_opt, label=_opt)
        _w.grid(sticky="wen")

        # 设定默认值以及变更跟踪
        for k, v in self.var_list.iteritems():
            v.set(self.empty_item[k])
            if k == "size":
                v.trace_variable("w", self.__change_array_size)
            else:
                v.trace_variable("w", lambda i,v,m,k=k:self.__change_option_value(k))

    def select_item(self, name):
        # 保存老的
        m = self.var_itemname.get()
        if m and m != name:
            x = self.items[m]
            for k, v in self.var_list.iteritems():
                x[k] = v.get()

        # 设置新的
        self.var_itemname.set(name)
        x = self.items[name]
        self.__refresh_flag = False
        for k, v in self.var_list.iteritems():
            v.set(x[k])
        self.value_text["state"] = "normal"
        self.value_text.delete("1.0", "end")
        self.value_text.insert("1.0", x["value"])
        self.value_text["state"] = "disabled"
        self.__refresh_flag = True

        # 显示对应的图片
        self.item_canvas.draw_item(name)

    def __change_option_value(self, key):
        if self.__refresh_flag:
            name = self.var_itemname.get()
            self.items[name][key] = self.var_list[key].get()
            if key == "type":
                tname = self.var_list[key].get()
                self.var_list["value"].set(TYPE_LIST[tname])
            if key == "value":
                self.value_text["state"] = "normal"
                self.tk.call(self.value_text,
                     "replace", "1.0", "end",
                     self.var_list["value"].get())
                self.value_text["state"] = "disabled"
        else:
            name = ""
        if name and name in self.items:
            self.item_canvas.draw_item(name)

    def __change_array_size(self, i, v, m):
        if self.__refresh_flag:
            name = self.var_itemname.get()
        else:
            name = ""
        if name and name in self.items:
            item = self.items[name]
            if item["type"] == "Array":
                key = "size"
                item[key] = self.var_list[key].get()

                # 设置数组新值
                data = eval(item["value"], {}, {})
                assert(isinstance(data, dict))
                size = item["size"]
                x = dict([(str(i), self.empty_item.copy()) for i in range(size)])
                for i in range(size, len(data)):
                    del data[str(i)]
                x.update(data)
                item["value"] = str(x)

                # 显示图片
                self.item_canvas.draw_item(name)

    def insert_item(self, name, tname, value, cflag=False):
        x =  self.empty_item.copy()
        x["type"] = tname
        x["value"] = value

        # 增加一个数组元素或者结构元素
        if cflag:
            item = self.items[self.var_itemname.get()]
            data = eval(item["value"], {}, {})
            assert(isinstance(data, dict))
            data[name] = x
            item["value"] = str(data)
            self.var_list["value"].set(str(data))
            self.item_canvas.draw_item(self.var_itemname.get())

        else:
            entries = self.tk.call(self.itemlist_menu, "entries")
            if name in self.items:
                raise Exception(_("Item name '%s' exists") % name)
            else:
                self.items[name] = x
                self.itemlist_menu.config(disablecallback=True)
                self.itemlist_menu.add_command(name, label=name)
                self.itemlist_menu.config(disablecallback=False)
                self.var_itemname.set(name)

    def __action_add(self):
        itemname = self.item_entry.get()
        if itemname and itemname not in self.items:
            self.insert(itemname)
            self.select_item(itemname)
            
    def __action_remove(self):
        name = self.var_itemname.get()
        if name:
            self.itemlist_menu.delete(name)
            del self.items[name]

    def __action_clone(self):
        name = self.var_itemname.get()
        newname = self.item_entry.get()
        if name and newname and name != newname and newname not in self.items:
            self.items[newname] = self.items[name].copy()
            self.itemlist_menu.add_command(newname, label=newname)
            self.select_item(newname)

    def __action_apply(self):
        self.save()

    def show_error(self, text):
        self.tk.call(
            "tk_messageBox",
            "-title",
            _("Data Pool"),
            "-message",
            text,
            )
            
    def __action_random_data(self):
        name = self.var_itemname.get()
        datatype = self.var_list['type'].get()
        if name and datatype:
            item = self.items[name]
            random.seed()
            if datatype == 'Integer':
                value = random.randint(1, 100)                
                item['value'] = str(value)
            elif datatype == 'Real':
                value = random.random()
                item['value'] = str(value)
            elif datatype == 'Array': 
                value = eval(item["value"], {}, {})
                for i in range(self.var_list['size'].get()):
                    k = str(i)
                    if isinstance(value[k], dict):
                        value[k]['value'] = str(random.randint(1, 100))
                    else:
                        value[k] = str(random.randint(1, 100))
                item['value'] = str(value)
            if value:
                self.item_canvas.draw_item(name)
                self.var_list['value'].set(item['value'])
                
class NewVarDialog(Tix.Toplevel):

    def __init__(self, master):
        Tix.Toplevel.__init__(self, master)
        self.title(_("New Item"))
        self.withdraw()
        self.protocol("WM_DELETE_WINDOW", self.withdraw)
        self.geometry("+300+200")
        self.cflag = False
        self.var_name = Tix.StringVar()
        self.var_type = Tix.StringVar()
        self.var_value = Tix.StringVar()
        
        self.__type_list = TYPE_LIST.copy()
        del self.__type_list["Array"]
        del self.__type_list["Record"]
        del self.__type_list["Tree"]   

        self.__create_widgets()
        self.var_type.set("Integer")

    def __create_widgets(self):
        _soptions = ("label.width 20 label.anchor w label.relief flat "
                     "menubutton.width 15 menubutton.relief groove ")
        _eoptions = ("entry.width 20 entry.relief groove "
                     "label.width 20 label.anchor w label.padx 0 ")

        _frame = Tix.Frame(self, borderwidth=2)
        _frame.grid(padx=2, pady=2, ipady=2, sticky="nesw")

        _w = Tix.OptionMenu(
            _frame,
            label=_("Type:"),            
            options=_soptions,
            )
        for opt in self.__type_list:
            _w.add_command(opt, label=opt)
        _w.config(variable=self.var_type)
        _w.grid(padx=2)

        _w = Tix.LabelEntry(
            _frame,
            label=_("Name:"),
            options=_eoptions,
            )
        _w.subwidget("entry").configure(textvariable=self.var_name)
        _w.grid(padx=0, ipady=2)
        _w.focus_set()

        _w = Tix.LabelEntry(
            _frame,
            label=_("Value:"),
            options=_eoptions,
            )
        _w.subwidget("entry").configure(textvariable=self.var_value)
        _w.grid(row=2, column=0, ipady=2)

        _frame = Tix.Frame(self, class_="Toolbar")
        _frame.grid()

        _w = Tix.Button(
            _frame,
            text=_("Insert"),
            command=self.__new_item,
            )
        _w.grid(row=0, column=0, padx=10, pady=4)

        _w = Tix.Button(
            _frame,
            text=_("Close"),
            command=self.withdraw,
            )
        _w.grid(row=0, column=1, padx=10, pady=10)

    def __new_item(self):
        try:
            self.master.insert_item(
                self.var_name.get(),
                self.var_type.get(),
                self.var_value.get(),
                cflag=True,
                )
        except Exception, inst:
            self.master.show_error(_("New item failed:") + str(inst))
    
    def show(self):
        self.var_name.set("")        
        self.var_value.set("")                         
        self.deiconify()
        self.state("normal")
        self.transient(self.master)

class VisualItem(Tix.Frame):

    def __init__(self, master):
        Tix.Frame.__init__(self, master)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.item_name = ""
        self.master = master

        self.__canvas = Tix.Canvas(
            self,
            width=500,
            height=500,
            highlightthickness=0,
            )
        self.__canvas.grid(sticky="nesw")

    def draw_item(self, name):
        self.item_name = name
        self.__show_variable()

    def __show_variable(self):
        for obj in self.__canvas.find_all():
            self.__canvas.delete(obj)
        _name = self.item_name
        if _name == "":
            return
        _args = self.master.items[_name].copy()
        _type = _args["type"]
        if _type == "Tree":
            _frame = Tix.Frame(self.__canvas)
            _w = Tix.Button(
                _frame,
                text=_("Add left child"),
                relief="flat",
                overrelief="groove",
                command=self.__add_left_child,
                )
            _w.grid(row=0, column=0, padx=10, pady=2)
            _w = Tix.Button(
                _frame,
                text=_("Add right child"),
                relief="flat",
                overrelief="groove",
                command=self.__add_right_child,
                )
            _w.grid(row=0, column=2, padx=10, pady=2)
            _w = Tix.Button(
                _frame,
                text=_("Remove child"),
                relief="flat",
                overrelief="groove",
                command=self.__remove_tree_child,
                )
            _w.grid(row=0, column=1, padx=10, pady=2)
            self.__canvas.create_window(2, 2, window=_frame, anchor="nw")
            self.__draw_tree_var(
                self.__canvas,
                _name,
                x=0,
                y=30,
                **_args
                )

        elif (_type == "Array") or (_type == "Record"):
            _frame = Tix.Frame(self.__canvas)
            if _type == "Record":
                _w = Tix.Button(
                    _frame,
                    text=_("Add member"),
                    relief="flat",
                    overrelief="groove",
                    command=self.__add_child,
                    )
                _w.grid(row=0, column=0, padx=10, pady=2)
                _w = Tix.Button(
                    _frame,
                    text=_("Remove member"),
                    relief="flat",
                    overrelief="groove",
                    command=self.__remove_child,
                    )
                _w.grid(row=0, column=1, padx=10, pady=2)
            else:
                w = Tix.Label(
                    _frame,
                    text=_("Change property 'Array Size' to append or remove"
                           "the element")
                    )
                w.grid()
            self.__canvas.create_window(0, 0, window=_frame, anchor="nw")
            self.__draw_complex_var(
                self.__canvas,
                self.master.items[_name],
                name=_name,
                x=0,
                y=30,
                **_args
                )

        elif _type is not None:
            _text = _args["value"]
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

    def __add_tree_child(self, cname):
        tag = self.__current_node_tag()
        varname = self.item_name
        item = self.master.items[varname]
        if tag:
            data = eval(item["value"], {}, {})
            assert(isinstance(data, dict))
            child = {"value": "", "lchild":{}, "rchild":{}}
            expr = "%s.update({'%s':%s})" % (tag, cname, child)
            eval(expr)
            item["value"] = str(data)
            self.__show_variable()
        else:
            if item["value"] == "{}":
                item["value"] = "{'value':''}"
                self.__show_variable()

    def __current_node_tag(self):
        tags = self.__current_node_tag_list()
        if tags is None or len(tags) == 0:
            return ""
        else:
            return tags[0]

    def __current_node_tag_list(self):
        w = self.__canvas.focus_get()
        if w is None:
            return
        x = w.winfo_x()
        y = w.winfo_y()
        objs = self.__canvas.find_overlapping(x, y, x, y)
        if len(objs) == 0:
            return
        tags = self.__canvas.gettags(objs[0])
        return tags

    def __remove_tree_child(self):
        tag = self.__current_node_tag()
        if tag:
            name = self.item_name
            item = self.master.items[name]
            data = eval(item["value"], {}, {})
            assert(isinstance(data, dict))
            expr = "%s.clear()" % tag
            eval(expr)
            item["value"] = str(data)
            self.__show_variable()

    def __add_child(self):
        self.master.newitem_dialog.show()

    def __remove_child(self):
        tag = self.__current_node_tag()
        if tag:
            name = self.item_name
            item = self.master.items[name]
            data = eval(item["value"], {}, {})
            assert(isinstance(data, dict))
            del data[tag]
            item["value"] = str(data)
            self.master.var_list["value"].set(item["value"])
            self.__show_variable()
            self.__canvas.focus_get()

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
        _activefill = None

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
            _entry = Tix.Entry(
                canvas,
                width=5,
                relief="flat",
                borderwidth=0,
                justify="center",
                bg=_fill,
                )
            _entry.insert(Tix.END, _text)
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
        if event.char:
            name = self.item_name
            item = self.master.items[name]
            if item["type"] == "Tree":
                self.__change_tree_node()
            elif item["type"] in ("Array", "Record"):
                self.__change_struct_node()
            else:
                w = self.__canvas.focus_get()
                text = w.get()
                item["value"] = str(text)
            self.master.var_list["value"].set(item["value"])
    
    def __change_struct_node(self):
        tags = self.__current_node_tag_list()
        try:
            name = tags[1]
        except IndexError:
            return
        item = self.master.items[name]
        data = eval(item["value"], {}, {})
        assert(isinstance(data, dict))
        w = self.__canvas.focus_get()
        text = w.get()
        tag = tags[0]
        data[tag]["value"] = str(text)
        item["value"] = str(data)
        self.master.var_list["value"].set(item["value"])

    def __change_tree_node(self):
        tag = self.__current_node_tag()
        name = self.item_name
        item = self.master.items[name]
        if tag:
            data = eval(item["value"], {}, {})
            assert(isinstance(data, dict))
            w = self.__canvas.focus_get()
            title = w.get()
            expr = "%s.update({'value':'%s'})" % (tag, title)
            eval(expr)
            item["value"] = str(data)
            self.master.var_list["value"].set(item["value"])

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
                arrow=Tix.LAST,
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
                arrow=Tix.LAST,
                )
            self.__draw_tree_node(
                canvas,
                _child,
                tag + "['rchild']",
                _x,
                _y + 40,
                width / 2
                )

    def __draw_tree_var(self, canvas, name, **args):
        local = self.master.items
        item = self.master.items[name]
        text = item["value"]
        assert(isinstance(text, basestring) and text)
        data = eval(text, {}, local)
        assert(isinstance(data, dict))
        if len(data) == 0:
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
        self.__draw_tree_node(canvas, data, "data", _x, _y, _width)
        return _region

    def __draw_complex_var(self, canvas, item, **args):
        """显示一个结构体或者数组。

        结构体的孩子有两种类型：

        一是简单变量，一是结构体。

        两种类型都需要增加下列标签：

        tags = ( key, varname, 'tag_%s' % key)

        其中前面两个用来修改变量的值，后面用来定位和移动孩子结点。

        """
        name = args.get("name", "")
        text = item["value"]
        tname = item["type"]
        assert(tname in ("Array", "Record"))
        assert(isinstance(text, basestring) and text)
        data = eval(text, {}, self.master.items)
        assert(isinstance(data, dict))
        if len(data) == 0:
            return
        anonymous = args.get("anonymous", False)
        orientation = args.get("orientation", "horizontal")
        width = args.get("width", 40)
        height = args.get("height", 40)
        shape = args.get("shape", "oval")
        x = args.get("x", 0)
        y = args.get("y", 0)
        padx = args.get("padx", 2)
        pady = args.get("pady", 2)
        xincrement = args.get("xincrement", 0)
        yincrement = args.get("yincrement", 0)
        anchor = args.get("anchor", "nw")

        # 计算开始的填充宽度

        title_height = 20
        # 内置填充宽度
        ipadx = 2
        ipady = 2

        # 排序孩子元素
        klist = data.keys()
        if tname == "Array":
            klist.sort(lambda x,y: cmp(int(x), int(y)))
        else:
            klist.sort()
        n = len(klist)

        # 计算自身范围: x1, y1, x2, y2
        if canvas.winfo_viewable():
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
        else:
            canvas_width = canvas.winfo_reqwidth()
            canvas_height = canvas.winfo_reqheight()

        if orientation == "horizontal":
            x1 = x
            y1 = y
            x2 = canvas_width - x
            if height:
                y2 = y + height
            else:
                y2 = canvas_height - y

        else:
            x1 = x
            y1 = y
            if width:
                x2 = x + width
            else:
                x2 = canvas_width - x
            y2 = canvas_height - y
        y2 -= title_height
        assert(x1 >= 0 and x2 >= 0 and y1 >= 0 and y2 >= 0)
        assert(x1 < x2 and y1 < y2)

        x = x1 + ipadx + padx
        y = y1 + ipady + pady
        if width < 40: width = 40
        if height < 40: height = 40

        offset = 0
        xoffset = 0
        yoffset = 0
        for i in range(n):
            k = klist[i]
            v = data[k]
            if v is None:
                continue

            if orientation == "horizontal":
                if yincrement > 0:
                    yoffset = (n - i - 1) * yincrement
                else:
                    yoffset = - i * yincrement
            else:
                if xincrement > 0:
                    xoffset = (n - i - 1) * xincrement
                else:
                    xoffset = - i * xincrement

            assert(isinstance(v, dict))
            if v["type"] in ("Array", "Record", "Tree"):
                varname = v[0]
                child_frame = Tix.Frame(canvas)
                child_options = self.master.items[varname]
                child_canvas = Tix.Canvas(
                    child_frame,
                    highlightthickness=0,
                    width=_width,
                    height=_height,
                    )
                child_canvas.grid(sticky="nesw")
                canvas.create_window(
                    x + xoffset,
                    y + yoffset,
                    window=child_frame,
                    anchor="nw",
                    tags=(k, name, "tag_%s" % k),
                    )
                # 还需要判断是否是树还是结构体
                r = self.__draw_complex_var(
                    child_canvas,
                    v,
                    name=k,
                    x=0,
                    y=0,
                    **child_options
                    )
                # 重新设置宽度和高度
                child_canvas.configure(
                    width=r[2],
                    height=r[3],
                    )

            else:
                if anonymous:
                    title = None
                else:
                    title = k
                text = v["value"]
                r = self.__draw_simple_var(
                    canvas,
                    tags=(k, name, "tag_%s" % k),
                    title=title,
                    text=text,
                    x=x + xoffset,
                    y=y + yoffset,
                    width=width,
                    height=height,
                    shape=shape,
                    )
            if orientation == "horizontal":
                x += r[2]
                if offset < r[3]: offset = r[3]
            else:
                y += r[3]
                if offset < r[2]: offset = r[2]
            width += 2 * xincrement
            height += 2 * yincrement


        # 根据孩子的实际尺寸调整自身的尺寸
        # 计算尺寸：x1, y1, x2, y2
        # 实际坐标，x, y
        if orientation == "horizontal":
            xr = x
            yr = y + offset
        else:
            xr = x + offset
            yr = y

        # 修改终点值
        x2 = xr + ipadx + padx
        y2 = yr + ipady + pady
        xmount, ymount = self.__get_child_offset(
            anchor,
            (xr, yr),
            (x1, y1, x2, y2),
            (ipadx + padx, ipady + pady),
            )
        if xmount or ymount:
            for k in klist:
                canvas.move("tag_%s" % k, xmount, ymount)

        canvas.create_rectangle(
            x1 + ipadx,
            y1 + ipady,
            x2 - ipadx,
            y2 - ipady,
            )
        canvas.create_text(
            (x1 + x2) / 2,
            y2 + ipady,
            anchor="n",
            text=name,
            )
        return (x1, y1, x2 - x1, y2 - y1 + title_height)

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

class DataPool(Tix.Toplevel):

    def __init__(self, master, filename=None):
        Tix.Toplevel.__init__(self, master)
        self.withdraw()
        self.title(_("Data Pool"))
        self.geometry('-200-100')
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.withdraw)
        w = DataPoolFrame(self, filename)
        w.grid(sticky="nesw")

if __name__ == "__main__":
    import gettext
    gettext.NullTranslations().install()

    root = Tix.Tk()
    # w = DataPool(root, filename='datapool.data')
    w = DataPool(root)
    w.deiconify()
    w.state('normal')
    w.mainloop()