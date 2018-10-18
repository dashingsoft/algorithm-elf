# -*- coding: utf-8 -*-

import test3

class TypeRecord():
    pass

gcounter = 0


class testAlgorithm():

    def __init__(self):
        global driver
        driver = test3.Driver()

    def run(self):
        print "gcounter", gcounter
        x = TypeRecord()
        print "x is", type(x)

        driver.run(globals().keys())

    
if __name__ == '__main__':
    k = testAlgorithm()
    k.run()
    
