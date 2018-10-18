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
# @文件：about.py
#
# @作者：赵俊德(jondy.zhao@gmail.com)
#
# @创建日期: 2010/03/10
#
# @文件说明：
#
# 关于对话框，对于公司的介绍，产品的说明等。
#
# 这里定义了产品的版本和版权信息，其他脚本必须从这里引用。
# 每一次版本的升级，或者版权变化，都必须要同时修改这里。
#

import os
import Tix
import tkMessageBox
import webbrowser
import binascii
import locale

def get_product_info(name=None):
    infos = {
        "AppName":_("Algorithm Elf"),
        "AppVersion":"1.2.2",
        "AppCopyright":_("Copyright (c) 2009, 2010 Dashingsoft Corp.\n"
                         "All rights reserved."),
        "AppContact":_("Contact: Jondy Zhao (jondy.zhao@gmail.com)"),
        "AppPublisher":_("Dashingsoft Corp."),
        "AppPublisherURL":"http://www.dashingsoft.com",
        "AppSupportURL":"http://www.dashingsoft.com",
        "AppUpdatesURL":"http://www.dashingsoft.com",
        "AppRegisterURL":_("https://secure.shareit.com/shareit/checkout.html?"
                           "PRODUCT[300326756]=1"),
        "AppComments":_("A graphical way to show the implementation process of the "
                        "most data structure algorithms. Applicable to the production "
                        "of algorithms course and help the students understanding of "
                        "the software algorithm for the implementation process.")
        }
    if name is None:
        return infos
    else:
        return infos[name]

def open_document(filename): 
    lang = os.environ.get('LANG')
    if lang is None:
        lang, encode = locale.getdefaultlocale()
    if lang:
        lang = lang.split('.')[0].strip()            
        lang = lang.split('_')[0].lower()
        url = os.path.join("docs", lang, filename)
        if not os.path.exists(url):
            url = os.path.join("docs", filename)
    else:
        url = os.path.join("docs", filename)
    if os.path.exists(url):
        webbrowser.open(url)
    else:
        tkMessageBox.showinfo(
            title=get_product_info('AppName'),
            message=_("No document %s found") % filename,
            )

def register_product(master):
    w = RegisterDialog(master)
    w.go()
    
def open_about_dialog(master):
    w = AboutDialog(master)
    w.go()
    
def create_help_menu(master):
    menu = Tix.Menu(master)
    menu.add_command(
        label=_("Getting started"),
        command=lambda : open_document("getting-started.html"),
        )
    menu.add_command(
        label=_("User Guide"),
        command=lambda : open_document("user-guide.html"),
        )
    menu.add_separator()
    menu.add_command(
        label=_("Register Product"),
        command=lambda w=master : register_product(w),
        )
    # menu.add_command(
    #     label=_("Verify Serial Number"),
    #     command=lambda w=master : verify_serial_number(w),
    #     )
    menu.add_separator()
    menu.add_command(
        label=_("About..."),
        command=lambda w=master : open_about_dialog(w),
        )
    return menu
    
def get_license_information():    
    try:
        import pyshield
        code = pyshield.check_license()
    except Exception, inst:
        code = ""
    if code == "":
        try:
            trialdays = pyshield.get_trial_days()
        except Exception,inst:
            trialdays = 0
        msg = _("You are using a trial version, and the remaining "
                "trial days: %d. \n\nAfter the trial period ends, you "
                "must register this copy before you continue to use "
                "it. More information refer to the file LICENSE located "
                "in the product directory.") % trialdays
    else:
        msg = _("This copy has been registered as No.%s\n\n"
                "Thank you choose to Dashingsoft, we will "
                "be happy to provide you with better products "
                "and more satisfied services. If you have any "
                "question, feel free mail to jondy.zhao@gmail.com "
                "or visit www.dashingsoft.com to get the corresponding "
                "support. It'll be appreciated if you report any "
                "bug occurred when using this product. "
                "Thanks for you again.") % code
    return msg
    
class AboutDialog(Tix.Toplevel):

    def __init__(self, master=None):
        Tix.Toplevel.__init__(self, master)
        self.withdraw()
        _title = _("About %s") % get_product_info("AppName")
        self.title(_title)
        self.iconname(_title)
        self.resizable(False, False)

        self.__createWidgets()

        self.bind("<Return>", lambda e : self.destroy())
        self.bind('<Escape>', lambda e : self.destroy())
        self.title_text.bind("<KeyPress>", lambda e : "break")
        self.body_text.bind("<KeyPress>", lambda e : "break")

    def __createWidgets(self):

        frame = Tix.Frame(self)
        frame.grid()
        img = Tix.PhotoImage(
            master=self,            
            file="logo.gif",
            )
        self.logo_image = img
        w = Tix.Label(
            frame,
            image=self.logo_image,
            borderwidth=0,
            )
        w.grid(row=0, column=0, sticky="nesw")

        self.title_text = Tix.Text(
            frame,
            width=60,
            height=5,
            borderwidth=0,
            insertwidth=0,
            highlightthickness=0,            
            cursor="arrow",
            wrap="none",
            spacing1=5,
            spacing2=5,
            spacing3=5,
            )
        w.config(background=self.title_text["bg"])
        self.title_text.grid(
            row=0,
            column=1,
            sticky="nesw",
            )
        self.title_text.insert(
            "end",
            get_product_info("AppName"),
            ("pn",)
            )
        self.title_text.tag_configure(
                "pn",
                lmargin1=10,
                )
        self.title_text.insert("end", "\n")

        self.title_text.insert(
            "end",
            _("Version %s") % get_product_info("AppVersion"),
            ("pv",)
            )
        self.title_text.tag_configure(
                "pv",
                lmargin1=30,
                )
        self.title_text.insert("end", "\n")

        self.title_text.insert(
            "end",
            get_product_info("AppCopyright"),
            ("pc",)
            )

        self.title_text.tag_configure(
                "pc",
                lmargin1=30,
                )
        self.title_text.insert("end", "\n")

        self.title_text.insert(
            "end",
            get_product_info("AppPublisherURL"),
            ("ph",)
            )
        self.title_text.tag_configure(
                "ph",
                lmargin1=30,
                underline=1,
                )
        self.title_text.tag_bind(
                "ph",
                "<ButtonRelease-1>",
                lambda e:webbrowser.open(
                            get_product_info("AppPublisherURL")
                            )
                )
        self.body_text = Tix.Text(
            frame,
            width=60,
            height=15,
            borderwidth=0,
            insertwidth=0,
            highlightthickness=0,            
            cursor="arrow",
            wrap="word",
            padx=4,
            pady=2,
            spacing1=2,
            spacing2=2,
            spacing3=2,
            )
        self.body_text.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ewn",
            )
        self.body_text.insert("end", get_product_info("AppComments"))
        self.body_text.insert("end", "\n" * 3)
        self.body_text.insert("end", get_license_information())

        w = Tix.Button(
            self,
            text=_("OK"),
            overrelief="groove",
            width=8,
            command=self.destroy,
            )
        w.grid(row=1, column=0, padx=5, pady=5)

    def go(self):
        self.state("normal")
        self.wait_visibility()
        self.focus_set()
        self.grab_set()

class RegisterDialog(Tix.Toplevel):
    """ 显示注册对话框 """

    def __init__(self, master=None):
        Tix.Toplevel.__init__(self, master)
        self.withdraw()
        _title = _("Register %s") % get_product_info("AppName")
        self.title(_title)
        self.iconname(_title)
        self.resizable(False, False)
        self.__createWidgets()

    def __createWidgets(self):        
        frame = Tix.Frame(
            self,
            relief="groove",
            borderwidth=2,
            )
        frame.grid(
            padx=3,
            pady=3,
            row=0,
            column=0,
            sticky="nesw"
            )        
        w = Tix.Label(
            frame,
            text=_("1. Get Registration Code. Click Buy Now"
                   " to get one from the web site online."),
            justify="left",
            )
        w.grid(row=0, column=0, sticky='w')
        w = Tix.Button(
            frame,
            text=_("Buy Now"),
            overrelief="groove",
            command=lambda e : webbrowser.open( 
                get_product_info("AppRegisterURL")
                )                
            )
        w.grid(row=0, column=1, padx=10)

        frame = Tix.Frame(
            self,
            relief="groove",
            borderwidth=2,
            )
        frame.grid(
            padx=3,
            pady=3,
            row=1,
            column=0,
            sticky="nesw",
            )
        frame.columnconfigure(0, weight=1)
        
        w = Tix.Label(
            frame,
            text=_("2. Type the Registration Code in the text box."),
            justify="left",
            )
        w.grid(row=0, column=0, sticky='w')

        self.text = Tix.Text(
            frame,
            width=60,
            height=6,
            relief="groove",
            spacing1=2,
            spacing2=2,
            spacing3=2,            
            )
        self.text.grid(
            row=1,
            column=0,
            padx=2,
            pady=5,
            sticky="nesw",
            )
        
        # 命令按钮
        frame = Tix.Frame(
            self,
            relief="groove",
            borderwidth=2,
            )
        frame.grid(
            padx=3,
            pady=3,
            row=2,
            column=0,
            sticky="nesw",
            )
        w = Tix.Label(
            frame,
            text=_("3. Click Register to register."),
            justify="left",
            )
        w.grid(row=0, column=0, sticky='w')        
        w = Tix.Button(
            frame,
            text=_("Register"),
            overrelief="groove",
            command=self.do_register,
            )
        w.grid(row=0, column=1, padx=10)
        
        w = Tix.Button(
            self,
            text=_("Close"),
            overrelief="groove",
            command=self.destroy
            )
        w.grid(row=3, column=0, pady=10)

    def do_register(self):
        # 根据 key 生成 license.lic        
        buf = self.text.get("0.1", "end").strip()
        try:
            filename = "license.lic"
            f = open(filename, "wb")
            f.write(str(buf))
            f.close()
        # s = self.text.get("0.1", "end").strip()
        # try:
        #     filename = "license.lic"
        #     buf = binascii.unhexlify(s)
        #     f = open(filename, "wb")
        #     f.write(buf)
        #     f.close()

            # 提示用户重新启动
            tkMessageBox.showinfo(
                title=get_product_info("AppName"),
                message=_("Thank for you to register the product.\n"
                          "You need restart your application "
                          "to take it affect.\n\n")                          
                )
            self.destroy()
        except Exception, inst:
            tkMessageBox.showinfo(
                title=get_product_info("AppName"),
                message=_("Register product failed: %s") % str(inst),
                )
            
    def go(self):
        self.state("normal")
        self.wait_visibility()
        self.focus_set()
        self.grab_set()
        
if __name__ == '__main__':
    import gettext
    gettext.NullTranslations().install()

    root = Tix.Tk()
    w = AboutDialog(root)
    # w = RegisterDialog(root)
    print w.go()
    root.wait_window(w)