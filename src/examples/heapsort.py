# -*- coding: utf-8 -*-
#

import sys
import pascal
from aftype import Char, Integer, Boolean, Real
from aftype import String, Array
from aftype import Enum, Set, Record, Pointer
from aftype import Queue, Tree

def prepare(driver, configure):
    return mergesortAlgorithm(driver, configure)


class mergesortAlgorithm(object):

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

        Driver.simulate_main_entry('mergesort', 1, Vars)

    def run(self):
        self.mergesort(r=Vars['r'],r2=Vars['r2'],s=Vars['s'],t=Vars['t'],)
        Driver.simulate_function_return()

    def mergesort(self, r, r2, s, t):
        s.clone()
        t.clone()
        Driver.simulate_function_call('mergesort', 1, locals())
        Result = None

        class Integer5(Array):
            def __init__(self, value={}):
                Array.__init__(self, value=value, cls=Integer)
                self.frame = sys._getframe(1)
        r1 = Integer5()
        Driver.simulate_declare_var(r1)
        Driver.simulate_statement(6)
        Driver.simulate_statement(7)
        pascal.setlength(r1, t + Integer(1))
        Driver.simulate_statement(8)
        if s == t:
            Driver.simulate_statement(9)
            r1[s].assign(r[s])
        else:
            Driver.simulate_statement(11)
            _mergesort = self.mergesort(r, r2, s, ( s + t) / Integer(2))
            Driver.simulate_function_return()
            Driver.simulate_statement(11)
            _mergesort
            Driver.simulate_statement(12)
            _mergesort = self.mergesort(r, r2, ( s + t) / Integer(2) + Integer(1), t)
            Driver.simulate_function_return()
            Driver.simulate_statement(12)
            _mergesort
            Driver.simulate_statement(13)
            _merge = self.merge(r2, s, ( s + t) / Integer(2), t, r1)
            Driver.simulate_function_return()
            Driver.simulate_statement(13)
            _merge
        Driver.simulate_statement(15)

        return Result

    def merge(self, rs, s, m, n, rn):
        rs.clone()
        s.clone()
        m.clone()
        n.clone()
        Driver.simulate_function_call('merge', 17, locals())
        Result = None

        i = Integer()
        Driver.simulate_declare_var(i)
        j = Integer()
        Driver.simulate_declare_var(j)
        k = Integer()
        Driver.simulate_declare_var(k)
        ki = Integer()
        Driver.simulate_declare_var(ki)
        Driver.simulate_statement(23)
        i.show()
        j.show()
        k.show()
        Driver.simulate_statement(25)
        i.assign(s)
        Driver.simulate_statement(25)
        j.assign(m + Integer(1))
        Driver.simulate_statement(25)
        k.assign(s - Integer(1))
        Driver.simulate_statement(1)
        while ( i <= m) and ( j <= n):
            Driver.simulate_statement(28)
            k.assign(k + Integer(1))
            Driver.simulate_statement(29)
            if rs[i] <= rs[j]:
                Driver.simulate_statement(31)
                rn[k].assign(rs[i])
                Driver.simulate_statement(32)
                i.assign(i + Integer(1))
            else:
                Driver.simulate_statement(36)
                rn[k].assign(rs[j])
                Driver.simulate_statement(37)
                j.assign(j + Integer(1))
            Driver.simulate_statement(39)
            if i <= m:
                ki = k + Integer(1) - Integer(1)
                _for_end = n
                while True:
                    Driver.simulate_statement(40)
                    ki = ki + Integer(1)
                    if ki > _for_end: break
                    Driver.simulate_statement(41)
                    rn[ki].assign(rs[i + ki - k - Integer(1)])
            Driver.simulate_statement(43)
            if j <= n:
                ki = k + Integer(1) - Integer(1)
                _for_end = n
                while True:
                    Driver.simulate_statement(44)
                    ki = ki + Integer(1)
                    if ki > _for_end: break
                    Driver.simulate_statement(45)
                    rn[ki].assign(rs[j + ki - k - Integer(2)])
        i.hide()
        j.hide()
        k.hide()
        Driver.simulate_statement(48)

        return Result


# End of Class mergesortAlgorithm
