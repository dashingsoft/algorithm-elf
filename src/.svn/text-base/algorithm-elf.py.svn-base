#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#############################################################
#                                                           #
#      版权所有 2009 - 2010 德新软件公司。保留全部权利。    #
#                                                           #
#      数据结构算法助手                                     #
#                                                           #
#      版本区间：1.0.0 -                                    #
#                                                           #
#############################################################
#
# @文件：algorithm-elf.py
#
# @作者：赵俊德(jondy.zhao@gmail.com)
#
# @创建日期: 2010/02/07
#
# @文件说明：
#
# 算法精灵的主启动文件，进入算法集成编辑环境。
#

#: 导入模块
import os
import sys
import shlex
import Tkinter
import Tix
import tkMessageBox
import tkFileDialog
import tkFont
import re
import string
import webbrowser
import traceback
import subprocess

import mysite
import about
import register
import datapool
import buildprocess
import pascal
#;

#: 图片数据
images_data = { 
    "close" : """
    #define close_width 12
    #define close_height 12
    static unsigned char close_bits[] = {
      0xff, 0x0f, 0x03, 0x0c, 0x05, 0x0a, 0x09, 0x09,
      0x91, 0x08, 0x61, 0x08, 0x61, 0x08, 0x81, 0x09,
      0x09, 0x09, 0x05, 0x0a, 0x03, 0x0c, 0xff, 0x0f
    };
    """,
    
    "hand" : '''/* XPM */
    static char *h_point[] = {
    "32 32 6 1 12 3",
    "  c #000000",
    "! c #000080",
    "# c #808080",
    "$ c #C0C0C0",
    "% c #FFFFFF",
    "& c None",
    "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",
    "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",
    "&&&&&&&&&&&&$$&&&&&&&&&&&&&&&&&&",
    "&&&&&&&&&&&#%$ &&&&&&&&&&&&&&&&&",
    "&&&&&&&&&&&#%$ &&&&&&&&&&&&&&&&&",
    "&&&&&&&&&&&#%$ &&&&&&&&&&&&&&&&&",
    "&&&&&&&&&&&#%$ ##&&&&&&&&&&&&&&&",
    "&&&&&&&&&&&#%$ %$ ##&&&&&&&&&&&&",
    "&&&&&&&&&&&#%$ %$ %$ &&&&&&&&&&&",
    "&&&&&&&&&&&#%$ %$ %$ ##&&&&&&&&&",
    "&&&&&## &&&#%$ %$ %$ %$ &&&&&&&&",
    "&&&&&#%$ &&#%%#%%#%$ %$ &&&&&&&&",
    "&&&&&&#%$ &#%%%%%%%%#%$ &&&&&&&&",
    "&&&&&&#%%$  %%%%%%%%%%$ &&&&&&&&",
    "&&&&&&&#%%$ %%%%%%%%%%$ &&&&&&&&",
    "&&&&&&&#%%% %%%%%%%%%%$ &&&&&&&&",
    "&&&&&&&&#%%%%%%%%%%%%%$ &&&&&&&&",
    "&&&&&&&&#%%%%%%%%%%%%$ &&&&&&&&&",
    "&&&&&&&&&#%%%%%%%%%%%$ &&&&&&&&&",
    "&&&&&&&&&#%%%%%%%%%%%$ &&&&&&&&&",
    "&&&&&&&&&&#%%%%%%%%%$ &&&&&&&&&&",
    "&&&&&&&&&&&#%%%%%%%%$ &&&&&&&&&&",
    "&&&&&&&&&&&&#%%%%%%$ &&&&&&&&&&&",
    "&&&&&&&&&&&&#%%%%%%$ &&&&&&&&&&&",
    "&&&&&&&&&&&&!!       &&&&&&&&&&&",
    "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",
    "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",
    "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",
    "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",
    "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",
    "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",
    "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
    };
    ''',
    }
    

class AlgorithmElf(Tix.Frame):
    """算法集成编辑窗口."""

    # 文件打开的历史路径
    history_path = ""
    
    def __init__(self, master=None, options={}):
        Tix.Frame.__init__(self, master)        
        self.options = options
        self.hand_cursor = Tix.Image("pixmap", data=images_data["hand"])

        master.option_add("*relief", "flat")
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

        opt = options["style"].get("font", "TkFixedFont")
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
        master.option_add("*PanedWindow.showHandle", "False")
        master.option_add("*Panedwindow.sashWidth", "2")
        master.option_add("*Panedwindow.sashRelief", "groove")
    
        self.indent_width = options["style"].get("indent-width", 2)
        
        # 配置主窗口属性
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)
        self.rowconfigure(0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2)
        self.columnconfigure(0, weight=1)

        self.symbol_list = [pascal.kwlist]
        x = filter(lambda k : k[0] != "_", dir(pascal))
        x.remove("kwlist")
        self.symbol_list.append(x)
        self.symbol_list.append([])

        # 创建子控件
        self.__create_widgets()
        self.__configure_widgets()
        self.datapool = datapool.DataPool(self, filename="datapool.data")
        
        # 绑定窗口退出事件
        master.protocol(
                'WM_DELETE_WINDOW',
                lambda : self.__action_quit()
                )

        # 设定属性
        self.__set_status("none")
        self.__filename = None
        self.__builder = self.options.get("builder")
        self.__player = self.options.get("player")

    def __create_widgets(self):
        #: 创建工具栏
        _frame = Tkinter.Frame(
            self,
            class_="Coolbar",
            borderwidth=2,
            )
        _frame.grid(sticky="we")
        _toolbar1 = Tkinter.Frame(
            _frame,
            class_="Toolbar",
            padx=5,
            pady=2,
            borderwidth=1,
            )
        _toolbar2 = Tkinter.Frame(
            _frame,
            class_="Toolbar",
            padx=5,
            pady=2,
            borderwidth=1,
            )
        _toolbar3 = Tkinter.Frame(
            _frame,
            class_="Toolbar",
            padx=5,
            pady=2,
            borderwidth=1,
            )
        _toolbar1.grid(
            row=0,
            column=0,
            padx=5,
            sticky="w",
            )
        _toolbar2.grid(
            row=0,
            column=1,
            padx=5,
            sticky="w",
            )
        _toolbar3.grid(
            row=0,
            column=2,
            padx=5,
            sticky="w",
            )

        self.button_new = Tkinter.Button(
            _toolbar1,
            command=self.__action_new,
            text=_("New"),
            )
        self.button_open = Tkinter.Button(
            _toolbar1,
            command=self.__action_open,
            text=_("Open"),
            )
        self.button_save = Tkinter.Button(
            _toolbar1,
            command=self.__action_save,
            text=_("Save"),
            )
        self.button_new.grid(
            row=0,
            column=0,
            padx=2,
            sticky="w",
            )
        self.button_open.grid(
            row=0,
            column=1,
            padx=2,
            sticky="w",
            )
        self.button_save.grid(
            row=0,
            column=2,
            padx=2,
            sticky="w",
            )

        self.button_undo = Tkinter.Button(
            _toolbar2,
            command=self.__action_undo,
            text=_("Undo"),
            )
        self.button_redo = Tkinter.Button(
            _toolbar2,
            command=self.__action_redo,
            text=_("Redo"),
            )
        self.button_undo.grid(
            row=0,
            column=0,
            padx=2,
            sticky="w",
            )
        self.button_redo.grid(
            row=0,
            column=1,
            padx=2,
            sticky="w",
            )

        self.button_build = Tkinter.Button(
            _toolbar3,
            text=_("Build"),
            command=self.__action_build,
            )
        self.button_play = Tkinter.Button(
            _toolbar3,
            command=self.__action_play,
            text=_("Play"),
            )
        self.button_datapool = Tkinter.Button(
            _toolbar3,
            command=self.__action_datapool,
            text=_("Data Pool"),
            )
        self.button_build.grid(
            row=0,
            column=0,
            padx=2,
            sticky="w",
            )
        self.button_play.grid(
            row=0,
            column=1,
            padx=2,
            sticky="w",
            )
        self.button_datapool.grid(
            row=0,
            column=2,
            padx=2,
            sticky="w",
            )

        #: 创建编辑区
        frame = Tkinter.Frame(self)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.grid(row=1, sticky="nesw")
        
        w = Tkinter.PanedWindow(
            frame,
            orient="horizontal"
            )
        w.grid(sticky="nesw")
        self.paned_window = w

        w = Tix.ScrolledText(frame, scrollbar="none")
        self.editor = w.text
        self.paned_window.add(w, minsize=300, sticky="nesw")
        self.editor.configure(
            undo=True,
            autoseparators=True,
            maxundo=-1,
            )

        #: 创建编译消息窗口
        frame = Tix.Frame(self.paned_window)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)
        self.paned_window.add(frame, minsize=300, sticky="nesw")

        bg=self.editor["bg"]
        fg=self.editor["fg"]        
        frame1 = Tix.Frame(
            frame, 
            borderwidth=1, 
            bg=bg,
            relief="groove",
            )
        frame1.grid(sticky="we")
        frame1.columnconfigure(0, weight=1)
        w = Tix.Label(
            frame1,
            bg=bg,
            fg=fg,
            text=_("Compile Message"),
            )
        w.grid(sticky="nesw")
        self.img_close = Tix.BitmapImage(
            background=bg,
            foreground=fg,
            data=images_data["close"],
            )
        w = Tix.Button(
            frame1,
            background=bg,
            foreground=fg,
            borderwidth=0,
            activebackground=bg,                        
            image=self.img_close,
            command=lambda : self.paned_window.forget(self.__compile_frame)
            )
        w.grid(row=0, column=1, sticky="e")

        w = Tix.ScrolledText(frame, scrollbar="none")
        w.grid(row=1, column=0, sticky="nesw")
        self.compile_text = w.text
        self.compile_text.configure(
            cursor="arrow",
            insertwidth=0,
            state="disabled",
            )
        self.__compile_frame = frame

        #: 创建状态栏
        frame = Tkinter.Frame(self)
        frame.grid(row=2, sticky="we")
        self.var_msg = Tkinter.StringVar()
        w = Tkinter.Label(frame, textvariable=self.var_msg)
        w.grid(sticky="we")

        #: 创建主菜单
        _menubar = Tkinter.Menu(self.master)
        _menu_file = Tkinter.Menu(_menubar)
        _menu_edit = Tkinter.Menu(_menubar)
        _menu_algorithm = Tkinter.Menu(_menubar)
        _menu_help = about.create_help_menu(_menubar)

        _menubar.add_cascade(
            menu=_menu_file,
            label=_("File"),
            )
        _menubar.add_cascade(
            menu=_menu_edit,
            label=_("Edit")
            )
        _menubar.add_cascade(
            menu=_menu_algorithm,
            label=_("Algorithm")
            )
        _menubar.add_cascade(
            menu=_menu_help,
            label=_("Help")
            )

        _menu_samples = Tkinter.Menu(_menu_file)
        _menu_samples.add_command(
            command=lambda : self.__action_open_example(0),
            label=_("Hanoi(hanoi.paf)"),
            )
        _menu_samples.add_separator()
        _menu_samples.add_command(
            command=lambda : self.__action_open_example(1),
            label=_("Tree PreOrder(preorder.paf)"),
            )
        _menu_samples.add_command(
            command=lambda : self.__action_open_example(2),
            label=_("Tree InOrder(inorder.paf)"),
            )
        _menu_samples.add_command(
            command=lambda : self.__action_open_example(3),
            label=_("Tree PostOrder(postorder.paf)"),
            )
        _menu_samples.add_separator()
        _menu_samples.add_command(
            command=lambda : self.__action_open_example(4),
            label=_("Straight Sort(starightsort.paf)"),
            )
        _menu_samples.add_command(
            command=lambda : self.__action_open_example(5),
            label=_("Quick Sort(quicksort.paf)"),
            )
        _menu_samples.add_command(
            command=lambda : self.__action_open_example(6),
            label=_("Merge Sort(mergesort.paf)"),
            )

        _menu_file.add_command(
            command=self.__action_new,
            label=_("New"),
            )
        _menu_file.add_command(
            command=self.__action_open,
            label=_("Open"),
            )
        _menu_file.add_cascade(
            menu=_menu_samples,
            label=_("Open Samples"),
            )
        _menu_file.add_separator()
        _menu_file.add_command(
            command=self.__action_save,
            label=_("Save"),
            )
        _menu_file.add_command(
            command=self.__action_save,
            label=_("Save As..."),
            )
        _menu_file.add_separator()
        _menu_file.add_command(
            command=self.__action_close,
            label=_("Close"),
            )
        _menu_file.add_separator()
        _menu_file.add_command(
            label=_("Data Pool"),
            command=self.__action_datapool,
            )        
        _menu_file.add_command(
            label=_("Show Compile Window"),
            command=lambda : ( not self.compile_text.winfo_viewable() and
                               self.paned_window.add(self.__compile_frame))
            )
        _menu_file.add_separator()
        _menu_file.add_command(
            command=self.__action_quit,
            label=_("Quit"),
            )

        _menu_edit.add_command(
            label=_("Undo"),
            )
        _menu_edit.add_command(
            label=_("Redo"),
            )
        _menu_edit.add_separator()
        _menu_edit.add_command(
            label=_("Find"),
            )
        _menu_edit.add_command(
            label=_("Replace"),
            )
        _menu_edit.add_separator()
        _menu_edit.add_command(
            label=_("Select All"),
            )
            
        _menu_algorithm.add_command(
            label=_("Build"),
            command=self.__action_build,
            )
        _menu_algorithm.add_command(
            label=_("Play"),
            command=self.__action_build,
            )
        self.master.config(menu=_menubar)

    def __configure_widgets(self):
        
        self.compile_text.bind("<KeyPress>", lambda e : "break")
        
        # 绑定错误信息的 tag
        self.compile_text.tag_config("e1", underline=1)
        self.compile_text.tag_bind(
            "e1",
            "<Button-1>",
            self.__locate_error_line
            )
        self.compile_text.tag_bind(
            "e1",
            "<Enter>",
            lambda e : self.compile_text.config(cursor="arrow"),
            )
        self.compile_text.tag_bind(
            "e1",
            "<Leave>",
            lambda e : self.compile_text.config(cursor="arrow"),
            )
        
        # 快捷键绑定
        self.editor.bind(
            "<Control-s>",
            lambda e:(self.button_save['state'] == "normal"
                      and self.__action_save())
            )

        # 绑定显示标签
        fg = self.editor["foreground"]
        bg = self.editor["background"]
        opts = self.options["style"]
        self.editor.tag_config(
            "s_string",
            foreground=opts["string"].get("foreground", fg),
            )
        self.editor.tag_config(
            "s_keyword",
            foreground=opts["keyword"].get("foreground", fg),
            )
        self.editor.tag_config(
            "s_comment",
            foreground=opts["comment"].get("foreground", fg),
            )
        self.editor.tag_config(
            "s_match",
            foreground=opts["match"].get("foreground", fg),
            background=opts["match"].get("background", bg),
            )
        # 绑定事件
        self.editor.bind("<KeyRelease>", self.__keyrelease_event)
        self.editor.bind("<Button-1>", self.__mouse_click_event)
        self.editor.bind("<Return>", self.auto_indent_newline)
        self.editor.bind("<Alt-slash>", self.auto_symbol_complete)

    def __set_status(self, value):
        """设定算法文档的状态.

        算法文档状态的含义：

        none，没有任何算法文档打开；
        new，新建的文档，还没有文件名称；
        open，打开的文档；
        build，当前算法正在编译构建；
        play，当前算法正在演示。

        算法文档在不同的状态可以进行的操作不相同。

        """
        self.file_status = value

        if value == "none":
            self.editor.edit_reset()
            self.editor.edit_modified(False)
            self.editor.delete("1.0", "end")
            self.editor['state'] = "disabled"

            self.button_new['state'] = "normal"
            self.button_open['state'] = "normal"
            self.button_save['state'] = "disabled"
            self.button_build['state'] = "disabled"
            self.button_play['state'] = "disabled"
            self.button_redo['state'] = "disabled"
            self.button_undo['state'] = "disabled"

            _menubar = self.master.nametowidget(self.master.cget("menu"))
            _menu = _menubar.nametowidget(_menubar.entrycget(0, "menu"))
            _menu.entryconfigure(0, state="normal")
            _menu.entryconfigure(1, state="normal")
            _menu.entryconfigure(2, state="normal")
            _menu.entryconfigure(4, state="disabled")
            _menu.entryconfigure(5, state="disabled")
            _menu.entryconfigure(7, state="disabled")
            _menubar.entryconfigure(1, state="disabled")
            _menubar.entryconfigure(2, state="disabled")

            self.var_msg.set(_("No algorithm is opened"))
            self.master.title(_("Algorithm Elf"))
            self.__filename = None


        elif (value == "new") or (value == "open"):

            self.editor['state'] = "normal"
            self.editor.focus_set()
            self.editor.edit_reset()
            self.editor.edit_modified(False)

            self.button_new['state'] = "normal"
            self.button_open['state'] = "normal"
            self.button_save['state'] = "normal"
            self.button_build['state'] = "normal"
            self.button_play['state'] = "normal"
            self.button_redo['state'] = "normal"
            self.button_undo['state'] = "normal"

            _menubar = self.master.nametowidget(self.master.cget("menu"))
            _menu = _menubar.nametowidget(_menubar.entrycget(0, "menu"))
            _menu.entryconfigure(0, state="normal")
            _menu.entryconfigure(1, state="normal")
            _menu.entryconfigure(2, state="normal")
            _menu.entryconfigure(4, state="normal")
            _menu.entryconfigure(5, state="normal")
            _menu.entryconfigure(7, state="normal")
            _menubar.entryconfigure(1, state="normal")
            _menubar.entryconfigure(2, state="normal")

            if self.__filename is None:
                self.var_msg.set(_("New algorithm file"))
                self.master.title(_("Algorithm Elf - New"))
            else:
                self.var_msg.set(self.__filename)
                self.master.title(
                    _("Algorithm Elf - {0}").format(self.__filename)
                    )

        elif (value == "building") or (value == "play"):
            self.editor['state'] = "disabled"
            self.button_new['state'] = "disabled"
            self.button_open['state'] = "disabled"
            self.button_save['state'] = "disabled"
            self.button_build['state'] = "disabled"
            self.button_play['state'] = "disabled"
            self.button_redo['state'] = "disabled"
            self.button_undo['state'] = "disabled"

            _menubar = self.master.nametowidget(self.master.cget("menu"))
            _menu = _menubar.nametowidget(_menubar.entrycget(0, "menu"))
            _menu.entryconfigure(0, state="disabled")
            _menu.entryconfigure(1, state="disabled")
            _menu.entryconfigure(2, state="disabled")
            _menu.entryconfigure(4, state="disabled")
            _menu.entryconfigure(5, state="disabled")
            _menu.entryconfigure(7, state="disabled")
            _menubar.entryconfigure(1, state="disabled")
            _menubar.entryconfigure(2, state="disabled")

        else:
            assert(False)

    def __action_new(self):
        if self.__action_close():
            self.__set_status("new")

    def __action_open(self, filename=None):
        if filename is None:
            filename = tkFileDialog.askopenfilename(
                parent=self,
                initialdir=self.history_path,
                defaultextension=".paf",
                filetypes=[(_("Pascal Algorithm Elf"), "*.paf")],
                )
        if filename:
            if self.__action_close():
                filename = os.path.normpath(filename)
                self.history_path = os.path.dirname(filename)
                if self.__open_algorithm(filename):
                    self.__filename = filename
                    self.__set_status("open")

    def __action_open_example(self, index=0):
        if index == 0:
            self.__action_open(filename=os.path.join("examples", "hanoi.paf"))
        elif index == 1:
            self.__action_open(filename=os.path.join("examples", "preorder.paf"))
        elif index == 2:
            self.__action_open(filename=os.path.join("examples", "inorder.paf"))
        elif index == 3:
            self.__action_open(filename=os.path.join("examples", "postorder.paf"))
        elif index == 4:
            self.__action_open(filename=os.path.join("examples", "straightsort.paf"))
        elif index == 5:
            self.__action_open(filename=os.path.join("examples", "quicksort.paf"))
        elif index == 6:
            self.__action_open(filename=os.path.join("examples", "mergesort.paf"))

    def __action_save(self):
        self.__save_algorithm()
        self.editor.edit_modified(False)
        self.editor.edit_reset()

    def __action_close(self):
        _savechanged = False
        if self.editor.edit_modified():
            _answer = tkMessageBox.askyesnocancel(
                parent=self.master,
                title=about.get_product_info("AppName"),
                message=_("The text in the file has changed. "
                          "Do you want to save it?"),
                )
            if _answer is None:
                return False
            elif _answer:
                _savechanged = True
            else:
                _savechanged = False
        if self.__close_algorithm(_savechanged):
            self.__set_status("none")
            return True
        return False

    def __action_quit(self):
        if self.__action_close():
            self.master.destroy()

    def __action_build(self):
        if not self.__save_algorithm():
            return False
        self.__build_algorithm()

    def __action_play(self):
        self.__play_algorithm()

    def __action_undo(self):
        try:
            self.editor.edit_undo()
        except Exception, inst:
            pass

    def __action_datapool(self):
        """设置算法参数. """
        self.datapool.deiconify()
        self.datapool.state("normal")
        self.datapool.focus_set()
        self.datapool.transient()

    def __action_redo(self):
        try:
            self.editor.edit_redo()
        except Exception, inst:
            pass
    def __action_help(self):
        _file = "dshelp_%s.html" % self.options["lang"]
        if not os.path.exists(_file):
            _file = "dshelp.html"

        if os.path.exists(_file):
            webbrowser.open(_file)
        else:
            tkMessageBox.showinfo(
                title=about.get_product_info("AppName"),
                message=_("No help file is installed."),
                )

    def __action_about(self):
        w = about.AboutDialog(self)
        w.go()
        self.wait_window(w)

    def __action_make_license(self):
        _dialog = register.RegisterDialog()
        _dialog.go()
        self.master.focus_get()

    def __open_algorithm(self, filename):
        self.editor.configure(state="normal")
        self.editor.delete("1.0", "end")
        try:
            _file = open(filename, "r")
            _source = _file.read()
            self.editor.insert("end", _source.strip())
            _file.close()
            self.__highlight_syntax("1.0", "end", True)
            return True
        except Exception, inst:
            tkMessageBox.showinfo(
                title=about.get_product_info("AppName"),
                message=_("Could not open file: {0}").format(inst)
                )
            return False

    def __close_algorithm(self, savechanged=True):
        if self.file_status == "none":
            return True
        elif self.file_status == "building":
            if tkMessageBox.askyesno(
                title=about.get_product_info("AppName"),
                message=_("Building process is running, do you really "
                          "want to abort the process and quit?")
                ):
                self.build_process.kill()
                return True
            else:
                return False
        elif self.file_status == "play":
            tkMessageBox.showinfo(
                title=about.get_product_info("AppName"),
                message=_("Algorithm is playing, can not close it")
                )
            return False
        else:
            assert((self.file_status == "new")
                   or (self.file_status == "open"))
            if self.editor.edit_modified() and savechanged:
                if not self.__save_algorithm():
                    return False
            self.editor.delete("1.0", "end")
            return True

    def __save_algorithm(self):
        if self.__filename is None:
            _filename = tkFileDialog.asksaveasfilename(
                defaultextension=".paf",
                filetypes=[(_("Pascal Algorithm Elf"), "*.paf")],
                )
            if _filename == "":
                return False
            self.__filename = _filename
            self.var_msg.set(_filename)
            self.master.title(_("Algorithm Elf - {0}").format(_filename))

        assert(isinstance(self.__filename, basestring))

        # 保存文件
        try:
            _file = open(self.__filename, 'w')
            text = self.editor.get("1.0", "end").encode('utf-8')
            _file.write(text)
            _file.close()
            return True
        except Exception, inst:
            tkMessageBox.showinfo(
                title=about.get_product_info("AppName"),
                message=_("Could not save file: {0}").format(inst)
                )
            return False

    def __build_algorithm(self):
        """编译当前算法文件."""
        if self.__builder is None:
            tkMessageBox.showinfo(
                title=about.get_product_info("AppName"),
                message=_("Unsupport platform to build")
                )
            return

        ## 编译窗口的第一种显示方式，使用弹出对话框
        # _build_window = Tix.Toplevel(self.master)
        # _build_window.rowconfigure(0, weight=1)
        # _build_window.columnconfigure(0, weight=1)
        # _build_window.protocol(
        #     "WM_DELETE_WINDOW",
        #     lambda : (self.__set_status("open")
        #               or _build_window.destroy())
        #     );
        # _scrolltext = Tix.ScrolledText(_build_window)
        # _scrolltext.grid(sticky="nesw")
        # self.compile_text = _scrolltext.subwidget("text")
        # self.compile_text.bind(
        #     "<Double-Button-1>",
        #     lambda e: (self.__locate_error_line()
        #                or self.__set_status("open")
        #                or _build_window.destroy())
        #     )
        # _build_window.geometry("+%d+%d" % (self.winfo_rootx() + 100,
        #                           self.winfo_rooty() + 100))
        # _build_window.transient(self.master)
        # _build_window.grab_set()
        # _build_window.focus_set()

        ## 编译窗口的第二种显示方式，使用 pane window
        if not self.compile_text.winfo_viewable():
            self.paned_window.add(self.__compile_frame)
        self.compile_text.config(state="normal")
        self.compile_text.delete("1.0", "end")

        try:
            _algorithm_name = os.path.splitext(
                os.path.basename(self.__filename)
                )[0]
            self.build_process = buildprocess.BuildProcess(
                [self.__builder, self.__filename],
                output=self.__show_building_message,
                clean=self.__after_build,
                )
            # self.build_process = buildprocess.BuildProcess(
            #     ["ping", "-t", "127.0.0.1"],
            #     output=self.__show_building_message,
            #     clean=self.__after_build,
            #     )
            self.__set_status("building")
        except Exception, inst:
            self.__show_building_message(str(inst))

    def __after_build(self):
        self.__set_status("open")
        self.compile_text.config(state="disabled")

    def __locate_error_line(self, e):
        """定位发生语法错误的行. """
        linetext = self.compile_text.get("current linestart", "current lineend")
        m = re.match(r"^Error:([0-9]+):", linetext)
        if m is not None:
            lineno = int(m.group(1))
            self.editor.tag_remove("sel", "1.0", "end")
            self.editor.tag_add("sel", "%d.0" % lineno, "%d.end" % lineno)
            self.editor.mark_set("insert", "%d.0" % lineno)
            self.editor.see("%d.0" % lineno)
            self.editor.after_idle(self.editor.focus_set)

    def __show_building_message(self, msg):
        m = re.match(r"^Error:([0-9]+):", msg)
        if m is not None:
            self.compile_text.insert(
                "end",
                m.group(0),
                ("e1",)
                )
            self.compile_text.insert(
                "end",
                msg[len(m.group(0)):]
                )
        else:
            self.compile_text.insert("end", msg)
        self.compile_text.see("end")

    def __play_algorithm(self):
        """演示算法执行过程."""
        cmdlist = shlex.split(self.__player)
        cmdlist.append(self.__filename)
        subprocess.Popen(cmdlist)
        


    def __get_ignore_tag(self, index):
        """得到当前位置的可以忽略的标签名称。

        c 表示注释，
        s 表示字符串，
        None 表示不可以忽略。
        """
        tags = self.editor.tag_names(index)
        if "s" in tags:
            return "s"
        elif "c" in tags:
            return "c"
        else:
            return None

    def __highlight_syntax(self, index1, index2, refresh=False):
        """设置区域内的字符和注释标签，设置语法高亮标签。

        注意：不论语法高亮模式是否打开，都必须设置字符和注释
              的语法标签，即 's' 和 'c'。

        而其他的语法显示标签只有当语法高亮模式打开时候才增加。

        """
        # 对齐区域: 开始必须是一个词，结束必须是行尾
        # 如果是在字符串中，那么取字符串开头或者结束
        # 如果是在注释中，那么取注释的开头或者结尾
        index1 = self.editor.index(index1 + " wordstart")
        x = self.__get_ignore_tag(index1)
        if x:
            s = self.editor.tag_prevrange(x, index1)
            if s and self.editor.compare(s[0], "<", index1):
                index1 = self.editor.index(s[0])

        index2 = self.editor.index(index2 + " lineend")
        x = self.__get_ignore_tag(index2)
        if x:
            s = self.editor.tag_prevrange(x, index2)
            if s and self.editor.compare(s[1], ">", index2):
                index2 = self.editor.index(str(s[1]) + " lineend")

        # 删除原来区域中的标签 s_ 开头的标签
        self.editor.tag_remove("s_comment", index1, index2)
        self.editor.tag_remove("s_keyword", index1, index2)
        self.editor.tag_remove("s_name", index1, index2)
        self.editor.tag_remove("s_string", index1, index2)

        self.editor.tag_remove("s", index1, index2)
        self.editor.tag_remove("c", index1, index2)

        if refresh:
            del self.symbol_list[2][:]
            words = self.symbol_list[2]
        # 重新添加标签
        while 1:
            # 忽略所有的空白字符
            index1 = self.editor.search(
                "[^[:space:]]",
                index1,
                elide=True,
                regexp=True,
                stopindex=index2
                )
            if index1 == "":
                break

            ch = self.editor.get(index1)

            # 以 { 开头的设定增加 s_comment
            if ch == "{":
                s2 = self.editor.search(
                    "}",
                    index1,
                    elide=True,
                    stopindex=index2)
                if s2:
                    s2 += " +1c"
                    self.editor.tag_add("c", index1, s2)
                    self.editor.tag_add("s_comment", index1, s2)
                index1 = s2
                continue

            # 以 ' 开头的是字符串
            if ch in "'":
                s1 = index1
                while 1:
                    s1 = self.editor.search(
                        ch,
                        s1 + " +1c",
                        elide=True,
                        stopindex=index2,
                        )
                    if s1 == "":
                        s2 = index2 
                        break
                    ch1 = self.editor.get(s1 + " +1c")
                    if ch1 == "'":
                        s1 = s1 + " +1c"
                        continue
                    else:
                        s2 = self.editor.index(s1 + " +1c")
                        break
                self.editor.tag_add("s", index1, s2)
                self.editor.tag_add("s_string", index1, s2)
                index1 = s2
                continue

            # 看是不是关键词
            if ch in string.letters + "_":
                s1 = self.editor.search(
                    r"[^a-zA-Z0-9_]",
                    index1,
                    elide=True,
                    regexp=True,
                    stopindex=index1 + " lineend",
                    )
                if s1 == "":
                    s1 = self.editor.index(index1 + " lineend")
                name = self.editor.get(index1, s1)
                if (name.lower() in self.symbol_list[0] 
                     or name in self.symbol_list[1]):
                    self.editor.tag_add("s_keyword", index1, s1)
                elif refresh and words.count(name) == 0:
                    words.append(name)
                index1 = s1
                continue

            # 忽略其他任何字符
            index1 = self.editor.search(
                "[a-zA-Z_'{]",
                index1,
                elide=True,
                regexp=True,
                stopindex=index2,
                )
            if index1 == "":
                break

    def __guess_indent(self, index):
        """默认就是上一行的缩进。"""
        # 找到向上的第一个非空行
        x = self.editor.search(
            "[^[:space:]]",
            index,
            backwards=True,
            elide=True,
            regexp=True,
            stopindex="1.0",
            )
        if x == "":
            return 0

        word = self.editor.get(x + " wordstart", x + " wordend")
        if word.lower() in ("begin", "do", "of", "then"):
            x = self.editor.search(
                "^[[:blank:]]*(if|while|for|repeat|until|"
                "begin|end|procedure|programe|case)",
                x,
                backwards=True,
                elide=True,
                regexp=True,
                nocase=True,
                stopindex="1.0",
                )
            if x == "":
                return 0
        x = self.editor.search(
            "[^[:blank:]]",
            x + " linestart",
            elide=True,
            regexp=True,
            stopindex=x + " lineend",
            )
        if x == "":
            return 0
        indent = int(x.split(".")[1])
        if word.lower() in ("begin", "do", "then", "of"):
            indent += self.indent_width

        return indent

    def auto_indent_newline(self, event=None):
        """插入一个缩进对齐的新行。 """
        self.editor.insert("insert", "\n")
        # 计算缩进
        n = self.__guess_indent("insert")

        # 插入空格        
        if n:
            self.editor.insert("insert", " " * n)

        # 在最后一行插入，滚动屏幕使之可见
        self.editor.see("insert")
        return "break"

    def auto_insert_match(self, char):
        """根据当前输入的字符，自动插入匹配字符。

        例如，输入 '('，自动插入 ')', 光标停留在 '(' 后。

        另外还有 '{}' '[]', '"', "'" 等。

        """
        if char in "'([{":
            if char == "'":
                self.editor.insert("insert", char)
                self.editor.tag_add("s", "insert -2c", "insert")
            elif char == "{":
                self.editor.insert("insert", "}")
                self.editor.tag_add("c", "insert -2c", "insert")
            else:
                mchar = ")" if char == "(" else "]" 
                self.editor.insert("insert", mchar)
            self.editor.mark_set("insert", "insert -1c")

    def show_match_word(self, index):
        """显示匹配的字。"""
        self.editor.tag_remove("s_match", "1.0", "end")
        x = self.editor.get(index)
        if x in "({[":
            mx = ")" if x == "(" else "]" if x == "[" else "}"
            s1 = index
            s2 = index
            while 1:
                s2 = self.editor.search(
                    mx,
                    s2 + " +1c",
                    elide=True,
                    )
                if s2:
                    s3 = self.editor.search(
                        x,
                        s1 + " +1c",
                        elide=True,
                        stopindex=s2,
                        )
                    if s3 == "":
                        self.editor.tag_add("s_match", index)
                        self.editor.tag_add("s_match", s2)
                        break
                    else:
                        s1 = s3
                else:
                    break

        x = self.editor.get(index + " -1c")
        if x in "]})":
            mx = "(" if x == ")" else "[" if x == "]" else "{"
            s1 = index
            s2 = index
            while 1:
                s2 = self.editor.search(
                    mx,
                    s2 + " -1c",
                    elide=True,
                    backwards=True,
                    stopindex="1.0",
                    )
                if s2:
                    s3 = self.editor.search(
                        x,
                        s1 + " -1c",
                        elide=True,
                        backwards=True,
                        stopindex=s2,
                        )
                    if s3 == "":
                        self.editor.tag_add("s_match", s2)
                        self.editor.tag_add(
                            "s_match",
                            self.editor.index(index + " -1c")
                            )
                        break
                    else:
                        s1 = s3 + " +1c"
                else:
                    break        

    def auto_symbol_complete(self, event):
        """自动补齐功能。 """
        part = self.editor.get("insert -1c wordstart", "insert")
        if part:
            # 补齐功能
            k = len(part)
            symbols = []
            for i in range(3):
                symbols += filter(lambda x:x.startswith(part), self.symbol_list[i])
            n = len(symbols)
            if n == 1:
                self.editor.insert("insert", symbols[0][k:])
            elif n > 1:
                symbols.sort()
                r = self.editor.bbox("insert")
                if r:
                    pm = Tix.Menu(self)
                    for name in symbols:
                        pm.add_command(
                            label=name,
                            command=lambda x=name, k=k:(
                                self.editor.insert("insert", x[k:])
                                ),
                            )
                    pm.post(r[0] + 2, r[1] + 2)
        return "break"
    
    def __mouse_click_event(self, event):
        self.show_match_word("current")

    def __keyrelease_event(self, event):
        if (event.char == "'" or event.char == '"'):
            ch = self.editor.get("insert -1c")
            self.auto_insert_match(ch)
            self.__highlight_syntax("insert -1c", "insert +1c")

        elif event.char:
            # 自动匹配字符的输入
            if event.char in "([{":
                ch = self.editor.get("insert -1c")
                self.auto_insert_match(ch)
            self.__highlight_syntax("insert -2c", "insert")

        # 显示匹配字符
        self.show_match_word("insert")
        
def decode_handler(e):
    if type(e) is UnicodeDecodeError:
        s = e.args[1]
        text = s[e.start:].strip().decode('utf-8')
    return (text, -1)
                                                       
def main():
    os.chdir(os.path.normpath(os.path.dirname(sys.argv[0])))
    # 读取配置文件
    try:
        f = open("algorithm-elf.pycfg")
        options = eval(f.read())
        lang = options["lang"]               # 检查配置文件是否是字典类型
    except Exception, inst:
        sys.stderr.write("Warning: reading configure file failed: " + str(inst))
        lang = None
        options = {}
    mysite.set_locale("algorithm-elf", lang=lang)
    root = Tix.Tk()
    try:
        w = AlgorithmElf(root, options)        
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
        w.mainloop()
    except Exception, inst:
        root.tk.call(
            "tk_messageBox",
            "-title", _("Uncaught Exception"),
            "-message", str(inst),
            "-detail", traceback.format_exc(),
            )

if __name__ == '__main__':
    main()