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
 * @文件：dsgraph.py
 *
 * @作者：赵俊德(jondy.zhao@gmail.com)
 *
 * @创建日期: 2010/02/24
 *
 * @文件说明：
 *
 *   用于显示算法执行过程中的可视化数据，譬如汉诺塔，树，图等。
 *
"""

import Tix

import aftype
from dsvision import VisionNode
from dsvision import VisionTree
from dsvision import VisionPointer
from dsvision import VisionStruct
from dsvision import VisionContainer


class VisionView(Tix.Frame):
    """显示算法执行过程中的图像。譬如汉诺塔，树，图等。

    属性

        self.__canvas,    顶层窗口对象。

        self.options      配置文件中 vision 对应的全部可见对象的显示属性。
        
                          例如：实数显示格式等；

        self.current_frame, 当前函数的框架

        self.main_frame, 主框架，用于显示 new 产生的数据
        
        self.frame_list, 框架列表

    """
    def __init__(self, master, options):
        Tix.Frame.__init__(self, master)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.options = options        
        self.__create_widgets()     
        self.main_frame = None
        self.current_frame = None   

    def reset(self):
        for obj in self.canvas.winfo_children():
            obj.destroy()
        self.main_frame = VisionContainer(
            self.canvas,
            "main_frame",
            "0. GLOBAL HEAP",
            self.options.get("frame", {})
            )
        self.main_frame.grid(sticky="nwe")
        
        self.current_frame = self.main_frame
        self.frame_list = [self.main_frame]

    def __exists(self, var):
        """检查是否存在 var 对应的可见对象. """
        assert(issubclass(type(var), aftype.BaseType))
        return self.__widget_of_tag(self.canvas, var.tagid)

    def __widget_of_tag(self, w, tag):
        if w is None:
            return None
        if w.winfo_name() == tag:
            return w
        try:
            w = w.nametowidget(tag)
            return w
        except KeyError:
            pass
        for obj in w.winfo_children():
            w = self.__widget_of_tag(obj, tag)
            if w is not None:
                return w

    def __create_widgets(self):
        w = Tix.ScrolledWindow(
            self,
            scrollbar='auto',
            )
        w.grid(sticky="nesw")

        self.canvas = w.window
        self.canvas.columnconfigure(0, weight=1)

    def refresh(self, xzoom=1.0, yzoom=1.0):
        self.canvas.grid_forget()
        self.canvas.grid(sticky="nesw")

    def push(self, coname, lineno):
        row = len(self.frame_list)
        self.frame_list.append(self.current_frame)
        self.current_frame = VisionContainer(
            self.canvas,
            coname + str(row),
            "%d. %s:%d" % (row, coname, lineno),
            self.options.get("frame", {})
            )        
        self.current_frame.grid(row=row, column=0, sticky="nwe")

    def pop(self):
        if self.current_frame:
            self.current_frame.grid_remove()
            self.current_frame.destroy()
        self.current_frame = self.frame_list.pop()

    def add_variable(self, var):
        """增加变量 var 对应的可见对象. """
        assert(issubclass(type(var), aftype.BaseType))

        if issubclass(type(var), aftype.Tree):
            self.__watch_tree_variable(var)

        elif issubclass(type(var), aftype.Pointer):
             self.__watch_pointer_variable(var)

        elif issubclass(type(var), aftype.Struct):
            self.__watch_struct_variable(var)

        else:
            self.__watch_simple_variable(var)

    def __watch_simple_variable(self, var, frame=None):
        """创建简单数据类型对应的可见对象. 
        如果 var 没有初始化，其值为 None，那么不显示该对象。
        """
        if frame is None:
            frame = self.current_frame
        try:
            text = str(var)
        except aftype.AlgorithmError, inst:
            text = ""
        node = VisionNode(
            frame,
            var.tagid,
            varname=var.name,
            text=text,
            )
        frame.append(node)

    def __watch_tree_variable(self, var, frame=None):        
        if var is None:
            return
        if frame is None:
            frame = self.current_frame
        args = var.options
        width = frame.winfo_width()
        root = VisionTree(
            frame,
            var.tagid,
            None,
            width,
            )
        tag = var["value"].tagid
        node = VisionNode(
            root,
            tag,
            shape=args.get("shape", "oval"),
            text=var["value"],
            )
        root.value.append(node)

        if var["lchild"].get():
            args["index"] = 0
            lchild = self.__new_tree_node(
                root,
                var["lchild"].get(),
                args
                )

        if var["rchild"].get():
            args["index"] = 1
            rchild = self.__new_tree_node(
                root,
                var["rchild"].get(),
                args
                )
        frame.append_tree(root)

    def __new_tree_node(self, pnode, var, args):
        tag = var["value"].tagid
        index = args.get("index", 0)
        node = VisionNode(
            self.canvas,
            tag,
            shape=args.get("shape", "oval"),
            text=var["value"],
            )

        w = pnode.insert_child(var.tagid, node, index)
        if var["lchild"].get():
            args["index"] = 0
            self.__new_tree_node(w, var["lchild"].get(), args)
        if var["rchild"].get():
            args["index"] = 1
            self.__new_tree_node(w, var["rchild"].get(), args)
        return w

    def __watch_pointer_variable(self, var, frame=None):
        args = var.options
        node = VisionPointer(
            self.canvas,
            var.tagid,
            varname=var.name,
            **args
            )
        try:
            value = var.value
        except aftype.AlgorithmError, inst:
            value = None
        if value is None:
            return 
        assert issubclass(type(value), aftype.BaseType), type(value)
        target = self.__widget_of_tag(self.canvas, value.tagid)
        if target:
            node.update(target)

    def __watch_struct_variable(self, var, frame=None):
        """创建结构体对应的可见对象。

        传入的选项：
            orientation，结构的方向，水平或者垂直；
            increment，对于数组来说，每一个结点的尺寸增量，默认为 0；
            shape，简单数据类型对应的孩子结点类型。

        """
        if frame is None:
            frame = self.current_frame
        _args = var.options.copy()
        _orientation = _args.get("orientation", "horizontal")
        _padx = _args.get("padx", 2)
        _pady = _args.get("pady", 2)
        _xincrement = _args.get("xincrement", 0)
        _yincrement = _args.get("yincrement", 0)
        _anchor = _args.get("anchor", "nw")
        _shape = _args.get("shape", "oval")
        _width = _args.get("width", 40)
        _height = _args.get("height", 40)
        _anonymous = _args.get("anonymous", False)

        _node = VisionStruct(
            frame,
            var.tagid,
            varname=var.name,
            **_args
            )
        frame.append_struct(_node)
#         if _orientation == "horizontal":
#             _node.grid(sticky="wen")
#         else:
#             _node.grid(sticky="nsw")

        _keys = [k for k in var.value.keys()]
        _keys.sort()
        n = len(_keys)
        _xoffset = 0
        _yoffset = 0
        for i in range(n):
            k = _keys[i]
            v = var.value[k]
            if v is None:
                _node.append(None)
                continue
            assert(issubclass(type(v), aftype.BaseType))
            v.visible = 1

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

            if issubclass(type(v), (aftype.Array, aftype.Record, aftype.Tree)):
                _child = self.__watch_struct_variable(v)

            elif issubclass(type(v), aftype.Pointer):
                _child = VisionPointer(
                    frame,
                    v.tagid,
                    varname=v.name,
                    )
            else:
                if v:
                    _text = str(v)
                else:
                    _text = None
                _name = k
                _child = VisionNode(
                    frame,
                    v.tagid,
                    varname=_name,
                    text=_text,
                    width=_width,
                    height=_height,
                    shape=_shape,
                    padx=_padx + _xoffset,
                    pady=_pady + _yoffset,
                    anonymous=_anonymous,
                    )
            _node.append(_child)
            _width += 2 * _xincrement
            _height += 2 * _yincrement
        return _node

    def update_variable(self, var, value):
        # 检查是否存在 var 对应的可见对象
        w = self.__widget_of_tag(self.canvas, var.tagid)
        if w is None:
            return
        # 更新树结点
        if issubclass(type(var), aftype.Tree):
            self.__update_tree_node(w, var, value)

        # 更新指针，指向新的对象
        elif issubclass(type(var), aftype.Pointer):
            if value is None:
                w.place_forget()
                return
            assert issubclass(type(value), aftype.BaseType), type(value)
            assert issubclass(w.__class__, VisionPointer), w.__class__
            target = self.__widget_of_tag(self.canvas, value.tagid)
            w.update(target)

        # 更新数组
        elif issubclass(type(var), aftype.Array):
            for k, v in value.iteritems():
                text = str(v)
                node = VisionNode(
                    w,
                    v.tagid,
                    varname=str(k),
                    text=text,
                    )
                w.append(node)
                
        # 更新结点值
        else:
            assert(isinstance(w, VisionNode))
            if value is None:
                if w.winfo_viewable():
                    self.hide_variable(var)
            else:
                if not w.winfo_viewable():
                    self.show_variable(var)
                w.update(str(value))

    def __update_tree_node(self, widget, var, value):
        assert(issubclass(type(value), aftype.Tree))
        assert(issubclass(widget.__class__, VisionTree))
        _parent = widget.parent
        if value.is_empty_tree():
            if _parent is not None:
                parent.remove_child(widget)
            self.after_idle(widget.destroy)

        else:
            _index = widget.grid_info()["column"]
            self.after_idle(widget.destroy)
            if _parent is None:
                self.__watch_tree_variable(value)
            else:
                self.__new_tree_node(parent, value, _index)

    def copy_variable(self, source, dest):
        """拷贝变量的内容。

        目标和源必须数据类型一致。
        """
        assert(issubclass(type(source), aftype.BaseType))
        assert(issubclass(type(dest), aftype.BaseType))
        s = self.__widget_of_tag(self.canvas, source.tagid)
        if s is None: return

        t = self.__widget_of_tag(self.canvas, dest.tagid)
        if t is None: return

        # 简单结点的复制
        if (issubclass(s.__class__, VisionNode)
            and issubclass(t.__class__, VisionNode)):
            t.update(text=str(source))

    def remove_variable(self, var):
        w = self.__widget_of_tag(self.canvas, var.tagid)
        if w:
            w.destroy()

    def select_variable(self, var):
        """选中局部变量对应的可见对象. """
        w = self.__widget_of_tag(self.canvas, var.tagid)
        if w:
            w.focus_set()

    def active_variable(self, var):
        """激活局部变量对应的可见对象, 通过改变背景色实现. """
        w = self.__widget_of_tag(self.canvas, var.tagid)
        if issubclass(w.__class__, VisionNode):
            w.update(text=str(var.value), fill="#9932CC")

    def deactive_variable(self, var):
        """取消局部变量对应的可见对象的激活状态，恢复原来的背景色. """
        w = self.__widget_of_tag(self.canvas, var.tagid)
        if issubclass(w.__class__, VisionNode):
            w.update(text=str(var.value))
            
    def show_variable(self, var):
        """调用父对象的方法来显示变量. """
        w = self.__widget_of_tag(self.canvas, var.tagid)
        if w and w.parent:
            w.parent.show_child(w)

    def hide_variable(self, var):
        """调用父对象的方法来隐藏变量. """
        w = self.__widget_of_tag(self.canvas, var.tagid)
        if w and w.parent:
            w.parent.hide_child(w)
            
    def dispose_heap_variable(self, var):
        self.hide_variable(var)
        
    def new_heap_variable(self, var):
        """增加全局堆变量。"""
        assert(issubclass(type(var), aftype.BaseType))

        if issubclass(type(var), aftype.Tree):
            self.__watch_tree_variable(var, frame=self.main_frame)

        elif issubclass(type(var), aftype.Pointer):
             self.__watch_pointer_variable(var, frame=self.main_frame)

        elif issubclass(type(var), aftype.Struct):
            self.__watch_struct_variable(var, frame=self.main_frame)

        else:
            self.__watch_simple_variable(var, frame=self.main_frame)

        # w = self.__widget_of_tag(self.canvas, var.tagid)
        # if w:
        #     try:
        #         text = str(var)
        #     except aftype.AlgorithmError, inst:
        #         text = ""
        #     node = VisionNode(
        #         w,
        #         var.tagid,
        #         varname=var.name,
        #         text=text,
        #         )
        #     w.append(node)



if __name__ == '__main__':
    pass