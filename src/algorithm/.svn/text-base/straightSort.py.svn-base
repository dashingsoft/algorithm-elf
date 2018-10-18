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
# @文件：straightSort.py
#
# @作者：赵俊德(jondy.zhao@gmail.com)
#
# @创建日期: 2009/07/09
#
# @文件说明
#
# 直接插入排序算法的实现。
#

from dsException import dsError
from baseAlgorithm import baseAlgorithm

__srcCodeMain__ = ( "straisort",
"""
<1>
procedure straisort(var r:listtype);
{对r[1..n]进行直接插入排序，执行本算法后，r[1..]中的记录\
按关键字非递减有序排列}
BEGIN
<2>
    FOR i := 2 TO n DO
<3>
        straipass(r, i)

<4>
END {end of straisort}
""")

__srcCodeStraipass__ = ( "straipass",
"""
<1>
procedure straipass(var r:listtype; i:integer);
{已知r[1..i-1]中的记录按关键字非递减有序排列，本算法插入\
r[i]，使得r[1..i]中记录按关键字非递减有序排列}
BEGIN
<2>
    r[0] := r[i]; j := i - 1; x := r[i].key;
<3>
    WHILE x < r[j].key DO
    BEGIN
<4>
        r[j+1] := r[j];
<5>
        j := j - 1;
    END
<6>
    r[j + 1] := r[0]
<7>
END {end of straisort}
""")

def prepare(driver, configure):
    """ 外部调用统一接口 """
    return straightSortAlgorithm(driver, configure)

class straightSortAlgorithm(baseAlgorithm):
    """
    直接插入排序中的可见实体：
        r：初始的需要排序的一组数据。
           每一个元素的命名规则 r_i
        i: 当前排序指针，名称 pointer_i
        j: 搜寻指针，名称 pointer_j
    """

    def __init__(self, driver, configure):

        self.__configure = configure
        self.__driver = driver

        # 从配置文件读取初始数据
        _pa = self.buildArrayList(
            "r_{0}",
            u'0,' + configure["r"]
            )
        self.__i = 0
        self.__r = _pa.getIntList()
        
        # 设定堆栈数据
        _data = {
             "r":self.__r,
             "i":self.__i,
             }

        # 初始化驱动
        self.__driver.initializeDriver(
            __srcCodeMain__,
            _data,
            layout='queue',
            direction='right',
            canchor='center',
            cellwidth=40,
            cellheight=40,
            padx=5,
            )

        # 增加实体
        self.__driver.watchParameter(
            '__TOP__',
            _pa
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
        # 修改 r_0 的属性，这是监控哨
        self.__driver.simulateVisionUpdate(
            "r_0",
            shape='circle',
            options={'fill':'#BDB76B'},
            )            

        # 添加完成，启动重画
        self.__driver.enableVisionRefresh()

        # 指向第一条语句
        self.__driver.simulateStatementBefore(1, log=False)

    def run(self):

        # 模拟函数第一次调用
        self.__driver.simulateStatementBefore(1)

        # 调用算法主函数
        self.straightSort(
            self.__r,
            )

    def straightSort(self, r):

        # 模拟入栈
        self.__driver.simulateFunctionCall(
                __srcCodeMain__,
                locals()
                )

        self.__driver.simulateStatementBefore(2, locals())
        for i in range(2, len(r)):
            self.__driver.simulateAssignStatement("i", i)
            self.__driver.simulateVisionChange(
                "pointer_i",
                "target",
                "r_%d" % i
                )

            self.__driver.simulateStatementBefore(3, locals())
            self.straightPass(r, i)
            self.__driver.simulateFunctionReturn()

        # 函数返回语句
        self.__driver.simulateStatementBefore(4, locals())

    def straightPass(self, r, i):
        # 初始化局部变量
        x = 0
        j = 0
        # 模拟入栈
        self.__driver.simulateFunctionCall(
                __srcCodeStraipass__,
                locals()
                )

        self.__driver.simulateStatementBefore(2, locals())
        r[0] = r[i]
        j = i - 1
        x = r[i]
        self.__driver.simulateAssignStatement("r", r.__str__())
        self.__driver.simulateAssignStatement("j", j)
        self.__driver.simulateAssignStatement("x", x)
        self.__driver.simulateVisionChange(
                "pointer_j",
                "target",
                "r_%d" % j
                )
        self.__driver.simulateVisionCopy(
                        "r_%d" % i,
                        "r_0",
                        ("value",)
                        )

        self.__driver.simulateStatementBefore(3, locals())
        while j > 0 and x < r[j]:

            self.__driver.simulateStatementBefore(4, locals())
            r[j+1] = r[j]
            self.__driver.simulateAssignStatement("r", r.__str__())
            self.__driver.simulateVisionCopy(
                        "r_%d" % j,
                        "r_%d" % (j + 1),
                        ('value',)
                        )

            self.__driver.simulateStatementBefore(5, locals())
            j = j - 1
            self.__driver.simulateAssignStatement("j", j)
            self.__driver.simulateVisionChange(
                "pointer_j",
                "target",
                "r_%d" % j
                )

        self.__driver.simulateStatementBefore(6, locals())
        r[j + 1] = r[0]
        self.__driver.simulateAssignStatement("r", r.__str__())
        self.__driver.simulateVisionCopy(
                        "r_0",
                        "r_%d" % (j + 1),
                        ('value',)
                        )
        # 函数返回语句
        self.__driver.simulateStatementBefore(7, locals())


if __name__ == "__main__":
    pass

