#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#############################################################
#                                                           #
#      版权所有 2009 - 2010 德新软件公司。保留全部权利。    #
#                                                           #
#      数据结构算法助手                                     #
#                                                           #
#      版本区间：1.1.0 -                                    #
#                                                           #
#############################################################

"""
 * @文件：aftype.py
 *
 * @作者：赵俊德(jondy.zhao@gmail.com)
 *
 * @日期：2010/02/24
 *
 * @文件说明：
 *
 *      定义 Pascal 中对应的基础数据类型。
 *

Pascal 语言转换 Python 语言的基本规则：

* 数据类型转换
  用于转换 Type 部分的语句

  type
    Tx = Ty;
    PTx = ^Tx;
    Te = (red, green, blue);
    Ts = [0..2];
    Tr = record of
          name: string;
          value: real;
        end;
    Ta = array of Integer;
    Tfa = array [1..10] of Integer;

   分别转换成为

   class Tx(Ty): pass

   class PTx(Pointer):
       def __init__(self, cls=Tx):
           Pointer.__init__(self, cls=cls)
           self.frame = sys._getframe(1)

   class Te(Enum):
       def __init__(self, value=None):
           Enum.__init__(self, value=value)
           self.frame = sys._getframe(1)
           self.data_dict = {
               'red': 0,
               'green': 1,
               'blue': 2
               }
   global red
   red = 0
   global green
   green = 1
   global blue
   blue = 2

   class Ts(Set):
       pass

   class Tr(Record):
       def __init__(self, value={'name':String(), 'value':Real()}):
           Record.__init__(self, value=value)
           self.frame = sys._getframe(1)


   class Ta(Array):
       def __init__(self, value={}):
           Array.__init__(self, value=value, cls=Integer)
           self.frame = sys._getframe(1)

   class Tfa(Array):
       def __init__(
           self,
           value=dict([ [i, Integer()] for i in range(Low, High) ]),
           cls=Integer):
           Array.__init__(self, value=value)
           self.frame = sys._getframe(1)

* 变量转换
  用于转换 var 部分的语句。

  var
    i: Integer;
    s: String;

  分别转换成为

  i = Integer()
  s = String()

  约束：在变量声明部分不能定义类型
  譬如，不可以声明 r: set of [0..10];
  需要转换成为：
  type
      tr = set of [0..10];
  var
      r: tr;

* 赋值语句转换

  变量赋值
  i = 2

  =>

  i.assign(2)

  通过指针变量赋值
  p^ = 2

  =>

  p.get().assign(2)

  记录成员赋值
  r.name = value

  =>

  r['name'] = value

  数组赋值
  a[1] = 3

  =>

  a[Integer(1)] = 3

* 函数转换
  约束：函数的返回值使用变量 Result 来表示

  Pascal的函数被转换成为
  pascal.name

  例如
  new(p);

  被转换成为
  pascal.new(p);

  函数调用的返回

  function abs(value):float;

  被转换成为

  def abs(value):
      try:
          result = abs(value)
      finally:
          return result

  带有变量参数的函数

  procedure myproc(var x: integer, y: integer);

  会被转换成为

  def myproc(x, y):
      x.frame = sys._getframe()
      y = y.clone()
      result = None

      x.frame = sys._getframe(1)
      y.destroy()
      return result

  值参，进入之前进行克隆，退出时候要删除；
  变参，进入之前将 frame 设置为当前，退出的时候恢复到原来的 frame；

  因为所有的参数都是基于 BaseType，类参数的传递 Python 使用的
  是引用传递，而不是复制，所以必须进行处理。

  特别的，对于没有参数的过程，要增加后面的语句。
  因为 Pascal 中允许直接调用过程，而不使用小括号。


* 特殊转换

  Exit 会被转换成为 return
  nil 会被转换成为 Pointer()

  result 是一个特殊变量，可以引用函数的返回值

* AF 语言扩充

  在声明的时候增加 @ 前缀表示引用数据池中的同名数据项

  例如
      var
      @i : integer;

      将会被转换成为

      i = aftype.datapool(i, "Integer")

  可见对象在其作用堆栈返回的时候，会被自动删除。在函数的结束
  部分会自动增加 i.hide() 语句。

  设置一个变量成为数组的下标指示对象：

      var
          a = array [0..10] of integer;
          i: integer;
      begin
          @i := a;

      将被转换成为

           i.watch(a)

支持的数据类型说明：

    对于没有赋值的变量，其值 value 为 None；

    Array :

        内部存储的值和默认值，

            value 是一个 dict 类型，键值是 int 类型；

            数组元素的默认值是 None，表示数组元素没有赋值；

            空数组，value = {}

        在数据池中保存的方式，

            repr(value) 之后的结果； 对每一个数组元素，也会转
            换成其对应数据类型的数据池格式；

        动态数组的保存形式，

        数组元素没有赋值的形式，

    Boolean :

    Char :

    Integer :

    Pointer :

        内部存储的值和默认值

            value 是一个 BaseType 的继承类实例，表示指针指向的对象；

            空指针，value 如果是 BaseType 的实例，那么表示是空指针；

        在数据池中保存的方式，

            value 是一个 '[ name ]' 的列表，其中 name 表示指
            针指向的对象名称，一般这个名称就是数据池中另外一
            个项的名称；

            空指针，value = [ '' ] 的列表，有一个元素，但其值是空字符串。

        使用方式：

            声明
            k : integer;
            p : ^Integer;

            赋值
            new(p);
            p = @k;
            p = Addr(k);

            引用
            ^p
            ^p + 3
            p1 = p2 判断两个指针指向的对象是否相同；

    Real :

    Record :

        内部存储的值和默认值，

            value 是一个 dict 类型，键值是 str 类型，就是类型
            声明中的元素名称；

            结构元素的默认值是其数据类型对应的默认值；

        在数据池中保存的方式，

            就是将内部值 repr 之后的结果；

    String :

    Tree :

        内部存储的值和默认值，

            value 是一个 dict 类型，键值包括 'value'，'children',
                  前者是结点的值，后者是一个列表，列表中每一个元
                  素都是子结点。

                  二叉树有三个键值: 'value', 'lchild', 'rchild'

            空树，value = {}

        在数据池中保存的方式，

            就是将内部值 repr 之后的结果；

"""
import sys

# 算法驱动实例
DRIVER = None

# 可见数据选项
VOPTIONS = {}

# 数据池
DATAPOOL = {}

class AlgorithmError(Exception): 
    """算法本身出现的运行错误。
    主要有下面三种类型：
    1. 类型不匹配，譬如一个字符串和数值相加的操作
    2. 数组下标越界或者不存在的记录成员
    3. 试图读一个尚未初始化的变量
    4. 除以 0
    """
    emsg = ("", 
            "dismatch type", 
            "index override or unknown member", 
            "uninitialized variable", 
            "divide zero"
            )
    def __init__(self, ecode, *args):
        """初始化算法异常。
        ecode, 错误代码，每一个错误消息都有对应的代码。
        *args, 格式字符串需要的参数，依次列出全部的参数
        """
        Exception.__init__(self, self.emsg[ecode], *args)


class BaseType(object):
    """基础数据类型定义。

    使用新类风格，可以通过 type(实例) 的方式得到类对象。

    属性：

        driver, 算法类对应的驱动, 使用全局变量代替；

        id，

        tagid 字符串类型，= 'tag%d' % id(self)

        name,

        value, 内部使用 get_value，可以避免 None 异常

        options, 显示选项，参考 datapool.py 中定义的选项；基
                 本一致，除了这里没有 type 和 value 两个元素

    内部属性：

        __frame，创建变量所在的调用堆栈。

        __value，内部数据，对象的真正值。

                 非指针类型必须是 Python 中支持的数据类型；
                 指针类型的值必须是 BaseType 或者其子类的实例；

                 空指针的 __value 也是一个 BaseType() 类实
                 例，但是该实例的 value 为 None。

                 Integer, Float, String 对应相应的 int, float, str 类型；
                 Record 对应 dict 类型，键值类型为 str；
                 Array 对应 dict 类型，键值为 int 类型；
                 Set 对应 set 类型；
                 Pointer 对应 BaseType 或者其子类的实例；

                 __value is None 意味着没有初始化的值；譬如 new 操作之后。
                 
        __name，可以指定其名称，如果不指定则自动取名称。

    使用约束：

        变量的创建必须在对应的算法类中，譬如
            p = Pointer()
            i = Integer()

    支持的方法：

        基本运算符；

        declare，用于在局部堆栈中声明一个变量；
        destroy，用于毁灭一个局部堆栈变量；

        new,     用于在全局堆栈中创建一个变量；
        dispose, 用于释放在全局堆中的数据变量；

        clone, 用于值参的传递，创建值参变量；
        refer，用于变参的传递，创建变量参数；

        set, 设置变量的值；
        get, 得到变量的值；

    当变量转换成为字符串保存的时候：

        value 属性直接使用 repr() 进行转换；

        唯一例外的是 Pointer 类型，其 value 使用下面的表达式转换:

        repr([ value.name ])

    """
    def __init__(self, value=None, options=None):
        self.__frame = sys._getframe(1)
        self.__name = None
        self.__value = value
        if options is None:
            self.__options = VOPTIONS["single"].copy()
        else:
            self.__options = options

    def __getattr__(self, name):
        if name == "name":
            if self.__name is not None:
                return self.__name
            data = self.__frame.f_locals
            for (k, v) in data.iteritems():
                if v is self:
                    return str(k)
            data = self.__frame.f_globals
            x = data.get("DATAPOOL", {})
            for (k, v) in x.iteritems():
                if v is self:
                    return str(k)
            return ""

        elif name == "tagid":
            return "tag%d" % id(self)

        elif name == "driver":
            return DRIVER

        elif name == "value":
            return self.__value

        elif name == "visible":
            return self.__options["visible"]

        elif name == "options":
            return self.__options

        else:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name == "value":
            # 监控变量，这里不注释会导致断点检查发生死循环
            # 因为在断点中计算表达式要读变量的值，就又跑到
            # 这里来了
            # DRIVER.monitor_variable(self.__frame, self.name, "w")
            if value is None:
                pass
            elif issubclass(type(self), Pointer):
                assert(issubclass(type(value), BaseType))
            else:
                assert(not issubclass(type(value), BaseType))
            self.__value = value
            DRIVER.simulate_memory_update(self)

            if self.visible:
                DRIVER.simulate_update_variable(self, value)

        elif name == "frame":
            self.__frame = value

        elif name == "name":
            assert(isinstance(value, basestring))
            self.__name = value

        elif name == "visible":
            assert(isinstance(value, int))
            self.__options["visible"] = 1 if value else 0

        else:
            object.__setattr__(self, name, value)

    def get(self):
        """外部算法使用，空值会抛出算法异常。"""
        if self.__value is None:
            raise AlgorithmError(_("Variable might not be initialized"))
        # 监控变量
        # DRIVER.monitor_variable(self.__frame, self.name, "r")        
        return self.__value

    def assign(self, value):
        if value is None:
            self.value = None
        else:
            assert(issubclass(type(value), BaseType))
            self.value = value.get()

    def declare(self):
        """显示一个变量对应的可见对象，用于局部变量声明。"""
        if self.visible:
            name = self.name

        if self.visible:
            self.driver.simulate_declare_var(self)

    def destroy(self):
        """删除变量对应的可见对象，用于函数退出时候释放变量和参数。"""
        self.driver.simulate_remove_variable(self)
        self.visible = 0

    def select(self):
        """选中变量对应的可见对象。"""
        if self.visible:
            self.driver.simulate_select_variable(self)

    def active(self):
        """激活变量对应的可见对象。"""
        self.driver.simulate_active_variable(self)

    def deactive(self):
        """恢复激活状态变量对应的可见对象。"""
        self.driver.simulate_deactive_variable(self)

    def hide(self):
        """隐藏变量对应的可见对象，隐藏文本和标题。

        hide 和 destroy 不一样，后者会删除结点的图片，而前者
        只是隐藏文本和标题，其所在区域还是不变。

        """
        self.driver.simulate_hide_variable(self)
        self.visible = 0

    def show(self):
        """显示变量对应的可见对象。 """
        self.driver.simulate_show_variable(self)
        self.visible = 1

    def vcopy(self, source):
        """复制 source 对应的可见对象的可见属性。 """
        if source is None: return
        self.value = source.value
        self.driver.simulate_copy_variable(source, self)

    def clone(self):
        """生成一个新的实例，应用于参数传递的值参处理。
        value 直接拷贝过去；

        """
        obj = self.__new__(type(self))
        if isinstance(self.value, dict):
            type(self).__init__(
                obj,
                value=self.value.copy(),
                )
        else:
            type(self).__init__(
                obj,
                value=self.value,
                )
        obj.frame = sys._getframe(1)
        if issubclass(type(self), Pointer):
            obj.pcls = self.pcls
        return obj

    def new(self):
        """增加对象到全局堆. """
        self.driver.simulate_new_variable(self)

    def dispose(self):
        """删除对象从全局堆. """
        self.driver.simulate_dispose_variable(self)

    def __add__(self, other):
        assert(other is not None)
        assert(issubclass(type(other), BaseType))
        assert(not issubclass(type(self.value), BaseType))
        assert(not issubclass(type(other.value), BaseType))

        value = self.value + other.value
        obj = self.__new__(type(self))
        type(self).__init__(obj, value=value)
        obj.frame = sys._getframe(1)
        return obj

    def __sub__(self, other):
        assert(other is not None)
        assert(issubclass(type(other), BaseType))
        assert(not issubclass(type(self.value), BaseType))
        assert(not issubclass(type(other.value), BaseType))

        value = self.value - other.value
        obj = self.__new__(type(self))
        type(self).__init__(obj, value=value)
        obj.frame = sys._getframe(1)
        return obj

    def __mul__(self, other):
        assert(other is not None)
        assert(issubclass(type(other), BaseType))
        assert(not issubclass(type(self.value), BaseType))
        assert(not issubclass(type(other.value), BaseType))

        value = self.value * other.value
        obj = self.__new__(type(self))
        type(self).__init__(obj, value=value)
        obj.frame = sys._getframe(1)
        return obj

    def __div__(self, other):
        assert(other is not None)
        assert(issubclass(type(other), BaseType))
        assert(not issubclass(type(self.value), BaseType))
        assert(not issubclass(type(other.value), BaseType))

        value = self.value / other.value
        obj = self.__new__(type(self))
        type(self).__init__(obj, value=value)
        obj.frame = sys._getframe(1)
        return obj

    def __neg__(self):
        assert(not issubclass(type(self.value), BaseType))
        value = - self.value
        obj = self.__new__(type(self))
        type(self).__init__(obj, value=value)
        obj.frame = sys._getframe(1)
        return obj

    def __pos__(self):
        assert(other is not None)
        assert(issubclass(type(other), BaseType))
        assert(not issubclass(type(self.value), BaseType))
        assert(not issubclass(type(other.value), BaseType))

        value = + self.value
        obj = self.__new__(type(self))
        type(self).__init__(obj, value=value)
        obj.frame = sys._getframe(1)
        return obj

    def __mod__(self, other):
        assert(other is not None)
        assert(issubclass(type(other), BaseType))
        assert(not issubclass(type(self.value), BaseType))
        assert(not issubclass(type(other.value), BaseType))

        value = self.value % other.value
        obj = self.__new__(type(self))
        type(self).__init__(obj, value=value)
        obj.frame = sys._getframe(1)
        return obj

    def __invert__(self):
        assert(other is not None)
        assert(issubclass(type(other), BaseType))
        assert(not issubclass(type(self.value), BaseType))
        assert(not issubclass(type(other.value), BaseType))

        value = not self.value
        obj = self.__new__(type(self))
        type(self).__init__(obj, value=value)
        obj.frame = sys._getframe(1)
        return obj

    def __and__(self, other):
        assert(other is not None)
        assert(issubclass(type(other), BaseType))
        assert(not issubclass(type(self.value), BaseType))
        assert(not issubclass(type(other.value), BaseType))

        value = self.value and other.value
        obj = Boolean(value)
        obj.frame = sys._getframe(1)
        return obj

    def __or__(self, other):
        assert(other is not None)
        assert(issubclass(type(other), BaseType))
        assert(not issubclass(type(self.value), BaseType))
        assert(not issubclass(type(other.value), BaseType))

        value = self.value or other.value
        obj = Boolean(value)
        obj.frame = sys._getframe(1)
        return obj

    def __lt__(self, other):
        assert(other is not None)
        assert(issubclass(type(other), BaseType))
        assert(not issubclass(type(self.value), BaseType))
        assert(not issubclass(type(other.value), BaseType))

        value = self.value < other.value
        obj = Boolean(value)
        obj.frame = sys._getframe(1)
        return obj

    def __le__(self, other):
        assert(other is not None)
        assert(issubclass(type(other), BaseType))
        assert(not issubclass(type(self.value), BaseType))
        assert(not issubclass(type(other.value), BaseType))

        value = self.value <= other.value
        obj = Boolean(value)
        obj.frame = sys._getframe(1)
        return obj

    def __eq__(self, other):
        if other is None:
            value = False
        else:
            assert(issubclass(type(other), BaseType))
            assert(not issubclass(type(self.value), BaseType))
            assert(not issubclass(type(other.value), BaseType))
            value = (self.value == other.value)
        obj = Boolean(value)
        obj.frame = sys._getframe(1)
        return obj

    def __ne__(self, other):
        assert(other is not None)
        assert(issubclass(type(other), BaseType))
        assert(not issubclass(type(self.value), BaseType))
        assert(not issubclass(type(other.value), BaseType))

        value = self.value <= other.value
        obj = Boolean(value)
        obj.frame = sys._getframe(1)
        return obj

    def __gt__(self, other):
        assert(other is not None)
        assert(issubclass(type(other), BaseType))
        assert(not issubclass(type(self.value), BaseType))
        assert(not issubclass(type(other.value), BaseType))

        value = self.value > other.value
        obj = Boolean(value)
        return obj

    def __ge__(self, other):
        assert(other is not None)
        assert(issubclass(type(other), BaseType))
        assert(not issubclass(type(self.value), BaseType))
        assert(not issubclass(type(other.value), BaseType))

        value = self.value >= other.value
        obj = Boolean(value)
        obj.frame = sys._getframe(1)
        return obj

    def __contains__(self, item):
        assert(other is not None)
        assert(issubclass(type(other), BaseType))
        assert(not issubclass(type(self.value), BaseType))
        assert(not issubclass(type(other.value), BaseType))

        value = item.get() in self.value
        obj = Boolean(value)
        obj.frame = sys._getframe(1)
        return obj

    def __nonzero__(self):
        if self.value is None: 
            return False
        if issubclass(type(self.value), BaseType):
            return True
        elif isinstance(self.value, (dict, list, basestring)):
            return len(self.value) > 0
        elif isinstance(self.value, (int, float)):
            return self.value != 0
        elif isinstance(self.value, bool):
            return self.value
        else:
            return self.value.__nonzero__()

    def __int__(self):
        assert(self.value is not None)
        assert(not issubclass(type(self.value), BaseType))
        return self.value.__int__()

    def __long__(self):
        assert(self.value is not None)
        assert(not issubclass(type(self.value), BaseType))
        return self.value.__long__()

    def __float__(self):
        assert(self.value is not None)
        assert(not issubclass(type(self.value), BaseType))
        return self.value.__float__()

    def __str__(self):
        assert(not issubclass(type(self.value), BaseType))
        if self.value is None:
            return ""
        else:
            return str(self.value)

class Char(BaseType):
    def __init__(self, value=None, options=None):
        BaseType.__init__(self, value, options=options)
        self.frame = sys._getframe(1)

class Boolean(BaseType):
    def __init__(self, value=None, options=None):
        if value is None:
            value = False
        elif not isinstance(value, bool):
            value = bool(value)
        BaseType.__init__(self, value, options=options)
        self.frame = sys._getframe(1)

class Integer(BaseType):
    def __init__(self, value=None, options=None):
        if value is not None:
            value = int(value)
        BaseType.__init__(self, value, options=options)
        self.frame = sys._getframe(1)

class Real(BaseType):
    def __init__(self, value=None, options=None):
        if value is not None:
            value = float(value)
        BaseType.__init__(self, value, options=options)
        self.frame = sys._getframe(1)

class String(BaseType):
    def __init__(self, value=None, options=None):
        if value is not None:
            value = str(value)
        BaseType.__init__(self, value, options=options)
        self.frame = sys._getframe(1)

class Enum(BaseType):
    def __init__(self, value=None, options=None):
        BaseType.__init__(self, value, options=options)
        self.frame = sys._getframe(1)
        self.data_dict = {}

class Set(BaseType):
    def __init__(self, value=None, options=None):
        BaseType.__init__(self, value, options=options)
        self.frame = sys._getframe(1)

class Struct(BaseType):
    def __init__(self, value={}, options=None):
        assert(isinstance(value, dict))
        if options is None:
            options = VOPTIONS["struct"].copy()
        BaseType.__init__(self, value.copy(), options=options)
        self.frame = sys._getframe(1)
        self.size = len(value)

    def __setitem__(self, key, value):
        assert(issubclass(type(value), (BaseType, type(None))))
        assert(isinstance(self.value, dict))

        if not isinstance(key, (basestring, int)):
            key = key.value
        assert(isinstance(key, (basestring, int)))

        if value is None:
            self.value[key] = None        
        elif self.value.has_key(key) and (self.value[key] is not None):
            self.value[key].assign(value)
        else:
            # 动态生成变量的时候被调用，譬如 New 和 SetLength 函数
            # 用来初始化元素
            obj = type(value).__new__(type(value))
            type(value).__init__(obj)
            obj.frame = sys._getframe(1)
            self.value[key] = obj
            obj.name = str(key)
            
    def __getitem__(self, key):
        if not isinstance(key, (basestring, int)):
            key = key.value
        assert isinstance(key, (basestring, int)), type(key)
        return self.value.get(key, None)

    def __str__(self):
        result = ""
        indent = " " * 4
        _keys = [k for k in self.value.keys()]
        _keys.sort()
        for k in _keys:
            v = self.value[k]
            if issubclass(type(v), Struct):
                s1 = "{0:>5}: (\n".format(k)
                s2 = "{0}".format(v).replace("\n", "\n" + indent).rstrip()
                s3 = "\n{0:>{1}}".format(")", len(s1) - 1)
                result  += s1 + indent + s2 + s3 + "\n"
            else:
                result += "{0:>5}: {1}\n".format(k, v)
        return result

class Record(Struct):

    def __init__(self, value={}, options=None):
        Struct.__init__(self, value=value, options=options)
        self.frame = sys._getframe(1)

    def build(self, value, data, level):
        self.value.clear()
        keys = value.iterkeys()
        keys.sort()

        for k in keys:
            v = eval(value[k])
            obj = build_item(v, data, level)
            self.value[k] = obj
            self.value[k].frame = sys._getframe(1)

class Array(Struct):
    def __init__(self, value={}, cls=BaseType, options=None):
        Struct.__init__(self, value=value, options=options)
        self.frame = sys._getframe(1)
        self.pcls = cls
        
    def resize(self):
        """重画自身。一般用于动态生成的数组。"""
        self.driver.simulate_update_variable(self, self.value)
        
    def build(self, value, data, level):
        self.value.clear()
        keys = [ int(k) for k in value.iterkeys()]
        keys.sort()

        for k in keys:
            v = value[str(k)]
            assert(isinstance(v, dict))
            obj = build_item(v, data, level)
            self.value[k] = obj
            self.value[k].frame = sys._getframe(1)

class Pointer(BaseType):
    """指针数据类型。"""

    def __init__(self, value=None, options=None, cls=BaseType):
        """初始化指针变量， value 必须是第一个参数. """
        if value is None:
            value = BaseType()
        if options is None:
            options = VOPTIONS["pointer"].copy()
        BaseType.__init__(self, value=value, options=options)
        self.frame = sys._getframe(1)
        if cls:
            self.pcls = cls
        if value:
            self.pcls = type(value)

    def assign(self, value):
        if value is None:
            self.value = None
        else:
            assert(issubclass(type(value), BaseType))
            if issubclass(type(value), Pointer):
                self.value = value.get()
            else:
                self.value = value
    
    def __eq__(self, other):
        assert(issubclass(type(other), Pointer))
        if self.value is None:
            return other.value is None or type(other.value) is BaseType
        if other.value is None:
            return self.value is None or type(self.value) is BaseType
        assert(issubclass(type(self.value), BaseType))
        assert(issubclass(type(other.value), BaseType))
        if type(self.value) is type(other.value):
            if type(self.value) is BaseType:
                return True
            else:
                return self.value is other.value
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __setitem__(self, key, value):
        """仅仅适用于指向动态数组的指针。"""
        assert(issubclass(type(value), (BaseType, type(None))))
        assert(issubclass(type(self.value), (Array, type(None))))
        self.value[key] = value
            
    def __getitem__(self, key):
        """仅仅适用于指向动态数组的指针。"""
        assert(issubclass(type(self.value), (Array, type(None))))        
        return self.value[key]

    def __str__(self):
        if self.value is None:
            return "nil"
        else:
            assert(issubclass(type(self.value), BaseType))
            if self.value.name == "":
                return "->({0})".format(id(self))
            else:
                return "-> {0}".format(self.value.name)

    def build(self, value, data, level):
        if not value == "":
            self.value = data[value]

class Tree(Struct):
    """内置树结构对象。

    一个简单的二叉树类型，只能显示文本。
    属性：
        lchild,    左孩子；
        rchild,    右孩子；
        title，    树结点对应的文本，String()。
        value,     树结点对应的值，可以是任意的 BaseType 上的类型。

    空树：
        self.value = {}     表示是一棵空树

    """
    def __init__(self, value={}, options=None):
        assert(isinstance(value, dict))
        if options is None:
            options = VOPTIONS["tree"].copy()
        Struct.__init__(self, value, options=options)
        self.frame = sys._getframe(1)

    def is_empty_tree(self):
        return len(self.value) == 0

    def build(self, value, data, level):
        level += 1
        tree = value
        obj = String(tree.get("title", None))
        obj.frame = sys._getframe(level)
        self.value["title"] = obj
        obj = String(tree.get("value", None))
        obj.frame = sys._getframe(level)
        self.value["value"] = obj

        child = tree.get("lchild", {})
        assert(isinstance(child, dict))
        if child:
            obj = Tree(options=self.options)
            obj.frame = sys._getframe(level)
            obj.build(child, data, level)
        else:
            obj = BaseType()
            obj.frame = sys._getframe(level)
        self.value["lchild"] = Pointer(cls=Tree, value=obj)
        self.value["lchild"].frame = sys._getframe(level)

        child = tree.get("rchild", {})
        assert(isinstance(child, dict))
        if child:
            obj = Tree(options=self.options)
            obj.frame = sys._getframe(level)
            obj.build(child, data, level)
        else:
            obj = BaseType()
            obj.frame = sys._getframe(level)
        self.value["rchild"] = Pointer(cls=Tree, value=obj)
        self.value["rchild"].frame = sys._getframe(level)

class Indexpointer(Integer):
    """指向数组下标的可见对象类型。

    它的值本身是一个整型，但是其对应的可见对象指向了相应的数组元素。

    使用方法：
    var
        arr: array [0..10] of String;
        x: IndexPointer;               { 声明一个数组下标指针. }
    begin
        x := @arr;
        x := 0;
    end;

    """
    def __init__(self, value=None, options=None, data=None):
        Integer.__init__(self, value=value, options=None)
        self.frame = sys._getframe(1)
        self.array = None
        self.pointer = None
        if data:
            self.__pointer(data)
            
    def __pointer(self, data):
        if issubclass(type(data), Array):
            pvalue = data
        elif issubclass(type(data), Pointer):
            pvalue = data.value
        else:
            raise AlgorithmError(1, "Array, Pointer", type(data).__name__)
        if issubclass(type(pvalue), Pointer):
            pvalue = pvalue.value
        if not issubclass(type(pvalue), Array):
            raise AlgorithmError(1, "Array", type(pvalue).__name__)

        self.array = pvalue
        # 创建一个可见的指针对象
        if self.pointer is None:
            self.pointer = Pointer()
            self.pointer.name = self.name
            self.pointer.declare()
                
    def assign(self, value):
        if issubclass(type(value), Integer):
            self.value = int(value)
            # 显示指向数组元素的指针
            v = self.array[value]
            self.pointer.assign(v)
        elif issubclass(type(value), (Array, Pointer)):
            self.__pointer(value)
        else:
            raise AlgorithmError(1, "IndexPointer", type(value).__name__)
            
    def destroy(self):
        if self.pointer:
            self.pointer.destroy()
        
    # def __str__(self):
    #     if self.array is None or self.value is None:
    #         return "nil"
    #     else:
    #         assert(issubclass(type(self.value), BaseType))
    #         name = self.array.name
    #         if name == "":
    #             name == str(id(self))
    #         return "-> {0}[{1}]".format(name, self.index)
    def clone(self):
        """生成一个新的实例，应用于参数传递的值参处理。
        需要复制 array 和 pointer，无法使用基类的方法。

        """
        obj = self.__new__(type(self))
        type(self).__init__(obj, value=self.value)
        obj.frame = sys._getframe(1)
        obj.array = self.array
        obj.pointer = Pointer()
        if self.pointer:
            obj.pointer.assign(self.pointer.value)
        obj.pointer.name = self.name
        obj.pointer.declare()
        return obj

class Queue(Array): pass

class Graph(Struct): pass

def datapool(name, type_name):
    if name not in DATAPOOL:
        DRIVER.player.data_pool.insert(name)
    x = build_item(DATAPOOL[name], {})
    x.name = name
    return x
        
def build_datapool(data):
    """根据数据池的子集构建基于 BaseType 对象的数据集合。"""
    x = {}
    for k, v in data.iteritems():
        x[k] = build_item(v, x)
    return x

def build_item(item, data, level=2):
    tname = item["type"]
    text = item["value"]
    if text:
        value = eval(item["value"])
    else:
        value = None
    options = item.copy()
    del options["type"]
    del options["value"]
    if tname == "Integer":
        obj = Integer(value, options=options)
    elif tname == "Boolean":
        obj = Boolean(value, options=options)
    elif tname == "Char":
        obj = Char(value, options=options)
    elif tname == "String":
        obj = String(value, options=options)
    elif tname == "Real":
        obj = Real(value, options=options)
    elif tname == "Array":
        obj = Array(options=options)
        obj.build(value, data, level)
    elif tname == "Record":
        obj = Record(options=options)
        obj.build(value, data, level)
    elif tname == "Tree":
        obj = Tree(options=options)
        obj.build(value, data, level)
    elif tname == "Pointer":
        obj = Pointer(options=options)
        obj.build(value, data, level)
    else:
        raise Exception("impossible")
    return obj


if __name__ == '__main__':
    import gettext
    gettext.NullTranslations().install()

    i = BaseType(1)
    print i.name

    k = Integer(2)
    print k, k.name

    j = Integer(3)
    print j, j.name

    m = k + j
    print m, m.name

    a = Array()

    a.build("{'0':'1'}", {}, size=3)
    print a

    k = Integer(0)
    print 'k is ', k

    k = Boolean(False)
    print 'k is ', k

    p1 = Pointer()
    p2 = Pointer(value=k)

    print p1==p2

    s = String(value="abc")

    class Ca():

        def __init__(self, x):
            self.prop = x

        def fp(self):
            print "Ca:", self.prop

    class Cb():

        def test(self):
            self.y = {0: "a"}
            obj = Ca(self.y)

            self.y[1] = 'b'
            obj.fp()

            obj.prop[2] = 'c'
            print 'cb:', self.y

    k = Cb()
    k.test()