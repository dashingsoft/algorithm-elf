# -*- coding: utf-8 -*-
#
#############################################################
#                                                           #
#      Copyright @ 2009 - 2010 Dashingsoft corp.            #
#      All rights reserved.                                 #    
#                                                           #
#      Pyshield                                             #
#                                                           #
#      Version: 1.2.1 -                                     #
#                                                           #
#############################################################
#
#
#  @File: register.py
#
#  @Author: Jondy Zhao(jondy.zhao@gmail.com)
#
#  @Create date: 2010/10/19
#
#  @Description:
#
#    This file is uesd to register the product.
#

import os, sys
import Tix
import webbrowser
import tkMessageBox
import binascii

__register_url__ = ("https://secure.shareit.com/shareit/checkout.html?"
                    "PRODUCT[300326756]=1")
__title__ = "Register Algorithm Elf"

class RegisterDialog(Tix.Frame):
    def __init__(self, master):
        Tix.Frame.__init__(self, master)
        self.master.title(__title__)
        self.master.iconname(__title__)
        self.master.resizable(False, False)
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
            command=lambda : webbrowser.open(__register_url__),
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
            command=self.quit
            )
        w.grid(row=3, column=0, pady=10)

    def do_register(self):
        buf = self.text.get("0.1", "end").strip()
        try:
            filename = "license.lic"
            f = open(filename, "wb")
            f.write(str(buf))
            f.close()

            tkMessageBox.showinfo(
                title=__title__,
                message=_("Thank for you to register the product.\n"
                          "You need restart your application "
                          "to take it affect.\n\n")                          
                )
            self.destroy()
                    
        except Exception, inst:
            tkMessageBox.showinfo(
                title=__title__,
                message=_("Register product failed: %s") % str(inst),
                )
            
    def go(self):
        self.state("normal")
        self.wait_visibility()
        self.focus_set()
        self.grab_set()

if __name__ == "__main__":
    _ = str
    root = Tix.Tk()
    w = RegisterDialog(root)
    w.grid()
    root.mainloop()