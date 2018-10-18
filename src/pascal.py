#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""定义 Pascal 中对应的系统库函数。

"""
import sys
import math

from aftype import AlgorithmError
from aftype import BaseType
from aftype import Char, Integer, Boolean, Real
from aftype import String, Array, Tree
from aftype import Enum, Set, Record, Pointer
from aftype import Indexpointer

kwlist = ("array", "and", "begin", "case", "const", "do",
          "downto", "else", "end", "for", "from", "function",
          "if", "not", "of", "or", "procedure","program",
          "record", "repeat", "set", "then", "to", "type",
          "until", "var", "while", "arraypointer")

def addr(var):
    result = Integer(id(var))
    result.frame = sys._getframe(1)
    return result

def copy(s, index, count):
    assert(issubclass(type(s), String))
    assert(issubclass(type(index), Integer))
    assert(issubclass(type(count), Integer))
    index -= 1
    result = String(s.value[index:index+count])
    result.frame = sys._getframe(1)
    return result

def cos(x):
    assert(issubclass(type(x), (Real, Integer)))
    result = Real(math.cos(x.value))
    result.frame = sys._getframe(1)
    return result

def delete(s, index, count):
    assert(issubclass(type(s), String))
    assert(issubclass(type(index), Integer))
    assert(issubclass(type(count), Integer))
    index -= 1
    result = String(s.value[0:index] + s.value[index+count:])
    result.frame = sys._getframe(1)
    return result

def dispose(var):    
    assert issubclass(type(var), (Array, Pointer))
    if issubclass(type(var), Pointer):
        var.value.dispose()
        var.assign(BaseType())
            
def exp(x):
    assert(issubclass(type(x), (Real, Integer)))
    result = Real(math.exp(x.value))
    result.frame = sys._getframe(1)
    return result

def frac(x):
    assert(issubclass(type(x), (Real, Integer)))
    result = Real(math.modf(x.value)[0])
    result.frame = sys._getframe(1)
    return result

def high(x):
    assert issubclass(type(x), BaseType), type(x)
    assert(not issubclass(type(x), (Pointer, Record)))
    v = x.value
    if isinstance(v,dict):
        if len(v) == 0:
            result = Integer(-1)
        else:
            result = Integer(max(*v.keys()))
    elif isinstance(v, basestring):
        result = Integer(len(v))
    else:
        result = Integer(0)
    result.frame = sys._getframe(1)
    return result

def insert(source, s, index):
    assert(issubclass(type(source), String))
    assert(issubclass(type(s), String))
    assert(issubclass(type(index), Integer))
    s.assign(String(s.value[0:index] + source.value + s.value[index:]))

def int(x):
    assert(issubclass(type(x), (Integer, Real)))
    result = Integer(math.floor(x))
    result.frame = sys._getframe(1)
    return result

def length(var):
    assert(issubclass(type(var), BaseType))
    assert(not issubclass(type(index), Pointer))
    result = Integer(len(var.value))
    result.frame = sys._getframe(1)
    return result

def ln(x):
    assert(issubclass(type(x), (Integer, Real)))
    result = Integer(math.log(x))
    result.frame = sys._getframe(1)
    return result

def low(x):
    assert(issubclass(type(x), BaseType))
    assert(not issubclass(type(x), (Pointer, Record)))
    v = x.value
    if isinstance(v, dict):
        result = Integer(min(*v.keys()))
    else:
        result = Integer(0)
    result.frame = sys._getframe(1)
    return result

def move(source, dest, count):
    assert(issubclass(type(source), String))
    assert(issubclass(type(dest), String))
    assert(issubclass(type(count), Integer))
    dest.assign(String(source.value[0:count]))

def new(var):
    assert(issubclass(type(var), Pointer))
    obj = var.pcls.__new__(var.pcls)
    var.pcls.__init__(obj)
    obj.frame = sys._getframe(1)
    var.value = obj
    obj.name = "<%s>" % var.name
    obj.new()

def odd(x):
    assert(issubclass(type(x), Integer))
    result = Boolean(x % 2 == 1)
    result.frame = sys._getframe(1)
    return result

def ord(x):
    assert(issubclass(type(x), (Char, Enum, String, Integer)))
    v = x.value
    if isinstance(v, basestring):
        result = Integer(ord(v[0]))
    else:
        result = Integer(v)
    result.frame = sys._getframe(1)
    return result

def ptr(var):
    assert(issubclass(type(var), BaseType))
    return var

def pos(substr, s):
    result = Integer(s.value.find(substr.value) + 1)
    result.frame = sys._getframe(1)
    return result

def setlength(var, newlength):
    if not issubclass(type(var), (Array, Pointer)):
        raise AlgorithmError(1, "Pointer", type(var).__name__)
    if issubclass(type(var), Pointer):
        pcls = var.pcls
        value = Array(cls=pcls)
        value.frame = sys._getframe(1)
        value.name = "<%s>" % var.name    
        for i in range(newlength):
            obj = pcls.__new__(pcls)
            pcls.__init__(obj)
            value[Integer(i)] = obj
            value[Integer(i)].frame = sys._getframe(1)
        var.assign(value)
        value.new()
    elif issubclass(type(var), Array):
        pcls = var.pcls
        for i in range(newlength):
            obj = pcls.__new__(pcls)
            pcls.__init__(obj)
            var[Integer(i)] = obj
            var[Integer(i)].frame = sys._getframe(1)
            var.resize()
    else:
        raise AlgorithmError(1, "Pointer", type(var).__name__)
    
def sin(x):
    assert(issubclass(type(x), (Real, Integer)))
    result = Real(math.sin(x.value))
    result.frame = sys._getframe(1)
    return result

def sqr(x):
    assert(issubclass(type(x), (Real, Integer)))
    result = x.__new__(type(x))
    type(x).__init__(result, x.value * x.value)
    result.frame = sys._getframe(1)
    return result

def sqrt(x):
    result = Real(math.sqrt(x.value))
    result.frame = sys._getframe(1)
    return result

def str(x, s):
    pass
    
def trunc(x):
    result = Integer(math.modf(x.value)[1])
    result.frame = sys._getframe(1)
    return result
    
def val(x):
    pass
    
def write(f, *args):
    s = f.value
    for p in args:
        s = "{0} {1}".format(s, p.value)
    print s,

def writeln(f, *args):
    write(f, *args)
    print

if __name__ == '__main__':
    p1 = Pointer(Integer)
    print p1.name
    new(p1)

    p1.get().assign(Integer(123))
    print p1.get()

    s = String(String("123"))
    p1.assign(s)
    p1.get().assign(String("456"))
    print p1.get()

    write("123")
    writeln("123456:", 6, 7)
    write("aaa")
    write("bbb")

    a = Array()
    setlength(a, 3)
    print a[0]
    print "high(a)=", high(a)
    print "low(a)=", low(a)
    print a

    i = Integer(2)
    p1.assign(i)
    print p1.get()
    p1.get().assign(Integer(3))
    print i
    print p1.get()

    s = "12345"
    print delete(s, 2, 2)

    s = String("12345")

    insert("aaa", s, -21)
    print s
    print "s.name is: ", s.name
    print "high(s)=", high(s)
    print "low(s)=", low(s)

    move("456", s, 2)
    print "s.name is: ", s.name
    print s

    print ord_(Integer(1))
    print ord_(Char("c"))

    new(p1)
    print "first new p1's name:", p1.get().name
    new(p1)
    print "2nd new p1's name:", p1.get().name
    p1.get().assign(Integer(15))
    print p1.get()
    print p1.get().name