# -*- coding: utf-8 -*-

import sys
sys.path.append("..")

import aftype
from aftype import Char, Integer, Boolean, Real
from aftype import String, Array
from aftype import Enum, Set, Record, Pointer

def __get__(x):
    return x.get()

def prepare(driver, configure):
    return testAlgorithm(driver, configure)

class testAlgorithm():

    def __init__(self, driver, configure):

        global Driver
        Driver = driver

        n = Integer()
        x = Char()
        y = Char()
        z = Char()
        
        n.build(configure['paras']['n'])
        x.build(configure['paras']['x'])
        y.build(configure['paras']['y'])
        z.build(configure['paras']['z'])

        global Paras
        Paras = {
                  'n': n,
                  'x': x,
                  'y': y,
                  'z': z
                  }

        Driver.vision_initialize(configure['options'])
        for (name, args) in configure['images'].iteritems():
            Driver.vision_append_node(name, **args)

        # 添加盘子
        for i in range(n.get()):
            Driver.append_node(
                "A",
                'node',
                'plate_%d' % (i + 1),
                title=str(i+1),
                padx=(i + 1) * 5,
                tanchor='center',
                options={'fill':'#1E90FF'},
                )

        Driver.vision_enable_refresh()
        Driver.simulate_main_call("hanoi", 1, self.__paras)

    def run(self):

        self.hanoi(
            Paras['n'],
            Paras['x'],
            Paras['y'],
            Paras['z'],
            )

    def hanoi(self, n, x, y, z):
        n = Integer(n.get())
        x = Char(x.get())
        y = Char(y.get())
        z = Char(z.get())
        
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
        Driver.simulate_declare_var(i.name, i)

        Driver.simulate_statement(16)

        Driver.simulate_statement(17)
        # print x, " ", n, " ", y
        _name = "plate_%s" % (Paras['n'] - n + Integer(1))
        Driver.simulateVisionMove(str(_name),str(x), str(y))

        i.assign(Integer(5))
        Driver.simulate_statement(18)

    
if __name__ == '__main__':
    m = __import__("test2")
    print dir(m), type(m.__dict__["gcounter"])
    x = m.testAlgorithm()
    print globals().keys()
    x.run()
    
