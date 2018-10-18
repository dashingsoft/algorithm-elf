# -*- coding: utf-8 -*-

import pascal

from aftype import Char, Integer, Boolean, Real
from aftype import String, Array
from aftype import Enum, Set, Record, Pointer
from aftype import Tree


def prepare(driver, configure):
    return testAlgorithm(driver, configure)

class testAlgorithm(object):

    def __init__(self, driver, configure):

        global Driver
        Driver = driver
        Driver.vision_initialize(**configure['options'])

        global Vars
        Vars = {}
        for (name, args) in configure['vars']:
            Vars[name] = eval("%s()" % args[0])            
            Vars[name].build(args[1], Vars)
            Vars[name].options.update(args[2])
            if args[2].get("visible", False):
                Vars[name].show(**args[2])                        
            Vars[name].watch(eval(args[2].get("watch", "None"), Vars))
                
        Driver.simulate_main_entry("Algorithm Hanoi", 1, Vars)

    def run(self):
        self.hanoi(
            Vars['n'],
            Vars['x'],
            Vars['y'],
            Vars['z'],
            )
        Driver.simulate_function_return()
        
    def hanoi(self, n, x, y, z):        
        Driver.simulate_function_call("hanoi", 1, locals())
        
        # BEGIN
        Driver.simulate_statement(3)    

        Driver.simulate_statement(4)    
        if n == Integer(1):

            Driver.simulate_statement(5)
            self.move(x, Integer(1), z)
            Driver.simulate_function_return()

        else:
            # ELSE BEGIN
            Driver.simulate_statement(6)

            Driver.simulate_statement(8)
            self.hanoi(n - Integer(1), x, z, y)
            Driver.simulate_function_return()

            Driver.simulate_statement(9)
            self.move(x, n, z)
            Driver.simulate_function_return()

            # 模拟函数调用
            Driver.simulate_statement(11)
            self.hanoi(n - Integer(1), y, x, z)
            Driver.simulate_function_return()

        # 模拟函数返回
        Driver.simulate_statement(13)

    def move(self, x, n, y):
        Driver.simulate_function_call("move", 15, locals())

        i = Integer(3)

        Driver.simulate_statement(16)

        Driver.simulate_statement(17)

        i.assign(Integer(5))
        Driver.simulate_statement(18)

    
if __name__ == '__main__':
    pass
    
