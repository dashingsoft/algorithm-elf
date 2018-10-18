# -*- coding: utf-8 -*-
#
#############################################################
#                                                           #
#      版权所有 2009 - 2010 德新软件公司。保留全部权利。    #
#                                                           #
#      数据结构算法助手                                     #
#                                                           #
#      版本区间：1.0.0 -                                    #
#                                                           #
#############################################################
#
# @文件：bubbleSort.py
#
# @作者：赵俊德(jondy.zhao@gmail.com)
#
# @创建日期: 2009/07/09
#
# @文件说明
#
# 冒泡排序算法的实现。
#

from dsException import dsError
from baseAlgorithm import baseAlgorithm

__srcCodeMain__ = ( "qksort",
"""
<1>
procedure qksort(var r:listtype; s,t:integer);
{本算法对r[s..t]进行一趟快速排序}
BEGIN
<2>
    if s < t
<3>
        qkpass(r, s, t, k);    
<4>
        qksort(r, s, k - 1);
<5>
        qksort(r, k + 1, t);
<6>
END {end of qksort}
""")

__srcCodeQkpass__ = ( "qkpass",
"""
<1>
procedure qkpass(var r:listtype; s,t:integer; var i:integer);
{本算法对r[s..t]进行一趟快速排序，执行本算法之后，若 s<i, \
则r[s..i-1]中记录的关键字均不大于r[i].key，若 t>i, 则\
r[i+1..t]中记录的关键字均不小于r[i].key, s<=i<=t}
BEGIN
<2>
    i := s; j := t; rp := r[s]; x := r[s].key;
<3>
    WHILE i < j DO
    BEGIN
<4>
        WHILE i < j AND r[j].key >= x DO
<5>
            j := j + 1;
<6>
        r[i] := r[j];    {找到r[j].key<x}
<7>
        WHILE i < j AND r[i].key <= x DO
<8>
            i := i + 1;
<9>
        r[j] := r[i];    {找到r[i].key>x}
    END
<10>
    r[i] := rp;
<11>
END {end of qkpass}
""")

def prepare(driver, configure):
    """ 外部调用统一接口 """
    return bubbleSortAlgorithm(driver, configure)

class bubbleSortAlgorithm(baseAlgorithm):
    """
    冒泡排序中的可见实体：
        r：初始的需要排序的一组数据。
           每一个元素的命名规则 r_i
        i: 当前排序头指针，名称 pointer_i
        j: 当前排序尾巴指针，名称 pointer_j
        k: 当前排序中点指针，名称 pointer_k
        rp: 中间变量，名称 rp
    """

    def __init__(self, driver, configure):

        self.__configure = configure
        self.__driver = driver

        # 从配置文件读取初始数据
        _pa = self.buildArrayList(
            "r_{0}",
            configure["r"]
            )
        self.__r = _pa.getIntList()
        self.__s = 0
        self.__t = len(self.__r) - 1

        _data = {
             "r":self.__r,
             "s":self.__s,
             "t":self.__t,
             "k":0
             }
        
        # 初始化驱动
        self.__driver.initializeDriver(
            __srcCodeMain__,
            _data,
            layout='none',
            )

        # 增加实体
        self.__driver.appendVisionNode(
            '__TOP__',
            'container',
            "_rpcontainer_",
            layout='queue',
            title="rp",
            tanchor='n',
            tyoffset=-5,
            left=100,
            top=10,
            width=60,
            height=60,
            )
        self.__driver.appendVisionNode(
            '__TOP__',
            'container',
            "nodecontainer",
            layout='queue',
            direction='right',
            canchor='n',
            cellwidth=40,
            cellheight=40,
            top=100,
            padx=5,            
            )        
        self.__driver.watchParameter(
            'nodecontainer',
            _pa
            )
        self.__driver.appendVisionNode(
            '_rpcontainer_',
            'node',
            'rp',
            shape='circle',
            width=40,
            height=40,
            anchor='center',
            options={'fill':'#BDB76B'},
            )
        self.__driver.appendVisionNode(
            '',            
            'pointer',
            "pointer_i",
            target='',
            anchor='n',
            xoffset=0,
            yoffset=-15,
            title='i',
            txoffset=10,
            options={'arrow':'last'},
            )
        self.__driver.appendVisionNode(
            '',            
            'pointer',
            "pointer_j",
            target='',
            anchor='s',
            xoffset=0,
            yoffset=15,
            title='j',
            txoffset=10,
            options={'arrow':'last'},
            )
        self.__driver.appendVisionNode(
            '',            
            'pointer',
            "pointer_k",
            target='',
            anchor='ne',
            xoffset=10,
            yoffset=-10,
            title='k',
            txoffset=10,
            tyoffset=-10,
            options={'arrow':'last'},
            )

        # 添加完成，启动重画
        self.__driver.enableVisionRefresh()

        # 指向第一条语句
        self.__driver.simulateStatementBefore(1, log=False)

    def run(self):

        # 模拟函数第一次调用
        self.__driver.simulateStatementBefore(1)

        # 调用算法主函数
        self.qksort(
            self.__r,
            self.__s,
            self.__t,
            )

    def qksort(self, r, s, t):

        k = 0
        # 模拟入栈
        self.__driver.simulateFunctionCall(
                __srcCodeMain__,
                locals()
                )

        self.__driver.simulateStatementBefore(2, locals())
        if s < t:
            self.__driver.simulateExecuteStatement()

            self.__driver.simulateStatementBefore(3, locals())
            self.__k = self.qkpass(r, s, t, k)
            k = self.__k
            self.__driver.simulateFunctionReturn()
            self.__driver.simulateAssignStatement("k", k)
            self.__driver.simulateAssignStatement("r", r.__str__())
            self.__driver.simulateVisionChange(
                "pointer_k",
                "target",
                "r_%d" % k
                )        

            self.__driver.simulateStatementBefore(4, locals())
            self.qksort(r, s, k - 1)
            self.__driver.simulateFunctionReturn()
            self.__driver.simulateAssignStatement("r", r.__str__())
            
            self.__driver.simulateStatementBefore(5, locals())
            self.qksort(r, k + 1, t)
            self.__driver.simulateFunctionReturn()
            self.__driver.simulateAssignStatement("r", r.__str__())
        
        # 函数返回语句
        self.__driver.simulateStatementBefore(6, locals())
        self.__driver.simulateAssignStatement("r", r.__str__())

    def qkpass(self, r, s, t, i):

        # 初始化局部变量
        j = 0
        rp = 0
        x = 0

        # 模拟入栈
        self.__driver.simulateFunctionCall(
                __srcCodeQkpass__,
                locals()
                )

        self.__driver.simulateStatementBefore(2, locals())
        i = s
        j = t
        rp = r[s]
        x = r[s]

        self.__driver.simulateAssignStatement("i", i)
        self.__driver.simulateAssignStatement("j", j)
        self.__driver.simulateAssignStatement("rp",rp)
        self.__driver.simulateAssignStatement("x", x)

        self.__driver.simulateVisionChange(
                "pointer_j",
                "target",
                "r_%d" % j
                )
        self.__driver.simulateVisionChange(
                "pointer_i",
                "target",
                "r_%d" % i
                )
        self.__driver.simulateVisionCopy(
                "r_%d" % i,
                "rp",                
                ('value',)
                )
        

        self.__driver.simulateStatementBefore(3, locals())
        while i < j:

            self.__driver.simulateStatementBefore(4, locals())
            while i < j and r[j] >= x:

                self.__driver.simulateStatementBefore(5, locals())
                j -= 1
                self.__driver.simulateAssignStatement("j", j)
                self.__driver.simulateVisionChange(
                    "pointer_j",
                    "target",
                    "r_%d" % j
                    )

            self.__driver.simulateStatementBefore(6, locals())            
            r[i] = r[j]            
            self.__driver.simulateAssignStatement("r", r.__str__())
            self.__driver.simulateVisionCopy(
                "r_%d" % j,
                "r_%d" % i,
                ('value',)
                )

            self.__driver.simulateStatementBefore(7, locals())
            while i < j and r[i] <= x:

                self.__driver.simulateStatementBefore(8, locals())
                i += 1
                self.__driver.simulateAssignStatement("i", i)
                self.__driver.simulateVisionChange(
                        "pointer_i",
                        "target",
                        "r_%d" % i
                        )

            self.__driver.simulateStatementBefore(9, locals())
            r[j] = r[i]
            self.__driver.simulateAssignStatement("r", r.__str__())
            self.__driver.simulateVisionCopy(
                "r_%d" % i,
                "r_%d" % j,
                ('value',)
                )


        self.__driver.simulateStatementBefore(10, locals())
        r[i] = rp
        self.__driver.simulateAssignStatement("r", r.__str__())
        self.__driver.simulateVisionCopy(
                "rp",
                "r_%d" % i,
                ('value',)
                )
        
        # 函数返回语句
        self.__driver.simulateStatementBefore(11, locals())
        return i


if __name__ == "__main__":
    pass

