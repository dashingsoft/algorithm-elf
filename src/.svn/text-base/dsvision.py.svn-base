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
# @文件：dsvision.py
#
# @作者：赵俊德(jondy.zhao@gmail.com)
#
# @创建日期: 2010/02/25
#
# @文件说明：
#
#     可视化数据实体，和 aftype 中定义的数据类型相对应。
#
#     VisionNode, 支持的方法:
#     
#         update,
#         point_me,
#             
#     VisionPointer, 支持的方法：
#     
#         show,
#         hide,
#         update,
#         
#     VisionStruct, 支持的方法
#     
#         append(var)
#         remove(var)
#         show(var),
#         hide(var),
#         update(size),
#         point_me
#         
#     VisionTree,
#     
#         show(index)
#         hide(index)
#         update(index, child)
#         point_me
#         
#     VisionContainer，过程框架对应的可见实体
#
#         append(var)
#         remove(var)
#         show(var)
#         hide(var)
#         point_me
#

import Tkinter
import Tix


class VisionNode(Tkinter.LabelFrame):
    """基本数据类型对应的可见对象。

    一个基本数据类型对应的对象为一个 LabelFrame。

    变量名称为 Label，可以是简单变量名称，也可以是数组下标或者结
    构体的孩子名称。

    变量的值为 Canvas，包括一个 Oval 和 Text。

    空结点，text 为 None，占用区域，但是不显示图片。

    """
    def __init__(self, master, tag, varname="", text="", **args):
        width = args.get("width", 40)
        height = args.get("height", 40)
        anonymous = args.get("anonymous", False)
        if anonymous:
            varname = ""
        self.parent = master
        Tkinter.LabelFrame.__init__(
            self,
            master,
            name=tag,
            borderwidth=0,
            padx=30,
            labelanchor="s",
            text=varname,
            )
        self.args = args.copy()
        if width < 40: width = 40
        if height < 40: height = 40
        padx = self.args.get("padx", 2)
        pady = self.args.get("pady", 2)

        self.value = Tix.Canvas(
            self,
            borderwidth=0,
            width=width,
            height=height,
            selectbackground="#0000FF",
            highlightthickness=1,
            )
        self.value.grid(padx=padx, pady=pady)
        self.update(text)

    def update(self, text=None, fill=None):
        """更新结点文本或者清空结点。 """
        for obj in self.value.find_all():
            self.value.delete(obj)
        width = self.args.get("width", 40)
        height = self.args.get("height", 40)
        shape = self.args.get("shape", "oval")

        ipadx = 2
        ipady = 2
        if width < 40: width = 40
        if height < 40: height = 40
        if shape == "oval":
            func = self.value.create_oval
        else:
            func = self.value.create_rectangle
        if text is None:
            outline_width = 0
            fill = ""
            activefill = ""
        else:
            outline_width = 1
            if fill is None:
                fill="#6495ED"
            activefill="#0000FF"

        func(
            ipadx,
            ipady,
            width - ipadx,
            height - ipady,
            width=outline_width,
            fill=fill,
            activefill=activefill,
            )
        if text is not None:
            self.value.create_text(
                width / 2,
                height / 2,
                text=text
                )
            self.value.focus_set()

    def point_me(self, pointer):
        if pointer.direction != "left":
            pointer.change_arrow("left")
        pointer.place(
            in_=self,
            anchor="nw",
            x=self.value.winfo_width(),
            y=10
            )

class VisionPointer(Tix.Canvas):
    """指针数据类型对应的可见对象。

    就是一个 Canvas，一个圆圈外加一个箭头。

    """
    def __init__(self, master, tag, varname="", direction="left", **args):
        Tix.Canvas.__init__(
            self,
            master,
            name=tag,
            borderwidth=0,
            width=30,
            height=20,
            cursor="dot",
            )
        self.title = varname
        self.__ballon = Tix.Balloon(self, state="balloon", initwait=10)
        self.__ballon.label.destroy()
        self.__ballon.bind_widget(self, msg=varname)
        self.change_arrow(direction)

    def update(self, target):
        if target is None:
            self.place_forget()
        else:
            target.point_me(self)

    def change_arrow(self, direction):
        for obj in self.find_all():
            self.delete(obj)

        self.direction = direction
        # 指向上方的箭头
        if direction == "up":
            self.configure(width=20, height=30)
            self.create_oval(6, 20, 14, 28, fill="#6495ED")
            self.create_line(10, 20, 10, 0, arrow="last")
            _x = 20
            _y = 15
            _anchor = "e"

        # 指向下方的箭头
        elif direction == "down":
            self.configure(width=20, height=30)
            self.create_oval(6, 2, 14, 10, fill="#6495ED")
            self.create_line(10, 10, 10, 30, arrow="last")
            _x = 20
            _y = 15
            _anchor = "e"

        # 指向左方的箭头
        elif direction == "right":
            self.configure(width=30, height=20)
            self.create_oval(10, 6, 2, 14, fill="#6495ED")
            self.create_line(10, 10, 30, 10, arrow="last")
            _x = 15
            _y = 0
            _anchor = "n"

        # 指向右方的箭头
        else:
            self.configure(width=30, height=20)
            self.create_oval(20, 14, 28, 6, fill="#6495ED")
            self.create_line(20, 10, 0, 10, arrow="last")
            _x = 15
            _y = 0
            _anchor = "n"

        if self.title:
            self.create_text(_x, _y, text=self.title, anchor=_anchor)

class VisionStruct(Tix.Frame):
    """数组和记录体类型对应的可见对象。

    数组和结构数据类型对应的对象为一个 LabelFrame。

    """
    def __init__(self, master, tag, varname="", **args):
        self.parent = master
        ipadx = args.get("ipadx", 15)
        borderwidth = args.get("borderwidth", 2)
        Tix.Frame.__init__(
            self,
            master,
            name=tag,
            borderwidth=0,
            padx=ipadx,
            )
        self.value = Tkinter.LabelFrame(
            self,
            borderwidth=borderwidth,
            pady=2,
            relief="groove",
            labelanchor="nw",
            text=varname,
            )
        self.value.grid(row=0, column=0, sticky="nesw")
        self.options = args.copy()
        self.children_info = {}
        self.counter = 0

    def point_me(self, pointer):
        if pointer.direction != "left":
            pointer.change_arrow("left")
        pointer.place(
            in_=self,
            x=self.value.winfo_width(),
            y=10
            )

    def hide_child(self, w):
        opts = w.grid_info()
        self.children_info[id(w)] = opts
        w.grid_forget()

    def show_child(self, w):
        if id(w) in self.children_info:
            opts = self.children_info[id(w)]
            w.grid(**opts)
        else:
            self.append(w)

    def append(self, widget):
        orientation = self.options.get("orientation", "horizontal")
        if orientation == "vertical":
            row = self.counter
            col = 0
            self.counter += 1
        else:
            row = 0
            col = self.counter
            self.counter += 1

        if widget is not None:
            self.insert(widget, row, col)

    def insert(self, widget, row=0, col=0):
        """插入到指定位置. """
        ipadx = 2
        ipady = 2
        anchor = self.options.get("anchor", "nw")

        if anchor == "center": anchor = ""
        widget.grid(
            in_=self.value,
            row=row,
            column=col,
            padx=ipadx,
            pady=ipady,
            sticky=anchor,
            )

    def remove(self, widget):
        widget.grid_remove()
        widget.destroy()

# class VisionBinaryTree(Tix.Frame):
#     """二叉树对应的可见对象。

#     属性：

#     self.parent        父对象，根结点的父对象为 None，其他的均为 VisionTree 实例

#     self.lchild        左孩子，None 或者 VisionTree 实例
#     self.rchild        右孩子，None 或者 VisionTree 实例

#     self.__text        结点显示的文本

#     """
#     def __init__(self, master, tag, text, width):
#         Tix.Frame.__init__(
#             self,
#             master,
#             name=tag,
# #             borderwidth=2,
# #             relief="groove",
#             )
#         self.rowconfigure(0)
#         self.rowconfigure(1, weight=1)
#         self.columnconfigure(0, weight=1)

#         self.value = Tix.Canvas(
#             self,
#             borderwidth=0,
#             width=width,
#             height=80,
#             )
#         self.value.grid(row=0, column=0, sticky="nwe")

#         self.__children = Tix.Frame(self)
#         self.__children.grid(row=1, column=0, sticky="nesw")
#         self.__children.rowconfigure(0, weight=1)

#         self.child_list = {}
#         self.parent = None

#         self.__text = text
#         self.__draw_node(width)

#         self.bind("<Configure>", self.__resize)

#     def __getattr__(self, name):
#         if name == "lchild":
#             return self.child_list.get(0, None)
#         elif name == "rchild":
#             return self.child_list.get(1, None)
#         else:
#             raise AttributeError(name)

#     def __draw_node(self, width):
#         for obj in self.value.find_withtag("V"):
#             self.value.delete(obj)

# #         if self.value.winfo_viewable():
# #             x = self.value.winfo_width() / 2
# #         else:
# #             x =  self.value.winfo_reqwidth() / 2

#         x = width / 2
#         y = 2
#         r = 18
#         self.value.create_oval(
#             x - r,
#             y,
#             x + r,
#             y + r * 2,
#             fill="#6495ED",
#             activefill="#0000FF",
#             tags=("V",)
#             )
#         self.value.create_text(
#             x,
#             y + r,
#             text=self.__text,
#             tags=("V",)
#             )
# #         self.value.focus_set()

#     def __draw_tree(self, child):
#         x = self.value.winfo_width() / 2
#         y = 40
#         height = 40
#         for obj in self.value.find_withtag("C%d" % id(child)):
#             self.value.delete(obj)
#         self.value.create_line(
#             x,
#             y,
#             child.winfo_x() + child.winfo_width() / 2,
#             y + height,
#             arrow="last",
#             tags=("C%d" % id(child),)
#             )

#     def insert_child(self, name, text, index=0):
#         width = self.value.winfo_width() / 2

#         _child = VisionTree(self.__children, name, text, width)
#         _child.parent = self
#         self.child_list[index] = _child
#         self.__children.columnconfigure(index, weight=1)

#         self.child_list[index].grid(
#             in_=self.__children,
#             row=0,
#             column=index,
#             sticky="nwe"
#             )
# #         _xe = self.child_list[index].winfo_width()
# #         if _xe != x:
# #             self.child_list[index].update(_xe)
#         self.__draw_tree(self.child_list[index])
#         return _child

#     def point_me(self, pointer):
#         _x = self.value.winfo_width() / 2 + 30
#         _y = self.value.winfo_y() + 10
#         if pointer.direction != "left":
#             pointer.change_arrow("left")
#         pointer.place(in_=self, x=_x, y=_y)

#     def __resize(self, event=None):
#         width = self.value.winfo_width()
#         self.__draw_node(width)
#         if self.parent is not None:
#             self.parent.__draw_tree(self)

class VisionTree(Tix.Frame):
    """树对应的可见对象。

    属性：

    self.parent        父对象，根结点的父对象为 None，其他的均为 VisionTree 实例
    self.child_list    孩子字典，None 或者 VisionTree 实例

    """
    def __init__(self, master, tag, node, width):
        self.parent = master
        Tix.Frame.__init__(
            self,
            master,
            name=tag,
            )
        self.rowconfigure(0)
        self.rowconfigure(1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        self.value = VisionStruct(
            self,
            "value_frame",
            args={"anchor" :"center", "height" : 40},
            )
        self.value.grid(row=0, column=0)
        self.value.append(node)

        self.__tree = Tix.Canvas(
            self,
            borderwidth=0,
            width=width,
            height=40,
            )
        self.__tree.grid(row=1, column=0, sticky="wen")

        self.__children = Tix.Frame(self)
        self.__children.grid(row=2, column=0, sticky="nesw")
        self.__children.rowconfigure(0, weight=1)

        self.child_list = {}
        self.parent = None

        self.bind("<Configure>", self.__resize)

    def __draw_tree(self, child):
        assert(issubclass(child.__class__, VisionTree))
        x = self.__tree.winfo_width() / 2
        y = 0
        height = 40
        for obj in self.__tree.find_withtag("T%d" % id(child)):
            self.__tree.delete(obj)
        self.__tree.create_line(
            x,
            y,
            child.winfo_x() + child.winfo_width() / 2,
            y + height,
            arrow="last",
            tags=("T%d" % id(child),)
            )

    def remove_child(self, child):
        assert(issubclass(child.__class__, VisionTree))
        for obj in self.__tree.find_withtag("T%d" % id(child)):
            self.__tree.delete(obj)

    def insert_child(self, tag, node, index=0):
        width = self.__tree.winfo_width() / 2

        _child = VisionTree(self.__children, tag, node, width)
        _child.parent = self
        self.child_list[index] = _child
        self.__children.columnconfigure(index, weight=1)

        self.child_list[index].grid(
            in_=self.__children,
            row=0,
            column=index,
            sticky="wen"
            )
        self.__draw_tree(self.child_list[index])
        return _child

    def point_me(self, pointer):
        _x = self.__tree.winfo_width() / 2
        _y = 0
        if pointer.direction != "up":
            pointer.change_arrow("up")
        pointer.place(in_=self.__tree, anchor="n", x=_x, y=_y)

    def update(self, widget):
        if widget is None:
            pass

    def __resize(self, event=None):
        if self.parent is not None:
            self.parent.__draw_tree(self)

class VisionGraph(Tix.Canvas):
    pass

class VisionContainer(VisionStruct):
    """每一层函数调用对应的可见对象。

    简单变量都放在第一行，

    垂直布局的结构都放在第二行，

    树单独占一行，

    水平布局的结构也单独占一行，
    """
    def __init__(self, master, tag, title, args):
        VisionStruct.__init__(
            self,
            master,
            tag,
            varname=title,
            args=args,
            )
        self.counter0 = 0
        self.counter1 = 0
        
        self.single_frame = Tix.Frame(self.value)
        self.single_frame.grid(row=0, column=0, sticky="we")
        self.pole_frame = Tix.Frame(self.value)
        self.pole_frame.grid(row=1, column=0, sticky="we")
        
    def append(self, w):
        w.parent = self
        w.grid(in_=self.single_frame, row=0, column=self.counter0, sticky="w")        
        self.counter0 += 1
    
    def append_tree(self, w):
        col, row = self.value.grid_size()
        row += 1
        if row == 1:
            row = 2
        w.grid(in_=self.value, row=row, column=0, sticky="nesw")

    def append_struct(self, w):
        col, row = self.value.grid_size()
        orientation = w.options.get("orientation", "horizontal")
        if orientation == "vertical":
            w.grid(in_=self.pole_frame, row=0, column=self.counter1, sticky="w")
            self.counter1 += 1
        else:
            if row:
                row += 1
            else:
                row = 2
            w.grid(in_=self.value, row=row, column=0, sticky="nesw")


if __name__ == "__main__":
    import gettext
    gettext.NullTranslations().install()

    root = Tix.Tk()
    #root.state("zoomed")
    #root.attributes('-transparentcolor', __transparentcolor__)

    w4 = VisionNode(root, "me", varname="me", text="abc")
    w4.grid(padx=1, pady=0, sticky="nesw")

    w5 = VisionPointer(root, "o", varname="p0")
    w5.grid()

    v =  root.nametowidget('me')
    v.update("xyz")

    w6 = VisionNode(root, "me2", varname="me2", text="123.56")
    w6.grid()

    v =  root.nametowidget('me2')
    v.update("3.5")

    w7 = VisionPointer(root, "w7", varname="p")
    root.update_idletasks()
    v.point_me(w7)

    w8 = VisionStruct(root, "w8", varname="student")
    w8.grid()

    w9 = VisionNode(root, "w9", varname="name", text="jondy")
    w10 = VisionNode(root, "w10", varname="birthday", text="1976/01/21")

    w8.append(w9)
    w8.append(w10)

    # p1 = VisionPointer(root, "p1", varname="p1")
    # w10.destroy()
    # root.update_idletasks()
    # w9.point_me(p1)


    # w11 = VisionTree(root, "w11", None, 200)
    # t0 = VisionNode(w11, "t0", varname="root", text="A")
    # w11.value.append(t0)
    # w11.grid()

    # print w11.value.winfo_width(), w11.value.winfo_height()
    # print t0.winfo_width(), t0.winfo_height(), t0.winfo_x(), t0.winfo_y()

    # t1 = VisionNode(w11, "t1", text="B")
    # t2 = VisionNode(w11, "t2", text="C")
    # w11.insert_child("t1", t1, 0)
    # w11.insert_child("t2", t2, 1)

    # p2 = VisionPointer(root, "p2", varname="p2")
    # root.update_idletasks()
    # w11.child_list[0].point_me(p2)

    root.mainloop()