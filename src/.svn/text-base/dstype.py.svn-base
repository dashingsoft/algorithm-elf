# -*- coding: utf-8 -*-
#
#############################################################
#                                                           #
#      版权所有 2009 - 2010 德新软件公司。保留全部权利。    #
#                                                           #
#      数据结构算法助手                                     #
#                                                           #
#      版本区间：1.0.0 - 1.2.1                              #
#                                                           #
#############################################################
#
# @文件：dstype.py
#
# @作者：赵俊德(jondy.zhao@gmail.com)
#
# @创建日期: 2010/02/28
#
# @文件说明
#
#     定义树、图和队列从字符串向列表结构相互转换的类对象。
#
# 目前支持的算法参数：
#     StringArray
#     StringTree
#     StringGraph
#     
# @丢弃日期：2010/03/05 赵俊德
#
#  使用 eval 计算表达式的方式直接转换字符串到对应的结构，这个
#  文件的方式即复杂又麻烦，不再使用这种方式。
#
#    

# 配置文件中字符串参数的最大长度，一般不需要很长的
__MAX_PARAMETER_LENGTH__ = 4096


class StringParameter(object):

    def parseStrNode(self, strnode):
        """ 将 '名称部分 ( 属性=值, ... )' 格式的 的字符串解
        析成为一个列表，(名称部分, {属性字典}) """

        # 使用 “(” 分开名称和属性
        _index = strnode.find("(")
        if _index == -1:
            _name = strnode.strip()            
            return (_name, {}) # 只有名称，没有属性

        # 检查名称
        _name = strnode[:_index].strip()        

        # 得到属性字符串
        _propstr = strnode[_index:].strip()
        if not ( _propstr.startswith('(') and
                 _propstr.endswith(')') ):
            raise dsException.dsError(
                6009,
                self.__emsg(6009),
                strnode,
                _propstr
                )
        # 删除前后的括号以及括号里面的空格
        _propstr = _propstr.lstrip('(').rstrip(')').strip()

        # 分解属性字符串成为单独的属性
        _pdict = {}
        for kv in _propstr.split(','):
            _plist = kv.strip().split('=')
            if len(_plist) != 2:
                raise dsException.dsError(
                    6010,
                    self.__emsg(6010),
                    strnode,
                    kv
                    )
            _pdict[_plist[0].strip()] = _plist[1].strip()

        # 返回分解的结果
        return (_name, _pdict)


class StringArray(StringParameter):
    """ 字符串格式的数组对象。

字符串数组定义方式：

    以分号作为分隔符号的多个字符串元素，每一个字符串元素
    只能使用数值，字母，unicode也支持。

构造函数，传入字符串形式的数组列表

内部结构

    __data = [ 结点元素, ... ]

    结点元素 = [ 名称, 值, 属性字典 ]

    其中名称按照初始化参数初始化为连续的字符串，不支持 unicode
    例如，
        r0, r1, r2 ...
        s_2, s_3, s_4, s_5 ...

    第一个元素的初始计数值根据初始化参数传入的值确定，缺
    省值是从 0 开始。

    数组元素的值只能是字符串或者数值，不能是其他类型。


方法：
    __init__ 初始化，传入unicode编码的数组描述符，
                     可选参数包括
                         名字的模版，
                         名称开始计数值
    get(index)
    getString(index)，
    getInt(index),
    getFloat(index),
    setValue(index, value)，
    
    setProperty(index, name，value)
    getProperty(index, name, default)
    updateProperty(index, **args)
    
    setDefaultProperties(**args)
    
    getList()
    getIntList()
    getFloatList()
    getStringList()
    
    len()
    index(value)
    remove(value)
    append(name, value, **args)
    insert(index, name, value, **args)
    __str__,

异常：

   构造异常，

说明
    1. 如果传入的空，那么返回一个空列表。
    2. 最后的逗号可有可无。
    3. 如果只有一个逗号，那么返回一个空列表。
    
"""
    
    def __init__(self, namepattern, strarray, start=0):

        """ 根据字符串格式的数组生成一个列表，每一个列表元素
        为[ 名称，属性 ] 其中名称是字符串或者数值。属性是一个
        字典 """

        # 参数检查        
        _strarray = self.validateConfigurePrameter(strarray)

        # 删除后面的逗号，并且按照以逗号分隔形成列表
        _sperator = ','
        self.__data = []
        _counter = start
        for value in _strarray.rstrip(_sperator).split(_sperator):
            _name = namepattern.format(_counter)
            self.validateNodeName(_name)
            self.__data.append(
                [_name, value, {}]
                )
            _counter += 1

    def getName(self, index):
        try:
            return self.__data[index][0]
        except KeyError:
            raise dsException.dsError(
                6100,
                self.__emsg(6100),
                self.__data,
                index
                )
        
    def get(self, index):
        try:
            return self.__data[index][1]
        except KeyError:
            raise dsException.dsError(
                6100,
                self.__emsg(6100),
                self.__data,
                index
                )

    def getString(self, index):
        return self.get(index)

    def getInt(self, index):
        _value = self.get(index)
        try:
            return int(_value)
        except TypeError:
            raise dsException.dsError(
                6101,
                self.__emsg(6101),
                index,
                _value
                )

    def getFloat(self, index):
        _value = self.get(index)
        try:
            return float(_value)
        except TypeError:
            raise dsException.dsError(
                6102,
                self.__emsg(6102),
                index,
                _value
                )

    def setValue(self, index, value):
        if not (isinstance(value, int) or
                isinstance(value, long) or
                isinstance(value, float) or
                isinstance(value, basestring)):
            raise dsException.dsError(
                6103,
                self.__emsg(6103),
                value,
                type(value)
                )
        try:
            self.__data[index][1] = value
        except KeyError:
            raise dsException.dsError(
                6100,
                self.__emsg(6100),
                (self.__data, index)
                )

    def setProperty(self, index, name, value):
        try:
            self.__data[index][2][name] = value
        except KeyError:
            raise dsException.dsError(
                6100,
                self.__emsg(6100),
                (self.__data, index)
                )

    def updateProperty(self, index, **args):
        for (pname, pvalue) in args.iteritems():
            self.setProperty(index, pname, pvalue)
            
    def getProperty(self, index, name, default=None):
        try:
            _properties = self.__data[index][2]
        except KeyError:
            raise dsException.dsError(
                6100,
                self.__emsg(6100),
                (self.__data, index)
                )
        try:
            return _properties[name]
        except KeyError:
            return default

    def getIntList(self):
        _result = self.getList()
        return map(int, _result)        

    def getFloatList(self):
        _result = self.getList()
        return map(float, _result)
    
    def getStringList(self):
        return self.getList()
    
    def getList(self):
        _result = []
        for i in range(len(self.__data)):
            _result.append(self.get(i))
        return _result


    def setDefaultProperties(self, **args):
        for _index in range(self.len()):
            self.updateProperty(_index, **args)
            
    def len(self):
        return len(self.__data)

    def index(self, value):
        data = self.getList()
        return data.index(value)

    def remove(self, value):
        i = self.index(value)
        del self.__data[i]

    def append(self, name, value, **args):
        # 检查名称是否已经存在

        # 插入到数据列表中
        self.__data.append(
            [ name, value, args ]
            )

    def insert(self, index, name, value, **args):
        # 检查名称是否已经存在

        # 插入到数据列表中
        self.__data.insert(
            index,
            [ name, value, args ]
            )

    def __str__(self):
        _value = ""
        for i in range(len(self.__data)):
            _value += "%s:%s:%s\n" % (
                self.__data[i][0],
                self.__data[i][1],
                self.__data[i][2],
                )
        return _value
    
    def __emsg(self, ecode):
        """ 返回错误代码对应的消息格式字符串 """
        
        # 代码：6100
        # 参数：列表，索引
        # 描述：索引超出列表范围
        #
        if ecode == 6100:
            return ("index '{1}' out of range "
                    "in the list '{0}'")

        # 代码：6101
        # 参数：索引值，参数值
        # 描述：要转换的参数值不是一个整数
        #
        if ecode == 6101:
            return ("'{1}' in the data['{0}'] is "
                    "invalid literal for integer")
        
        # 代码：6102
        # 参数：索引值，参数值
        # 描述：要转换的参数值不是一个浮点数
        #
        if ecode == 6102:
            return ("'{1}' in the data['{0}'] is "
                    "invalid literal for float")
        
        # 代码：6103
        # 参数：参数，参数数据类型
        # 描述：数组元素的数据类型只能数值和字符，不能是其他类型
        #
        if ecode == 6103:
            return ("data type '{1}' of '{0}' is not supported "
                    "in the StringArray")
                
        # 未知的错误代码
        assert False, "unknown error code %d" % ecode

    

class StringTree(StringParameter):
    """ 字符串格式的树对象。
    
字符串树定义方式：

    字符串树是以分号分开的多个结点描述，格式如下

        字符串树 = 复合结点; 复合结点; ...
        空树 = 空字符串

        最后一个结点的分号可有可无。

    每一个复合结点是以冒号分开的父子结点对，格式如下：

        复合结点 = 父结点 : [ 孩子结点名称, ... ]

        多个孩子使用逗号分隔。

        注意:
            结点名称是一个字符串，合法的变量名称。
            特殊的结点名称：None，表示一个空结点。

        如果没有孩子结点，那么格式如下

        复合结点 = 父结点

    每一个父结点是结点名称和结点属性的字符串，格式如下：

        父结点 = 结点名称 ( 属性=值, ... )

        如果没有属性，则

        父结点 = 结点名称

        多个属性使用逗号分开
        注意：
            这里的结点名称不可以为 None

    结点名称是一个以 [a-zA-Z_] 的开头的字符串，可以包括的
    合法字符有 数值，下划线和字符。

    结点标准属性：
    结点的标准属性中包括 value, title，以及和位置相关的属
    性：x, y, width, height, relname, relx, rely

    示例：

    1. 下图
              A
             / \
            /   \
           B    C

        描述如下

                A : [ B, C ]

    2. 下图中, B 只有右子树，
              A
             / \
            /   \
           B    C
            \
             \
              D
        描述如下

        A : [ B, C ]; B : [ None, D ]

    3. 使用属性的描述
        A (x=0, y=10) : [ B, C ]; B (value=x)



内部结构

    __data = [ 名称, 值, 属性字典, 孩子列表 或者 None ]


方法：

    __init__ 

    build()  根据传入字符串树构建树
    
    get()
    getString()
    getInt()
    getFloat()
    setValue(value)

    getName()
    
    getProperty(name)
    setProperty(name, value)
    updateProperty(**args)

    getChildren()
    insert(index,child)
    append(child)
    remove(index)
    index(child)

    setChildrenProperty(name, value) 设置全部的孩子的属性
    updateChildrenProperty(**args)
    getChildByName(nodename)

    __str__,  显示 结点名称，孩子列表 和 值

"""
    
    def __init__(self, name=None, value=None, **args):
        if name is not None:
            # 检查结点的名称
            self.validateNodeName(name)
            
            # 初始化数据，孩子列表为 None
            self.__data = [ name, value, args, None ]

            # 检查一下值的合法性
            self.setValue(value)
            
    def build(self, strtree):
        """ 根据字符串树构建树，value 的缺省值是 name """

        # 参数检查
        strTree = self.validateConfigurePrameter(strtree)
        
        strtree = strtree.strip()
        if len(strtree) == 0:
            self.__data = None
            return 

        _pnodes = []    # 存放全部的有孩子的结点
        _pairnodes = [] # 存放结点对 （名称，对应的列表)

        # 处理全部的复合结点
        for strnode in strtree.rstrip(';').split(';'):
            _couple = strnode.split(':')
            _name, _pdict = self.parseStrNode(_couple[0].strip())
            if _name == 'None':
                raise dsException.dsError(
                    6201,
                    self.__emsg(6201),
                    strtree,
                    strnode
                    )
            self.validateNodeName(_name)
            try:
                _value = _pdict['value']
            except KeyError:
                _value = _name
            _node = StringTree(_name, _value, **_pdict)

            _pairnodes.append((_name, _node))
            if len(_couple) == 1:
                _pnodes.append((_node, None))
            else:
                _pnodes.append((_node, _couple[1]))

        # 将孩子结点的名称替换成为实际的实例
        for node, strchildren in _pnodes:
            if strchildren is None:
                continue
            _children = strchildren.strip(
                ).lstrip('[').rstrip(']').split(',')
            _snodes = []
            for childname in _children:
                childname = childname.strip()
                if childname in dict(_pairnodes):
                    node.append(dict(_pairnodes)[childname])
                else:                    
                    if childname == 'None':   # 特殊的子结点
                        node.append(None)
                    else:
                        self.validateNodeName(childname)
                        node.append(
                            StringTree(childname, childname)
                            )

        # 设定 self.__data 根据 _pnodes[0][0]
        self.__data =  _pnodes[0][0].__getData()

    def __getData(self):
        return self.__data
    
    def get(self):
        if self.__data is None:
            raise dsException.dsError(
                6200,
                self.__emsg(6200)
                )
        return self.__data[1]

    def getString(self):
        return self.get()

    def getInt(self):
        _value = self.get()
        try:
            return int(_value)
        except TypeError:
            raise dsException.dsError(
                6202,
                self.__emsg(6202),
                self.getName(),
                _value
                )

    def getFloat(self):
        _value = self.get()
        try:
            return float(_value)
        except TypeError:
            raise dsException.dsError(
                6203,
                self.__emsg(6203),
                self.getName(),
                _value
                )

    def setValue(self, value):
        if self.__data is None:
            raise dsException.dsError(
                6200,
                self.__emsg(6200)
                )
        if not (isinstance(value, int) or
                isinstance(value, long) or
                isinstance(value, float) or
                isinstance(value, basestring)):
            raise dsException.dsError(
                6204,
                self.__emsg(6204),
                self.getName(),
                value,
                type(value)
                )
        self.__data[1] = value

    def setProperty(self, name, value):
        if self.__data is None:
            raise dsException.dsError(
                6200,
                self.__emsg(6200)
                )
        self.__data[2][name] = value

    def updateProperty(self, **args):
        for (name, value) in args.iteritems():
            self.setProperty(name, value)
            
    def getProperty(self, name, default=None):
        if self.__data is None:
            raise dsException.dsError(
                6200,
                self.__emsg(6200)
                )
        _properties = self.__data[2]
        try:
            return _properties[name]
        except KeyError:
            return default


    def getName(self):
        if self.__data is None:
            raise dsException.dsError(
                6200,
                self.__emsg(6200)
                )
        return self.__data[0]

    def getChildren(self):
        if self.__data is None:
            raise dsException.dsError(
                6200,
                self.__emsg(6200)
                )
        if self.__data[3] is None:
            return []
        else:
            return self.__data[3]

    def __setChildren(self, children):
        """ 内部使用，不做参数检查 """
        self.__data[3] = children
        
    def getChildByName(self, name):
        for child in filter(None, self.getChildren()):
            if child.getName() == name:
                return child
        return None

    def insert(self, index, child):
        # 参数检查
        if (child is not None and
            not isinstance(child, StringTree)):
            raise dsException.dsError(
                6206,
                self.__emsg(6206),
                self.getName(),
                child,
                type(child)
                )
        _children = self.getChildren()
        if len(_children) == 0:
            self.__setChildren([child])
        else:
            _children.insert(index, child)

    def append(self, child):
        # 参数检查
        if (child is not None and
            not isinstance(child, StringTree)):
            raise dsException.dsError(
                6206,
                self.__emsg(6206),
                self.getName(),
                child,
                type(child)
                )
        _children = self.getChildren()
        if len(_children) == 0:
            self.__setChildren([ child ])
        else:
            _children.append(child)

    def remove(self, index):
        _children = self.getChildren()
        del _children[index]

    def index(self, child):
        _children = self.getChildren()
        return _children.index(child)

    def setChildrenProperty(self, name, value):
        self.setProperty(name, value)
        for child in filter(None, self.getChildren()):
            child.setChildrenProperty(name, value)

    def updateChildrenProperty(self, **args):
        self.updateProperty(**args)
        for child in filter(None, self.getChildren()):
            child.updateChildrenProperty(**args)
        
    def __str__(self):
        """ 显示当前结点信息: 名称 : [ 孩子名称 ] = 值 """
        if self.__data is None:
            return ""
        _value = "%s" % self.getName()
        _children = self.getChildren()
        _x = len(_children)
        for k in range(_x):
            if k == 0:
                _value = _value + ' : [ '
            _child = _children[k]
            if _child is None:
                _value = _value + 'None'
            else:
                _value = _value + _child.getName()
            if k < _x - 1:
                _value = _value + ', '
            else:
                _value = _value + ' ]'

        #_value += " = '" + self.getString() + "'"
        #for child in filter(None, _children):
        #    _value = "%s; %s" % (_value, child.__str__())
        return _value
    
    def __emsg(self, ecode):
        """ 返回错误代码对应的消息格式字符串 """
        
        # 代码：6200
        # 参数：
        # 描述：不能对空树进行任何操作
        #
        if ecode == 6200:
            return _("tree is empty")

        # 代码：6201
        # 参数：字符串树，复合结点字符串
        # 描述：字符串树中的复合结点的名称不能为 None
        #
        if ecode == 6201:
            return _("in the string tree '{0}' "
                     "the complex node '{1}' has "
                     " the invalid name 'None'")

        # 代码：6202
        # 参数：结点名称，结点值
        # 描述：结点值不是一个合法的整数
        #
        if ecode == 6202:
            return ("the value '{1}' of node '{0}' is "
                    "invalid literal for integer")

        # 代码：6203
        # 参数：结点名称，结点值
        # 描述：结点值不是一个合法的浮点数
        #
        if ecode == 6203:
            return ("the value '{1}' of node '{0}' is "
                    "invalid literal for float")

        # 代码：6204
        # 参数：结点名称，结点值，数据类型
        # 描述：结点值的数据类型是不支持的
        #
        if ecode == 6204:
            return ("data type '{2}' of '{1}' in the node '{0}'"
                    "is not supported in the StringTree")

        # 代码：6205
        # 参数：结点属性参数，结点属性数据类型
        # 描述：结点属性参数必须是字典类型
        #
        if ecode == 6205:
            return _("'{0}' should be a dictionary, not '{1}'")

        # 代码：6206
        # 参数：结点名称，孩子，孩子类型
        # 描述：结点的孩子必须是 StringTree
        #
        if ecode == 6206:
            return _("a StringTree is expected, "
                     "but the actual type of '{0}' is '{1}'")

        # 未知的错误代码
        assert False, "unknown error code %d" % ecode


class StringGraph(StringParameter):
    """字符串格式的图对象定义。
    
字符串格式的图描述方式：

    字符串图是一个以冒号分开的结点组和连线组组成，格式如
    下：

        字符串图 = 结点组 : 连线组
        没有连线的孤立图 = 结点组
        空图 = 空字符串

    结点组是使用分号分开的多个结点，格式如下：

        结点组 = 结点; 结点; ...

        结点组至少包括一个结点，结点组字符串最后的一个分
        号可有可无。

    结点是使用括号包含的结点名称和属性对，格式如下：

        结点 = 结点名称 ( 属性=值, 属性=值, ... )

        或者

        结点 = 结点名称

        结点名称是一个合法的变量名称，但是不可以为 None。

    结点标准属性参见 StringTree 中的说明。

    连线组是一个以分号分隔的多个结点对，相当于边组成，格
    式如下：

        连线组 = 结点对; 结点对; ...


        连续组至少要存在一个结点对，最后一个结点对的分号
        可有可无。

    每一个结点对是使用小括号包含的两个结点加一组属性，格
    式如下：

        结点对 = < 结点名称, 结点名称 > ( 属性=值, 属性=值, ... )

        其中属性和值可以有多组，默认属性包括 arrow，表示连
        线的类型，可选值：none, single, both


内部结构

    __data = [ 结点列表, 连线列表 或者 None ]

    结点列表 = [ 结点, ... ]

    结点 = [ 名称, 值，属性字典 ]

    连线列表 = [ ( 结点名称, 结点名称 ), 属性字典 ]

方法
    __init__  初始化

    setValue(nodename, value)
    getValue(nodename)
    
    getNodes()    返回名称列表        
    getEdges()    返回名称列表

    indexOfNode(nodename)
    indexOfEdge(sourcename, targetname)
    
    getEdgeName(sourcename, targetname)
    
    addEdge(sourcename, targetname, **options)
    removeEdge(sourcename, targetname)

    setNodeProperty(nodename, pname, value)
    getNodeProperty(nodename, pname, default=None)

    setEdgeProperty(sourcename, targetname, pname, value)
    getEdgeProperty(sourcename, targetname, pname, default=None)

"""
    def __init__(self):

        self.__data = None

    def build(self, strgraph):
        """ 根据图的字符串描述生成图列表结构，返回图列表
        
        失败抛出异常

        参数说明
            strgraph 是 unicode 的字符串图

        如果没有 value 属性的化，设置其值为字符串图中的名称。
        """
        
        # 检查从配置文件中得到的参数
        strgraph = self.validateConfigurePrameter(strgraph)

        # 空图
        if len(strgraph.strip()) == 0:
            self.__data = None
            return 

        _nodes = []     # 存放结点表
        _edges = []     # 存放图的边
        _nodeNames = {}  # 存放结点名称和列表的对应关系

        # 分解 结点列表和边列表
        _plist = map(unicode.strip, strgraph.split(":"))
        if len(_plist) > 2:
            raise dsException.dsError(
                6301,
                self.__emsg(6301),
                strgraph
                )
        _strnodes = _plist[0]
        try:
            _stredges = _plist[1].strip().rstrip(';')
        except IndexError:
            _stredges = ""

        # 分解 结点组
        for snode in map(unicode.strip, _strnodes.split(";")):
            if snode == "":
                raise dsException.dsError(
                    6302,
                    self.__emsg(6302),
                    _strnodes
                    )

            # 分解结点
            _name, _pdict = self.parseStrNode(snode.strip())
            if _name == 'None':
                raise dsException.dsError(
                    6303,
                    self.__emsg(6303),
                    _strnodes,
                    snode
                    )
            try:
                _value = _pdict['value']
            except KeyError:
                _value = _name
                
            # 增加结点
            if _name in _nodeNames:     # 重复定义
                raise dsException.dsError(
                    6304,
                    self.__emsg(6304),
                    _strnodes,
                    _name
                    )
            _nodes.append([_name, _value, _pdict])
            _nodeNames[_name] = _nodes[-1]

        # 增加边
        if _stredges == "":
            self.__data = [ _nodes, None ]
            return

        for sedge in map(unicode.strip, _stredges.split(";")):
            # 分解边为结点对和属性
            _name, _pdict = self.parseStrNode(sedge.strip())
            _name = _name.strip()
            if not ( _name.startswith('<') and
                     _name.endswith('>') ):
                raise dsException.dsError(
                    6306,
                    self.__emsg(6306),
                    _stredges,
                    sedge
                    )
            # 分解结点对
            _plist = _name.lstrip('<').rstrip('>').split(',')
            if not (len(_plist) == 2):
                raise dsException.dsError(
                    6307,
                    self.__emsg(6307),
                    sedge,
                    _name
                    )
            _source = _plist[0].strip()
            _target = _plist[1].strip()
            if _source not in _nodeNames:
                raise dsException.dsError(
                    6305,
                    self.__emsg(6305),
                    sedge,
                    _source
                    )            
            if not _target in _nodeNames:
                raise dsException.dsError(
                    6305,
                    self.__emsg(6305),
                    sedge,
                    _target
                    )
       
            # 检查是否已经存在重复的边，不过，有的图允许
            # 两个结点之间存在多条边
            for edge in _edges:
                if (edge[0] == (_source, _target) or
                    edge[0] == (_target, _source)
                    ):
                    raise dsException.dsError(
                        6308,
                        self.__emsg(6308),
                        sedge,
                        edge[0]
                        )

            # 增加一条边
            _edges.append([(_source, _target), _pdict])

        # 返回图列表
        self.__data = [_nodes, _edges]

    def getNodes(self):
        if self.__data is None:
            return []
        _nodes = self.__data[0]
        if _nodes is None:
            return []
        
        _result = []
        for node in _nodes:
            _result.append(node[0])
        return _result
    
    def getEdges(self):
        if self.__data is None:
            return []
        _edges = self.__data[1]
        if _edges is None:
            return []

        _result = []
        for edge in _edges:
            _result.append(edge[0])
        return _result

    def getEdgeName(self, sourcename, targetname):
        if sourcename > targetname:
            return "%s_%s" % (targetname, sourcename)
        else:
            return "%s_%s" % (sourcename, targetname)

    def indexOfNode(self, nodename):
        _nodenames = self.getNodes()
        try:
            return _nodenames.index(nodename)
        except ValueError:
            raise dsException.dsError(
                6309,
                self.__emsg(6309),
                nodename
                )

    def indexOfEdge(self, sourcename, targetname):
        _edgenames = self.getEdges()
        try:
            return _edgenames.index(tuple((sourcename, targetname)))
        except ValueError:
            try:
                return _edgenames.index(tuple((targetname, sourcename)))
            except ValueError:        
                raise dsException.dsError(
                    6310,
                    self.__emsg(6310),
                    tuple((sourcename, targetname))
                    )

    def setValue(self, nodename, value):
        _index = self.indexOfNode(nodename)
        self.__data[0][_index][1] = value

    def getValue(self, nodename):
        _index = self.indexOfNode(nodename)
        return self.__data[0][_index][1]

    def setNodeProperty(self, nodename, pname, value):
        _index = self.indexOfNode(nodename)
        self.__data[0][_index][2][pname] = value

    def getNodeProperty(self, nodename, pname, default=None):
        _index = self.indexOfNode(nodename)
        return self.__data[0][_index][2].get(pname, default)

    def setEdgeProperty(self, sourcename, targetname, pname, value):
        _index = self.indexOfEdge(sourcename, targetname)
        self.__data[1][_index][1][pname] = value
        
    def getEdgeProperty(self, sourcename, targetname, pname, default=None):
        _index = self.indexOfEdge(sourcename, targetname)
        return self.__data[1][_index][1].get(pname, default)        
        
    def __emsg(self, ecode):
        """ 返回错误代码对应的消息格式字符串 """
        
        # 代码：6300
        # 参数：
        # 描述：空图不能进行任何操作
        #
        if ecode == 6300:
            return _("graph is empty")

        # 代码：6301
        # 参数：字符串图
        # 描述：字符串图只能包括一个冒号分隔结点和边
        #
        if ecode == 6301:
            return _("more than one ':' is used "
                     "in the graph string '{0}'")

        # 代码：6302
        # 参数：结点组字符串
        # 描述：结点组字符串中不能包含空的结点字符串
        #
        if ecode == 6302:
            return _("an empty node is in the node string '{0}'")

        # 代码：6303
        # 参数：结点组字符串，结点字符串
        # 描述：结点字符串中的名称不能为 None
        #
        if ecode == 6303:
            return _("a node '{1}' named 'None' is in the node string '{0}'")

        # 代码：6304
        # 参数：结点组字符串，结点字符串
        # 描述：结点字符串中结点已经被定义
        #
        if ecode == 6304:
            return _("duplicated node name '{0}' in the node string '{0}'")

        # 代码：6305
        # 参数：边字符串，结点名称
        # 描述：边字符串中引用的结点不存在
        #
        if ecode == 6305:
            return _("node '{1}' in the edge '{0}' doesn't exist")

        # 代码：6306
        # 参数：边字符串，结点对字符串
        # 描述：结点对字符串必须包含在 <> 中
        #
        if ecode == 6306:
            return _("node string '{1}' in the edge '{0}' "
                     "should be the form '<x,y>'")

        # 代码：6307
        # 参数：边字符串，结点对字符串
        # 描述：结点对字符串必须使用分号分开的两个结点
        #
        if ecode == 6307:
            return _("node string '{1}' in the edge '{0}' "
                     "should be the form '<x,y>'")

        # 代码：6308
        # 参数：边字符串
        # 描述：出现了重复的边
        #
        if ecode == 6308:
            return _("dupliated edge '{0}'")

        # 代码：6309
        # 参数：结点名称
        # 描述：不存在的结点
        #
        if ecode == 6309:
            return _("no node '{0}' found in the graph")

        # 代码：6310
        # 参数：结点对
        # 描述：两个结点之间没有边存在
        #
        if ecode == 6310:
            return _("no edge '{0}' found in the graph")

        # 未知的错误代码
        assert False, "unknown error code %d" % ecode

    

if __name__ == "__main__":
    import gettext
    gettext.NullTranslations().install(unicode=True)
