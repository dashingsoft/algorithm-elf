# -*- coding: utf-8 -*-
#

import sys
import pascal
from aftype import Char, Integer, Boolean, Real
from aftype import String, Array
from aftype import Enum, Set, Record, Pointer
from aftype import Queue, Tree

def prepare(driver, configure):
    return postorderAlgorithm(driver, configure)


class postorderAlgorithm(object):

    def __init__(self, driver, configure):
        global Driver
        Driver = driver
        Driver.vision_initialize(**configure['options'])

        global Vars
        Vars = {}
        for (name, args) in configure['vars']:
            Vars[name] = eval(args[0] + '()')
            Vars[name].build(args[1], Vars)
            Vars[name].options.update(args[2])
            if args[2].get('visible', False):
                Vars[name].show(**args[2])
            Vars[name].watch(eval(args[2].get('watch', 'None'), Vars))

        Driver.simulate_main_entry('postorder', 1, Vars)

    def run(self):
        self.postorder(bt=Vars['bt'],)
        Driver.simulate_function_return()

    def postorder(self, bt):
        bt.clone()
        Driver.simulate_function_call('postorder', 1, locals())
        Result = None

        Driver.simulate_statement(2)
        Driver.simulate_statement(3)
        if bt != Pointer():
            Driver.simulate_statement(5)
            bt.get()['value'].select()
            Driver.simulate_statement(6)
            _postorder = self.postorder(bt.get()['lchild'])
            Driver.simulate_function_return()
            Driver.simulate_statement(6)
            _postorder
            Driver.simulate_statement(7)
            bt.get()['value'].select()
            Driver.simulate_statement(8)
            _postorder = self.postorder(bt.get()['rchild'])
            Driver.simulate_function_return()
            Driver.simulate_statement(8)
            _postorder
            Driver.simulate_statement(9)
            bt.get()['value'].select()
            Driver.simulate_statement(10)
            _visit = self.visit(bt)
            Driver.simulate_function_return()
            Driver.simulate_statement(10)
            _visit
        Driver.simulate_statement(12)

        return Result

    def visit(self, bt):
        bt.clone()
        Driver.simulate_function_call('visit', 14, locals())
        Result = None

        Driver.simulate_statement(15)
        Driver.simulate_statement(16)
        bt.get()['value'].active()
        Driver.simulate_statement(17)

        return Result


# End of Class postorderAlgorithm
