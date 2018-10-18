#! /usr/bin/env python
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
# @文件：dsplayer.py
#
# @作者：赵俊德(jondy.zhao@gmail.com)
#
# @创建日期: 2010/02/24
#
# @文件说明：
#
#   算法演示窗口，用于显示算法执行过程。
#
# @修改日期: 210/09/05
#
#   重新调整主界面和算法启动过程，以及入口参数的处理。
#

import sys
import os
import Tkinter
import Tix
import tkFileDialog

from traceback import format_exc

import mysite
import about
import datapool

import dsgraph
import dscore


class AlgorithmPlayer(Tix.Frame):
    """算法演示主程序，用于显示算法执行过程。

    一个工具栏，包括打开算法，设置算法参数，设置演示参数，显
    示堆栈、内存、日志视图的开关，以及算法的启动、单步、暂停
    等功能按钮。

    中间部分是源代码和可见视图部分。

    下面是一个状态栏，显示当前算法文件的名称。

    其中堆栈、内存和日志视图都是主窗口的子窗口，浮动显示在主
    窗口上面，可以隐藏。

    内部属性：

    /**    var_status
    表示当前算法状态的一个变量，可用值：
        none,       没有算法被选中。
        open,       算法打开。
        run,        算法正在运行中。
        pause,      算法暂停运行。
        finish,     算法已经结束运行，可能是多种原因，
                    正常结束，运行异常，用户终止等。

        算法状态的改变直接影响着各个按钮是否可用，使用
        trace_variable 方式设置按钮状态。
    */

    外部属性：
    /**     var_interval

    演示语句延时变量。

    */

    /**    options

    字典类型的系统配置选项。例如
    {'interval' : 100, 'debug-mode' : 1}

    */

    """
    options = {}
    history_path = ""

    def __init__(self, master, options={}):
        Tix.Frame.__init__(self, master)

        self.var_interval = Tix.IntVar()
        self.options.update(options)

        self.master.protocol('WM_DELETE_WINDOW', self.wm_delete_window)

        #: 显示设置
        master.option_add("*relief", "flat")
        master.option_add("*overRelief", "groove")

        master.option_add("*Menu*tearOff", "0")
        master.option_add("*Coolbar*relief", "groove")
        master.option_add("*Toolbar*relief", "flat")
        master.option_add("*Toolbar*Button.relief", "flat")
        master.option_add("*Toolbar*Button.overRelief", "groove")
        master.option_add("*Toolbar*Button.width", "8")
        master.option_add("*Toolbar*Menubutton.relief", "groove")

        master.option_add("*Entry.relief", "ridge")
        master.option_add("*Entry.highlightThickness", "0")
        master.option_add("*Menu*tearOff", "0")
        master.option_add("*Menubutton.relief", "groove")

        opt = options["style"].get("font", "TkTextFont")
        master.option_add("*Text.font", opt)
        master.option_add("*TixHList.font", opt)
        opt = options["style"].get("background", "white")
        master.option_add("*Text.background", opt)
        master.option_add("*TixHList.background", opt)
        opt = options["style"].get("foreground", "black")
        master.option_add("*Text.foreground", opt)
        master.option_add("*TixHList.foreground", opt)

        opt = options["style"]["select"]["background"]
        master.option_add("*Text.selectBackground", opt)
        opt = options["style"]["select"]["foreground"]
        master.option_add("*Text.selectForeground", opt)
        opt = options["style"]["insert"]["background"]
        master.option_add("*Text.insertBackground", opt)
        master.option_add("*TixTree.*scrollbar", "none")
        master.option_add("*PanedWindow.showHandle", "False")
        master.option_add("*Panedwindow.sashWidth", "2")
        master.option_add("*Panedwindow.sashRelief", "groove")

        #: 配置主窗口是可以改变大小的
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)
        self.rowconfigure(0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        #: 创建子控件
        self.__create_widgets()
        self.__configure_widgets()
        self.algorithm_driver = dscore.AlgorithmDriver(
            self,
            self.options["playback"],
            )

        #: 算法状态设置
        self.var_status = Tix.StringVar(master)
        self.var_status.trace("w", self.__update_status)
        self.var_status.set("none")

    def __create_widgets(self):
        #: 命令面板
        coolbar = Tix.Frame(
            self,
            class_="Coolbar",
            borderwidth=2,
            pady=2,
            )
        coolbar.grid(row=0, sticky="we")
        coolbar.columnconfigure(1, weight=1)

        w = Tix.Frame(
            coolbar,
            class_="Toolbar",
            padx=5,
            pady=2,
            borderwidth=2,
            )
        w.grid(
            row=0,
            column=0,
            padx=5,
            sticky="w",
            )
        self.__create_command_toolbar1(w)

        w = Tix.Frame(
            coolbar,
            class_="Toolbar",
            padx=5,
            pady=2,
            borderwidth=2,
            )
        w.grid(
            row=0,
            column=1,
            padx=5,
            )
        self.__create_command_toolbar2(w)

        w = Tix.Frame(
            coolbar,
            class_="Toolbar",
            padx=5,
            pady=2,
            borderwidth=2,
            )
        w.grid(
            row=0,
            column=2,
            padx=5,
            sticky="e",
            )
        self.__create_command_toolbar3(w)

        #: 视图窗口
        pane = Tkinter.PanedWindow(
            self,
            orient="horizontal",
            width=800,
            height=600,
            )
        pane.grid(
            row=1,
            column=0,
            sticky="nesw",
            )
        pane1 = Tkinter.PanedWindow(
            pane,
            orient="vertical",
            showhandle=False,
            )
        self.data_view = dsgraph.VisionView(pane, self.options["vision"])

        self.code_view = SourceFrame(pane1, self)
        self.console_view = ConsoleFrame(pane1)

        pane1.add(self.code_view, minsize=300, sticky="nesw")
        pane1.add(self.console_view, minsize=100, sticky="nesw")

        pane.add(pane1, minsize=300, sticky="nesw")
        pane.add(self.data_view, minsize=300, sticky="nesw")

        # 堆栈、内存和日志视图
        self.stack_view = ViewStack(self)
        self.bp_view = ViewBreakpoint(self)
        self.para_view = ViewParameter(self)
        self.data_pool = self.para_view.data_pool

        #: 状态栏
        frame = Tix.Frame(self)
        frame.grid(row=2, sticky="we")
        self.var_info = Tix.StringVar(self.master)
        w = Tix.Label(frame, textvariable=self.var_info)
        w.grid(sticky="we")

    def __configure_widgets(self):
        hbg = self.options["style"]["highlight"]["background"]
        hfg = self.options["style"]["highlight"]["foreground"]
        efg = self.options["style"]["error"]["foreground"]
        self.code_view.text.tag_configure(
            "i",
            background=hbg,
            foreground=hfg,
            )
        self.console_view.text.tag_configure(
            "e",
            foreground=efg,
            )

    def __create_command_toolbar1(self, toolbar):
        self.button_open = Tix.Button(
            toolbar,
            command=self.__action_open,
            text=_("Open"),
            )
        self.button_open.grid(
            row=0,
            column=0,
            padx=2,
            sticky="w",
            )
        self.button_setting = Tix.Button(
            toolbar,
            command=self.__action_parameter,
            text=_("Parameter"),
            )
        self.button_setting.grid(
            row=0,
            column=1,
            padx=2,
            sticky="w",
            )
        w = Tix.Button(
            toolbar,
            command=self.__action_breakpoint,
            text=_("Breakpoint"),
            )
        w.grid(
            row=0,
            column=2,
            padx=2,
            sticky="w",
            )

    def __create_command_toolbar2(self, toolbar):
        self.__button_start = Tix.Button(
            toolbar,
            text=_("Start"),
            command=self.__action_start,
            state="disabled",
            width=8,
            )
        self.__button_run = Tix.Button(
            toolbar,
            text=_("Run"),
            command=self.__action_run,
            state="disabled",
            )
        self.__button_step = Tix.Button(
            toolbar,
            text=_("Step"),
            command=self.__action_step,
            state="disabled",
            )
        self.__button_pause = Tix.Button(
            toolbar,
            text=_("Pause"),
            command=self.__action_pause,
            state="disabled",
            )
        self.__button_abort = Tix.Button(
            toolbar,
            text=_("Abort"),
            command=self.__action_abort,
            state="disabled",
            )
        # 调用堆栈框架
        self.var_frame = Tix.IntVar()
        self.var_frame.set("")
        self.frame_menu = Tix.OptionMenu(
            toolbar,
            label=_("Execute Frame:"),
            disablecallback=True,
            variable=self.var_frame,
            command=self.__select_frame,
            options="menubutton.width 30",
            )
        self.__button_start.grid(
            row=0,
            column=0,
            padx=2,
            sticky="w",
            )
        self.__button_run.grid(
            row=0,
            column=1,
            padx=2,
            sticky="w",
            )
        self.__button_step.grid(
            row=0,
            column=2,
            padx=2,
            sticky="w",
            )
        self.__button_pause.grid(
            row=0,
            column=3,
            padx=2,
            sticky="w",
            )
        self.__button_abort.grid(
            row=0,
            column=4,
            padx=2,
            sticky="w",
            )
        self.frame_menu.grid(row=0, column=5, sticky="nesw")

    def __create_command_toolbar3(self, toolbar):
        _control = Tix.Control(
            toolbar,
            label=_("Step Interval(ms):"),
            step=100,
            variable=self.var_interval,
            value=self.var_interval.get(),
            min=0,
            max=10000,
            options=('decr.relief flat incr.relief flat '
                     'entry.width 5 entry.borderwidth 2 '
                     'entry.relief groove'
                     )
            )
        _control.grid(
            row=0,
            column=0,
            padx=5,
            )

    def __action_start(self):
        self.var_status.set("pause")
        try:
            self.algorithm_driver.start()
        except Exception, inst:
            self.var_status.set("open")
            self.console_view.fprint(_("Start algorithm failed:"))
            self.console_view.fprint_err(format_exc())

    def __action_abort(self):
        self.code_view.text.tag_remove("sel", "1.0", "end")
        self.algorithm_driver.abort()

    def __action_run(self):
        self.code_view.text.tag_remove("sel", "1.0", "end")
        self.var_status.set("run")
        self.algorithm_driver.run()

    def __action_pause(self):
        if self.var_status.get() == "run":
            self.var_status.set("pause")
            self.algorithm_driver.pause()

        else:
            self.algorithm_driver.resume()
            self.var_status.set("run")

    def __action_step(self):
        self.code_view.text.tag_remove("sel", "1.0", "end")
        self.algorithm_driver.step()

    def __action_open(self, filename=None):
        """打开一个算法文件. """
        if filename is None:
            filename = tkFileDialog.askopenfilename(
                parent=self,
                initialdir=self.history_path,
                defaultextension=".paf",
                filetypes=[(_("Pascal Algorithm Elf"), "*.paf")],
                )
        if filename:
            self.history_path = os.path.dirname(filename)
            try:
                self.para_view.remove_paras()
                self.code_view.clear()
                self.algorithm_driver.load(filename)
                self.var_info.set(filename)
                self.var_status.set("open")
            except Exception, inst:
                self.console_view.fprint(_("Open algorithm failed:"))
                self.console_view.fprint_err(format_exc())
                return

    def __action_parameter(self):
        """设置算法参数。"""
        self.para_view.deiconify()
        self.para_view.state("normal")
        self.para_view.transient(self)

    def __action_breakpoint(self):
        """显示断点列表。 """
        self.bp_view.deiconify()
        self.bp_view.state("normal")
        self.bp_view.transient(self)

    def __select_frame(self, entry):
        level = self.var_frame.get()
        label = self.frame_menu.menu.entrycget(level, "label")
        lineno = int(label.split('@')[-1])
        if lineno:
            self.code_view.goto_line(lineno)

    def clear(self):
        """清空全部动态视图的显示. """
        self.stack_view.clear()
        self.console_view.clear()
        self.data_view.clear()

    def __update_status(self, name, index, mode):
        """ 用于根据状态的不同设定命令按钮是否可用。

        """
        s = self.var_status.get()

        if s == "none":
            self.button_open["state"] = "normal"
            self.__button_start["state"] = "disabled"
            self.__button_abort["state"] = "disabled"
            self.__button_run["state"] = "disabled"
            self.__button_pause["state"] = "disabled"
            self.__button_step["state"] = "disabled"

        elif s == "open":
            self.button_open["state"] = "normal"
            self.__button_start["state"] = "normal"
            self.__button_abort["state"] = "disabled"
            self.__button_run["state"] = "disabled"
            self.__button_pause["state"] = "disabled"
            self.__button_step["state"] = "disabled"

        elif s == "run":
            self.button_open["state"] = "disabled"
            self.__button_start["state"] = "disabled"
            self.__button_abort["state"] = "normal"
            self.__button_run["state"] = "disabled"
            self.__button_pause["state"] = "normal"
            self.__button_step["state"] = "disabled"

        elif s == "pause":
            self.button_open["state"] = "disabled"
            self.__button_start["state"] = "disabled"
            self.__button_abort["state"] = "normal"
            self.__button_run["state"] = "normal"
            self.__button_pause["state"] = "disabled"
            self.__button_step["state"] = "normal"

        elif s == "finish":
            self.button_open["state"] = "normal"
            self.__button_start["state"] = "normal"
            self.__button_abort["state"] = "disabled"
            self.__button_run["state"] = "disabled"
            self.__button_pause["state"] = "disabled"
            self.__button_step["state"] = "disabled"

        # 不应该出现的非法算法状态
        else:
            assert False, ("unknow algorithm status %s" % s)

    def wm_delete_window(self):
        """终止已经启动的算法线程. """
        s = self.var_status.get()
        if s == "run" or s == "pause":
            self.algorithm_driver.abort()
            # 这里必须暂时释放对 GUI 的控制，否则回放线程
            # 无法执行，
            # ？？？需要释放什么呢
            # ？？？这个语句是什么呢
            # 原来是你 wait_variable
            self.wait_variable(self.var_status)
        self.master.quit()

    def open_algorithm(self, filename):
        if os.path.exists(filename):
            self.__action_open(filename)

    def is_playing(self):
        """检查算法是否正在运行。 """
        return self.var_status.get() == "run"

    def __create_time_indicator(self):
        # self.indicator_time = Tix.Label(
        #     self,
        #     bitmap="@images/timeIndicator.xbm"
        #     )
        # return
        __transparentcolor__ = "#F1F1F1"

        self.indicator_time = Tix.Toplevel(self)
        self.indicator_time.withdraw()
        try:
            self.indicator_time.attributes(
                "-transparentcolor",
                __transparentcolor__
                )
        except KeyError:
            pass
        _canvas = Tix.Canvas(
            self.indicator_time,
            borderwidth=0,
            width=16,
            height=16,
            cursor="none",
            bg=__transparentcolor__,
            highlightthickness=0,
            )
        _canvas.create_oval(
            0, 9, 6, 15,
            fill="#696969",
            width=0,
            )
        _canvas.create_line(
            6, 9, 15, 0,
            fill="black",
            arrow="last",
            smooth=True,
            arrowshape=(8, 10, 6),
            )
        _canvas.grid()

        self.indicator_time.deiconify()
        self.indicator_time.update_idletasks()
        self.indicator_time.overrideredirect(True)

    def update_time_indicator(self, inner, x=0, y=0):
        assert inner is not None
        if not inner.winfo_viewable():
            return

        _x = x + inner.winfo_rootx()
        _y = y + inner.winfo_rooty()
        self.indicator_time.geometry("+%d+%d" % (_x, _y))
        self.indicator_time.transient()
        sleep(self.var_internal.get() / 1000.0)

        # self.indicator_time.place(
        #     x=x + inner.winfo_rootx() - 16 - self.winfo_rootx(),
        #     y=y + inner.winfo_rooty() - self.winfo_rooty()
        #     )
        # sleep(self.var_internal.get() / 1000.0)

    def __emsg(self, ecode):
        """ 返回错误代码对应的消息格式字符串 """
        # 代码：1000
        # 参数：
        # 描述：保留
        #
        if ecode == 0:
            return ""

        # 代码：1001
        # 参数：算法名称
        # 描述：没有找到对应的算法
        #
        if ecode == 1001:
            return _("There is no algorithm '{0}' found")

        # 代码：1002
        # 参数：算法名称
        # 描述：算法类中缺少 prepare 方法
        #
        if ecode == 1002:
            return _("There is no function prepare found "
                     "in the algorithm class '{0}'")

        # 未知的错误代码
        assert False, "unknown error code %d" % ecode

class ConsoleFrame(Tix.Frame):
    """查看输出的窗口。 """
    def __init__(self, master=None):
        Tix.Frame.__init__(self, master)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        w = Tix.ScrolledText(
            self,
            scrollbar="none",
            )
        w.text.config(
            width=80,
            height=20,
            cursor="arrow",
            )
        w.text.bind("<KeyPress>", lambda e : "break")
        w.grid(sticky="nesw")
        self.text = w.text

    def fprint(self, msg, tag=None):
        self.text.insert("end", msg + "\n", (tag,))
        self.text.see("end")

    def fprint_err(self, msg):
        self.text.insert("end", msg + "\n", "e")
        self.text.see("end")

    def clear(self):
        self.text.delete("1.0", "end")

class SourceFrame(Tix.Frame):
    """查看源代码的窗口。 """
    def __init__(self, master, player):
        Tix.Frame.__init__(self, master)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        w = Tix.ScrolledText(
            self,
            scrollbar="none",
            )
        w.text.config(
            width=80,
            cursor="arrow",
            )
        w.text.bind("b", lambda e : self.insert_breakpoint())
        w.text.bind("p", lambda e : self.print_expr())
        w.text.bind("r", lambda e : self.insert_watchpoint('r'))
        w.text.bind("s", lambda e : self.step())
        w.text.bind("v", lambda e : self.insert_watchpoint('v'))
        w.text.bind("w", lambda e : self.insert_watchpoint('w'))
        w.text.bind("<KeyPress>", lambda e : "break")
        w.text.bind("<1>", self.__mouse_click)
        w.grid(sticky="nesw")
        self.text = w.text
        self.player = player

    def clear(self):
        self.text.delete("1.0", "end")

    def highlight_line(self, lineno):
        self.text.tag_remove("i", "1.0", "end")
        index1 = "%d.0" % lineno
        index2 = "%d.0" % (lineno + 1)
        self.text.tag_add("i", index1, index2)
        self.text.see(index1)
        # b = self.text.bbox(index1)
        # if not b:
        #     y = self.text.tk.call(self.text, "count", "-update",
        #                           "-ypixels", "@1,1", index1)
        #     self.text.yview_scroll(y, "pixels")

    def load(self, filename):
        f = open(filename)
        i = 1
        for line in f:
            self.text.insert(
                "end",
                "{0:4}: {1}".format(i, line.decode("utf-8")),
                )
            i += 1

    def step(self):
        self.player.algorithm_driver.step()
        return "break"

    def print_expr(self):
        try:
            expr = self.text.selection_get()
        except Exception:
            expr = ""
        if expr:
            self.player.console_view.fprint(_("Eval expression: ") + expr)
            try:
                level = self.player.var_frame.get()
                frame = self.player.algorithm_driver.stack_list[level][2]
                value = eval(expr, frame.f_globals, frame.f_locals)
                if isinstance(value, unicode):
                    value = value.encode('utf-8')
                self.player.console_view.fprint(str(value))
            except Exception, inst:
                self.player.console_view.fprint_err(str(inst))
        return "break"

    def goto_line(self, lineno):
        b = "%d.0" % lineno
        self.text.focus_set()
        self.text.mark_set("insert", b)
        self.text.see(b)

    def select_line(self, lineno):
        b = "%d.0" % lineno
        e = "%d.end" % lineno
        self.text.focus_set()
        self.text.tag_remove("sel", "1.0", "end")
        self.text.tag_add("sel", b, e)
        self.text.see(b)

    def __mouse_click(self, event):
        index = self.text.index("@%d, %d" % (event.x, event.y))
        lineno, col = map(int, index.split('.'))
        if col < 4:
            b = "%d.0" % lineno
            e = "%d.1" % lineno
            ch = self.text.get(b, e)
            if ch == '*':
                self.player.bp_view.remove(lineno=lineno)
                self.tk.call(self.text, 'replace', b, e, " ")
            else:
                self.player.bp_view.add_break(lineno=lineno)
                self.tk.call(self.text, 'replace', b, e, "*")

    def insert_watchpoint(self, mode='w'):
        try:
            varname = self.text.selection_get()
        except Exception:
            return
        condition = "'%s' in var['%s']" % (varname, mode)
        self.player.bp_view.add_watch(condition=condition)
        return "break"

    def insert_breakpoint(self):
        index = self.text.index("insert")
        if index:
            lineno = int(index.split(".")[0])
            b = "%d.0" % lineno
            e = "%d.1" % lineno
            ch = self.text.get(b, e)
            if ch == '*':
                self.player.bp_view.remove(lineno=lineno)
                self.tk.call(self.text, 'replace', b, e, " ")
            else:
                self.player.bp_view.add_break(lineno=lineno)
                self.tk.call(self.text, 'replace', b, e, "*")
        return "break"

class ViewParameter(Tix.Toplevel):
    def __init__(self, master):
        Tix.Toplevel.__init__(self, master)
        self.withdraw()
        self.geometry("-200-100")
        self.title(_("Algorithm Parameter"))
        self.protocol(
            'WM_DELETE_WINDOW',
            lambda : self.withdraw()
            )
        self.__create_widgets()

    def __create_widgets(self):
        frame = Tix.Frame(self)
        frame.rowconfigure(1, weight=1)
        frame.grid(sticky="nesw")
        self.para_frame = Tix.Frame(
            frame,
            borderwidth=2,
            relief="groove",
            pady=4,
            )
        self.para_frame.grid(sticky="we")
        w = Tix.Label(self.para_frame, text=_("Algorithm Parameters:"))
        w.grid(sticky="w")
        self.data_pool = datapool.DataPoolFrame(
            frame,
            filename="datapool.data",
            )
        self.data_pool.cmdbar.grid_forget()
        self.data_pool.grid(row=1, column=0, sticky="nesw")

    def remove_paras(self):
        for w in self.para_frame.winfo_children():
            w.destroy()
        self.data_pool.select_item("")

    def add_paras(self, varlist):
        w = Tix.Label(self.para_frame, text=_("Algorithm Parameters:"))
        w.grid(sticky="w")
        n = 1
        for k, v in varlist:
            name = k
            if name not in self.data_pool.items:
                try:
                    self.data_pool.insert(name, v)
                except Exception, inst:
                    self.data_pool.insert(name)

            w = Tix.Radiobutton(
                self.para_frame,
                value=name,
                text=name,
                variable=self.data_pool.var_itemname,
                command=lambda v=name : self.data_pool.select_item(v)
                )
            w.grid(row=0, column=n, padx=10, sticky="w")
            n += 1
        if varlist:
            varname = varlist[0][0]
            self.data_pool.var_itemname.set(varname)
            self.data_pool.select_item(varname)

class ViewStack(Tix.Frame):
    """树状结构显示调用堆栈。

    结点格式：函数名称：行号 - 文件名称：行号
    """
    def __init__(self, master):
        Tix.Frame.__init__(self, master)
        self.player = master
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        tree = Tix.Tree(
            self,
            options='separator "."',
            highlightthickness=0,
            )
        tree.grid(sticky="nesw")
        self.tree = tree

    def clear(self):
        self.tree.hlist.delete_all()
        self.player.frame_menu["disablecallback"] = True
        x = self.tk.call(self.player.frame_menu, "entries")
        for name in x.split():
            self.player.frame_menu.delete(name.strip("{}"))
        self.player.frame_menu["disablecallback"] = False
        return

    def push(self, node):
        level = self.player.frame_menu.menu.index("end")
        if level is None:
            level = 0
        else:
            level += 1
        co_name, co_lineno, frame = node
        co_varnames = frame.f_code.co_varnames
        co_argcount = frame.f_code.co_argcount
        argnames = co_varnames[1:co_argcount]
        paras = reduce(lambda x,y:x+", "+y, argnames, "")
        paras = paras[2:]
        text = "%d. %s(%s) @ %d" % (level + 1, co_name, paras, co_lineno)
        self.player.frame_menu.add_command(
            str(level),
            label=text,
            )
        self.player.var_frame.set(level)

    def pop(self):
        level = self.player.frame_menu.menu.index("end")
        if level is not None:
            self.player.frame_menu.delete(str(level))
            level -= 1
            self.player.var_frame.set(level)

    def set(self, stacklist):
        self.clear()
        name = ""
        level = 0
        for co_name, co_lineno, frame in stacklist:
            if name:
                name = name + "." + co_name
            else:
                name = co_name
            text = co_name + " : " + str(co_lineno)
            self.tree.hlist.add(name, text=text)
            self.player.frame_menu.add_command(
                str(level),
                label=text,
                )
            level += 1
        self.player.frame_menu["disablecallback"] = True
        self.tree.autosetmode()

class ViewBreakpoint(Tix.Toplevel):
    """显示当前的断点信息。"""
    def __init__(self, master):
        Tix.Toplevel.__init__(self, master)
        self.title(_("Breakpoint List"))
        self.geometry("-200-50")
        self.withdraw()
        self.player = master
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.protocol(
            'WM_DELETE_WINDOW',
            lambda : self.withdraw()
            )

        self.var_index = Tix.IntVar()
        self.var_index.set(0)

        w = Tix.ScrolledText(self, scrollbar="none")
        w.grid(sticky="nesw")
        self.text = w.text
        self.text.config(
            cursor="arrow",
            wrap="none",
            spacing1=1,
            insertwidth=0,
            )
        self.text.tag_configure(
            "title",
            relief="groove",
            borderwidth=2,
            )
        self.text.tag_configure(
            "field",
            relief="groove",
            )
        frame = Tix.Frame(self, pady=4, class_="Toolbar")
        frame.grid(row=1, column=0, sticky="we")
        frame.columnconfigure(0, weight=1)
        w = Tix.Button(
            frame,
            text=_("Remove"),
            command=self.remove,
            )
        w.grid(row=0, column=0, padx=20, sticky='w')
        w = Tix.Entry(frame, width=60)
        w.grid(row=0, column=1, sticky="e")
        self.entry = w
        w = Tix.Button(
            frame,
            text=_("Watch"),
            command=self.add_watch,
            )
        w.grid(row=0, column=1, sticky="e")

        w = Tix.Button(
            frame,
            text=_("Close"),
            command=self.withdraw,
            )
        w.grid(row=0, column=2, padx=10, sticky="e")

        self.text.bind("<1>", self.__select)
        self.text.bind("<KeyPress>", lambda e : "break")
        self.set([])

    def add_break(self, lineno=0):
        bp = [1, "", lineno, "", 0, "", None]
        bp_list = self.player.algorithm_driver.bp_list
        bp_list.append(bp)
        self.var_index.set(len(bp_list) - 1)
        self.set(bp_list)

    def add_watch(self, condition=None):
        if condition is None:
            condition = self.entry.get()
        if condition:
            bp = [1, "", 0, condition, 0, "", None]
            bp_list = self.player.algorithm_driver.bp_list
            bp_list.append(bp)
            self.var_index.set(len(bp_list) - 1)
            self.set(bp_list)

    def remove(self, lineno=None):
        bp_list = self.player.algorithm_driver.bp_list
        if lineno:
            index = None
            for bp in bp_list:
                if bp[2] == lineno:
                    index = bp_list.index(bp)
                    break
        else:
            index = self.var_index.get()
            if index >= len(bp_list):
                index = None
        if index is not None and bp_list:
            del bp_list[index]
            if index == 0:
                index = len(bp_list) - 1
            self.var_index.set(index - 1)
            self.set(bp_list)

    def __select(self, event):
        index = self.text.index("@%d,%d" % (event.x, event.y))
        lineno = self.var_index.get() + 2
        b = "%d.0" % lineno
        e = "%d.1" % lineno
        lineno = int(index.split('.')[0])
        if lineno:
            self.tk.call(self.text, 'replace', b, e, " ")
            b = "%d.0" % lineno
            e = "%d.1" % lineno
            self.tk.call(self.text, 'replace', b, e, "*")
            self.var_index.set(lineno - 2)

    def get(self):
        """得到当前选中的断点索引。
        """
        return self.var_index.get()

    def set(self, bplist):
        """显示断点列表。
        [ 是否可用，函数名称，行号，条件表达式，命中次数，表达式的当前值 ]
        """
        # self.text.config(state="normal")
        self.text.delete("1.0", "end")
        msg = "%4s %-16s %s\n" % ("#", "Location", "Watch Expression")
        self.text.insert("end", msg, ('title',))

        i = 1
        for bp in bplist:
            flag, co_name, lineno, expr, hits, action, value = bp
            self.text.insert(
                "end",
                "%4d %-16s %s\n" % (i, lineno, expr),
                ('field',),
                )
            i += 1
        lineno = self.var_index.get() + 2
        if lineno:
            b = "%d.0" % lineno
            e = "%d.1" % lineno
            self.tk.call(self.text, 'replace', b, e, "*")
        # self.text.config(state="disabled")

def decode_handler(e):
    if type(e) is UnicodeDecodeError:
        s = e.args[1]
        text = s[e.start:].strip().decode('utf-8')
    return (text, -1)
        
def main(filename=None):
    os.chdir(os.path.normpath(os.path.dirname(sys.argv[0])))
    # 读取配置文件
    try:
        f = open("algorithm-elf.pycfg")
        options = eval(f.read())
        lang = options["lang"]              # 检查配置文件是否是字典类型
    except Exception, inst:
        sys.stderr.write("Warning: reading configure file failed: " + str(inst))
        lang = None
        options = {}
    mysite.set_locale("algorithm-elf", lang=lang)
    root = Tix.Tk()
    try:
        w = AlgorithmPlayer(root, options)
        root.title(about.get_product_info("AppName"))
        # 默认图标和最大化窗口
        try:
            # Windows 和 MacOS，使用设置 state 的方式
            if sys.platform == 'win32':
                root.state("zoomed")
                root.iconbitmap(default="main.ico")
            # On X11, 使用修改属性的方式最大化
            elif sys.platform == 'linux2':
                root.attributes("-zoomed", True)
                root.iconbitmap("main.ico")
        except (KeyError, Tkinter.TclError):
            pass
        root.focus_set()
        w.grid(sticky="nesw")
        if filename:
            w.after_idle(w.open_algorithm, filename)
        w.mainloop()
    except Exception, inst:
        root.tk.call(
            "tk_messageBox",
            "-title", _("Uncaught Exception"),
            "-message", str(inst),
            "-detail", format_exc(),
            )

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(filename=sys.argv[1])
    else:
        main()