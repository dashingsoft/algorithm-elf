# -*- coding: utf-8 -*-
#

import sys
import pascal
from aftype import Char, Integer, Boolean, Real
from aftype import String, Array
from aftype import Enum, Set, Record, Pointer
from aftype import Queue, Tree

def prepare(driver, configure):
    return hanoiAlgorithm(driver, configure)


class hanoiAlgorithm(object):

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

        Driver.simulate_main_entry('hanoi', 1, Vars)

    def hanoi(self, n, x, y, z):
        n = n.clone()
        x = x.clone()
        y = y.clone()
        z = z.clone()
        Driver.simulate_function_call('hanoi', 3, locals())
        Result = None

        Driver.simulate_statement(5)
        Driver.simulate_statement(6)
        if n == Integer(1):
            Driver.simulate_statement(7)
            pascal.move(x, Integer(1), z)
        else:
            Driver.simulate_statement(10)
            _hanoi = self.hanoi(n - Integer(1), x, z, y)
            Driver.simulate_function_return()
            Driver.simulate_statement(10)
            _hanoi
            Driver.simulate_statement(11)
            pascal.move(x, n, z)
            Driver.simulate_statement(13)
            _hanoi = self.hanoi(n - Integer(1), y, x, z)
            Driver.simulate_function_return()
            Driver.simulate_statement(13)
            _hanoi
        Driver.simulate_statement(15)


        return Result

    def move(self, x1, x2):
        x1 = x1.clone()
        x2 = x2.clone()
        Driver.simulate_function_call('move', 17, locals())
        Result = None

        v0 = Integer()
        Driver.simulate_declare_var(v0)
        v1 = Char()
        Driver.simulate_declare_var(v1)
        v1 = Char()
        Driver.simulate_declare_var(v1)
        v1 = Char()
        Driver.simulate_declare_var(v1)
        v4 = Integer()
        Driver.simulate_declare_var(v4)
        Driver.simulate_statement(22)
        Driver.simulate_statement(23)
        v0.assign(Integer(1))
        v0.assign(Integer(1) - Integer(1))
        _for_end = Integer(100)
        while True:
            Driver.simulate_statement(24)
            v0.assign(v0 + Integer(1))
            if v0 > _for_end: break
            Driver.simulate_statement(26)
            v1.assign(xxx)
        Driver.simulate_statement(30)
        v2.assign(yyy)
        Driver.simulate_statement(29)
        while True:
            Driver.simulate_statement(31)
            if v2 == Integer(0): break
