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
 * @文件：dsoutput.py
 *
 * @作者：赵俊德(jondy.zhao@gmail.com)
 *
 * @创建日期: 2010/02/24
 *
 * @文件说明：
 *
 *    输出视图，用于显示执行过程中的输出信息和行为动作的说明。
 *
"""
import Tkinter
import Tix


class OutputView(Tkinter.Toplevel):
    def __init__(self, master=None):
        Tkinter.Toplevel.__init__(self, master)
        self.withdraw()
        self.title(_("Output"))
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
        """清空视图的数据. """
        self.__text_output["state"] = "normal"
        self.__text_output.delete("1.0", Tkinter.END)
        self.__text_output["state"] = "disabled"

    def message(self, value):
        self.__text_output["state"] = "normal"
        self.__text_output.insert(
            Tkinter.END,
            value,
            ()
            )
        self.__text_output.see(Tkinter.END)
        self.__text_output.insert(Tkinter.END, "\n")
        self.__text_output["state"] = "disabled"

    def error(self, value):
        self.__text_output["state"] = "normal"
        _tags = ("e",)
        self.__text_output.insert(
            Tkinter.END,
            value,
            _tags
            )
        self.__text_output.see(Tkinter.END)
        self.__text_output.insert(Tkinter.END, "\n")
        self.__text_output["state"] = "disabled"
        self.show()

    def __create_widgets(self):
        _scrolled_text = Tix.ScrolledText(
            self,
            scrollbar="none",
            borderwidth=2,
            relief="groove",
            height=300,
            )
        self.__text_output = _scrolled_text.subwidget("text")
        self.__text_output.configure(
                wrap="word",
                takefocus=0,
                borderwidth=2,
                relief="groove",
                background="#F5F5F5",
                state="disabled",
                cursor="arrow",
                pady=2,
                )
        _scrolled_text.grid(sticky="nesw")        
        self.__text_output.tag_config(
            "e",
            foreground='red'
            )


if __name__ == "__main__":
    import gettext
    gettext.NullTranslations().install()

    root = Tix.Tk()
    _dialog = OutputView(root)
    _dialog.output("123")
    _dialog.output("abc", True)
    _dialog.show()
    _dialog.mainloop()
    

