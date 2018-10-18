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

from dsException import dsError
from baseAlgorithm import baseAlgorithm

__srcCodeMain__ = ( "inOrder",
"""
<1>
procedure inOrder(bt:bitreptr);
{先序遍历根结点为 bt 的二叉树}
BEGIN
<2>
    IF bt <> NIL THEN
    BEGIN
<3>
        inOrder(bt.lchild);
<4>
        visit(bt);    {访问根结点}
<5>
        inOrder(bt.rchild);
    END {end of if}

<6>
END {end of inOrder}
""")

def prepare(driver, configure):
    """ 外部调用统一接口 """
    return inOrderAlgorithm(driver, configure)

class inOrderAlgorithm(baseAlgorithm):

    def __init__(self, driver, configure):

        self.__configure = configure
        self.__driver = driver

        # 所有主函数局部变量都在这里定义，并从配置文件
        # 读取初始值
        self.__bt = self.buildTreeList(configure["bt"])

        _data = {
             "bt":self.__bt
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
            'visited',
            layout='queue',
            direction='right',
            canchor='s',
            anchor='sw',
            height=100,
            padx=20,
            pady=10,
            cellwidth=30,
            cellheight=40,
            )        
        self.__driver.watchParameter(
            '__TOP__',
            self.__bt
            )

        # 添加完成，启动重画
        self.__driver.enableVisionRefresh()

        # 指向第一条语句
        self.__driver.simulateStatementBefore(1, log=False)

    def run(self):

        # 模拟函数第一次调用
        self.__driver.simulateStatementBefore(1)

        # 调用算法主函数
        self.postOrder(
            self.__bt,
            )

    def postOrder(self, bt):

        # 模拟入栈
        self.__driver.simulateFunctionCall(
                __srcCodeMain__,
                locals()
                )

        self.__driver.simulateStatementBefore(2, locals())
        if bt is not None:
            self.__driver.simulateExecuteStatement()

            _children = bt.getChildren()
            try:
                _lchild = _children[0]
            except IndexError:
                _lchild = None
            try:
                _rchild = _children[1]
            except IndexError:
                _rchild = None
            
            self.__driver.simulateStatementBefore(3, locals())            
            self.postOrder(_lchild)    
            self.__driver.simulateFunctionReturn()

            self.__driver.simulateStatementBefore(4, locals())
            self.__visit(bt)
            self.__driver.simulateExecuteStatement()

            self.__driver.simulateStatementBefore(5, locals())
            self.postOrder(_rchild)
            self.__driver.simulateFunctionReturn()

        # 函数返回语句
        self.__driver.simulateStatementBefore(6, locals())

    def __visit(self, node):
        # 高亮显示 node
        self.__driver.simulateVisionUpdate(
                node.getName(),
                options={'fill':'#9932CC'},
                )
        self.__driver.simulateVisionInsert(
            'visited',
            'node',
            'v_%s' % node.getName(),
            shape='circle',
            title=node.getName(),
            options={'fill':'#9932CC'},
            padx=5,
            pady=5,
            )

if __name__ == "__main__":
    pass

