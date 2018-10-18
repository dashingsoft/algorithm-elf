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

"""
递归演示程序：汉诺塔。
"""

from baseAlgorithm import baseAlgorithm

__srcCodeMain__ = ("hanoi",
"\
<1>\n\
procedure hanoi(n:integer, x,y,z:char);\n\
{将塔座x上编号从1至n，直径依小至大的n个圆盘移到\
塔座z上，y可用作辅助塔座}\n\
BEGIN\n\
<2>\n\
    IF n=1\n\
<3>\n\
        THEN move(x,1,z) {将编号为1的圆盘从x移到z}\n\
    ELSE BEGIN\n\
        {将x上编号从1至n-1的圆盘移动到y上，z为辅助塔座}\n\
<4>\n\
        hanoi(n-1,x,z,y); {将编号n-1的圆盘从x移到z}\n\
<5>\n\
        move(x,n,z);\n\
        {将y上编号从1至n-1的圆盘移动到z上，x为辅助塔座}\n\
<6>\n\
        hanoi(n-1,y,x,z);\n\
    END\n\
<7>\n\
END; {hanoi}")

def prepare(driver, configure):
    """ 外部调用统一接口 """
    return hanoiAlgorithm(driver, configure)

class hanoiAlgorithm(baseAlgorithm):

    def __init__(self, driver, configure):

        self.__configure = configure
        self.__driver = driver
        
        self.__numberOfPlate = self.buildInteger(
            configure["numberOfPlate"]
            )
        self.__nameOfSource = self.buildString(
            configure["nameOfSource"]
            )
        self.__nameOfMedia = self.buildString(
            configure["nameOfMedia"]
            )
        self.__nameOfTarget = self.buildString(
            configure["nameOfTarget"]
            )

        _data = {
             "n":self.__numberOfPlate,
             "x":self.__nameOfSource,
             "y":self.__nameOfMedia,
             "z":self.__nameOfTarget,
             }


        # 初始化驱动
        self.__driver.initializeDriver(
            __srcCodeMain__,
            _data,
            layout='queue',
            direction='right',
            cellwidth=180,
            cellheight=400,
            )

        # 添加可视实体
        # 添加柱子
        self.__driver.appendVisionNode(
            '__TOP__',
            'node',
            self.__nameOfSource,
            layout='queue',
            direction='up',
            cellheight=20,
            width=10,
            anchor='center',
            options={'fill':'black'},
            )
        self.__driver.appendVisionNode(
            '__TOP__',
            'node',
            self.__nameOfMedia,
            layout='queue',
            direction='up',
            cellheight=20,
            width=10,
            anchor='center',
            options={'fill':'black'},
            )
        self.__driver.appendVisionNode(
            '__TOP__',
            'node',
            self.__nameOfTarget,
            layout='queue',
            direction='up',
            cellheight=20,
            width=10,
            anchor='center',
            options={'fill':'black'},
            )

        # 添加盘子
        for i in range(self.__numberOfPlate):
            self.__driver.appendVisionNode(
                self.__nameOfSource,
                'node',
                'plate_%d' % (i + 1),
                title=str(i+1),
                padx=(i + 1) * 5,
                tanchor='center',
                options={'fill':'#1E90FF'},
                )

        # 添加完成，启动重画
        self.__driver.enableVisionRefresh()

        # 指向第一条语句 
        self.__driver.simulateStatementBefore(1, log=False)

    def run(self):

        # 模拟函数第一次调用
        self.__driver.simulateStatementBefore(1)
        
        self.hanoi(
            self.__numberOfPlate,
            self.__nameOfSource,
            self.__nameOfMedia,
            self.__nameOfTarget
            )

    def hanoi(self, n, x, y, z):
        """
        将 n 个盘子从 x 塔 移动到 z 塔.
        """
        # 模拟入栈
        self.__driver.simulateFunctionCall(
                __srcCodeMain__,
                locals()
            )

        # 模拟语句执行 if n=1
        self.__driver.simulateStatementBefore(
                2,
                locals()
            )
        if n == 1:
            self.__driver.simulateExecuteStatement()

            # 模拟语句执行 move
            self.__driver.simulateStatementBefore(
                3,
                locals()
                )
            self.move(x, 1, z)
            self.__driver.simulateExecuteStatement()

        else:
            # if n=1 的模拟结束语句
            self.__driver.simulateExecuteStatement()

            # 模拟函数调用
            self.__driver.simulateStatementBefore(
                4,
                locals()
                )
            self.hanoi(n - 1, x, z, y)
            self.__driver.simulateFunctionReturn()

            # 模拟语句执行 move
            self.__driver.simulateStatementBefore(
                5,
                locals()
                )
            self.move(x, n, z)
            self.__driver.simulateExecuteStatement()

            # 模拟函数调用
            self.__driver.simulateStatementBefore(
                6,
                locals()
                )
            self.hanoi(n - 1, y, x, z)
            self.__driver.simulateFunctionReturn()

        # 模拟函数返回
        self.__driver.simulateStatementBefore(
                7,
                locals()
            )

    def move(self, x, n, y):
        """ 移动第 n 个盘子到 x 到 y """
        # print x, " ", n, " ", y
        _name = "plate_%d" % (self.__numberOfPlate - n + 1)
        self.__driver.simulateVisionMove(_name, x, y)
