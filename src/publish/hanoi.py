# -*- coding: utf-8 -*-
#
# This script is generated by Algorithm Elf 1.2.1

import sys
import pascal
from aftype import DRIVER, datapool
from aftype import Char, Integer, Boolean, Real
from aftype import String, Array
from aftype import Enum, Set, Record, Pointer
from aftype import Queue, Tree, Indexpointer

class Pole(Pointer):
    def __init__(self, value=None, cls=Integer):
        Pointer.__init__(self, cls=cls)
        self.frame = sys._getframe(1)


class AlgorithmInstance(object):

    def __init__(self):
        n.declare()
        x.declare()
        y.declare()
        z.declare()

    def hanoi(self, n, x, y, z):
        DRIVER.simulate_function_call('hanoi', 10, sys._getframe())
        n = n.clone()
        n.declare()
        x.frame = sys._getframe()
        y.frame = sys._getframe()
        z.frame = sys._getframe()
        result = None

        DRIVER.simulate_statement(11, sys._getframe())
        DRIVER.simulate_statement(12, sys._getframe())
        if n == Integer(1):
            DRIVER.simulate_statement(13, sys._getframe())
            _move_node = self.move_node(x, Integer(1), z)
            DRIVER.simulate_function_return()
            DRIVER.simulate_statement(13, sys._getframe())
            _move_node
        else:
            DRIVER.simulate_statement(15, sys._getframe())
            _hanoi = self.hanoi(n - Integer(1), x, z, y)
            DRIVER.simulate_function_return()
            DRIVER.simulate_statement(15, sys._getframe())
            _hanoi
            DRIVER.simulate_statement(16, sys._getframe())
            _move_node = self.move_node(x, n, z)
            DRIVER.simulate_function_return()
            DRIVER.simulate_statement(16, sys._getframe())
            _move_node
            DRIVER.simulate_statement(17, sys._getframe())
            _hanoi = self.hanoi(n - Integer(1), y, x, z)
            DRIVER.simulate_function_return()
            DRIVER.simulate_statement(17, sys._getframe())
            _hanoi
        DRIVER.simulate_statement(19, sys._getframe())

        n.destroy()
        x.frame = sys._getframe(1)
        y.frame = sys._getframe(1)
        z.frame = sys._getframe(1)

        return result

    def move_node(self, x, n, y):
        DRIVER.simulate_function_call('move_node', 21, sys._getframe())
        x.frame = sys._getframe()
        n = n.clone()
        n.declare()
        y.frame = sys._getframe()
        result = None

        DRIVER.simulate_statement(22, sys._getframe())
        DRIVER.simulate_statement(23, sys._getframe())
        x[n - Integer(1)].assign(None)
        DRIVER.simulate_statement(24, sys._getframe())
        y[n - Integer(1)].assign(n)
        DRIVER.simulate_statement(25, sys._getframe())

        x.frame = sys._getframe(1)
        n.destroy()
        y.frame = sys._getframe(1)

        return result

    def run(self):
        DRIVER.simulate_program_entry('hanoi', 27)
        DRIVER.simulate_statement(28, sys._getframe())
        _hanoi = self.hanoi(n, x, y, z)
        DRIVER.simulate_function_return()
        DRIVER.simulate_statement(28, sys._getframe())
        _hanoi
        DRIVER.simulate_statement(29, sys._getframe())

def init():
    vlist = []
    global n
    vlist.append(('n', 'Integer'))
    n = datapool('n', 'Integer')
    global x
    vlist.append(('x', 'Pole'))
    x = datapool('x', 'Pole')
    global y
    vlist.append(('y', 'Pole'))
    y = datapool('y', 'Pole')
    global z
    vlist.append(('z', 'Pole'))
    z = datapool('z', 'Pole')

    return vlist
var_list = init()

# End of Class hanoiAlgorithm
