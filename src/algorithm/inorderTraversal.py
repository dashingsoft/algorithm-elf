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
中序遍历线索二叉树算法。
"""

from dsException import dsError
from baseAlgorithm import baseAlgorithm

__srcCodeMain__ = ( "crt_inthlinked",
"""
<1>
procedure crt_inthlinked(var thrt:thlinktp; bt:thlinktp);
{已知bt指向二叉树的根结点，中序遍历生成中序线索二叉树链表，\
thrt为指向头结点的指针}
BEGIN
<2>
    new(thrt); thrt.ltag := 0; thrt.rtag := 0; {建立头结点}
<3>
    thrt.rchild := thrt;
<4>
    IF bt = NIL THEN
<5>
        thrt.lchild := thrt;
    ELSE BEGIN
<6>
        thrt.lchild := bt;
<7>
        pre := thrt;
<8>
        inthread(bt); {中序遍历线索化}
<9>
        pre.rchild := thrt; pre.rtag := 1;
<10>
        pre.rchild := pre;  thrt.rtag := 1;
    END; {if}
<11>
ENDP; {crt_inthlinked}
""")

__srcCodeInthread__ = ("inthread",
"""
<1>
procedure intherad(p:thlinktp);
{中序线索化以p为根指针的二叉树}
BEGIN
<2>
    IF p <> NIL THEN
    BEGIN
<3>
        inthread(p.lchild); {左子树线索化}
<4>
        IF p.lchild = NIL THEN
<5>
            p.ltag := 1, p.lchild := pre; {建立前驱线索}
<6>
        IF pre.rchild = NIL THEN
<7>
            pre.rtag := 1; pre.rchild := p; {建立后继线索}
<8>
        pre := p;  {保持pre指向p的前驱}
<9>
        inthread(p.rchild); {右子树线索化}
    END; {if}
<10>
ENDP; {inthread}
""")

def prepare(driver, configure):
    """ 外部调用统一接口 """
    return inorderTraversalAlgorithm(driver, configure)

class inorderTraversalAlgorithm(baseAlgorithm):
    """
    可视实体的命名规则：
        头指针， 名称为 thrt
        全局变量 pre，名称为 pre
        全局变量关联指针，preRelation

        树结点，就是结点的名称。
        结点左线索，结点名称_lchild
        结点右线索，结点名称_rchild
    """

    def __init__(self, driver, configure):

        self.__configure = configure
        self.__driver = driver

        # 初始化辅助参数
        self.__thrt = self.buildTreeList(
            "thrt (ltag=0, rtag=0)"
            )
        self.__thrt.setValue("0,0")
        self.__pre = None

        # 从配置文件中读取初始化参数
        self.__bt = self.buildTreeList(configure["bt"])        

        # 设定堆栈数据
        _data = {
            "thrt": self.__thrt,
            "bt": self.__bt
            }

        # 初始化驱动
        self.__driver.initializeDriver(
            __srcCodeMain__,
            _data,
            layout='none',
            )

        # 添加可视实体
        self.__driver.appendVisionNode(
            '',
            'relation',
            "thrt_lchild",
            source="thrt",
            rsanchor='w',
            target="",
            options={'dash':(3,5),'arrow':'last'},
            )
        self.__driver.appendVisionNode(
            '',
            'relation',
            "thrt_rchild",
            source="thrt",
            rsanchor='e',
            target="",
            options={'dash':(3,5),'arrow':'last'},
            )
        self.__driver.appendVisionNode(
            '',
            'pointer',
            "prepointer",
            title="pre",
            tanchor='w',
            tyoffset=-10,
            txoffset=-10,
            target="",
            anchor='w',
            xoffset=-20,
            yoffset=0,
            options={'arrow':'last','fill':'#FF00FF'},
            )
        self.__driver.appendVisionNode(
            '__TOP__',
            'container',
            '__HEADER__',
            layout='none',
            height=80
            )
        self.__driver.appendVisionNode(
            '__TOP__',
            'container',
            '__TREE__',
            layout='none',
            top=100,
            padx=2
            )

        # 添加线索和树
        self.__initTree(self.__bt)
        self.__driver.watchParameter(
            '__TREE__',
            self.__bt,
            vdirection='horizontal'
            )

        # 添加完成，启动重画
        self.__driver.enableVisionRefresh()

        # 指向第一条语句
        self.__driver.simulateStatementBefore(1, log=False)

    def run(self):

        # 模拟函数第一次调用
        self.__driver.simulateStatementBefore(1)

        self.crt_inthlinked(
            self.__thrt,
            self.__bt,
            )

    def crt_inthlinked(self, thrt, bt):
        """ 建立中序线索化二叉树 """

        # 模拟入栈
        self.__driver.simulateFunctionCall(
                __srcCodeMain__,
                locals()
                )

        self.__driver.simulateStatementBefore(2, locals())
        # 增加可视实体 thrt
        self.__driver.simulateVisionInsert(
            "__HEADER__",
            'node',
            "thrt",
            shape='rectangle',
            anchor='center',
            options={'fill':'#BDB76B'},
            pady=2,
            width=60,
            height=40,
            value='0,0',
            vdirection='horizontal',
            title="thrt",
            tanchor='n',
            tyoffset=-10
            )
        self.__driver.simulateExecuteStatement()

        thrt.setProperty("ltag", 0)
        thrt.setProperty("rtag", 0)
        self.__driver.simulateVisionChange(
            "thrt",
            'value',
            '0,0'
            )
        self.__driver.simulateStatementBefore(3, locals())

        # thrt.lchild = None
        thrt.append(None)
        # thrt.rchild = thrt
        thrt.append(thrt)

        self.__driver.simulateStatementBefore(4, locals())
        if bt is None:
            self.__driver.simulateExecuteStatement()

            self.__driver.simulateStatementBefore(5, locals())
            # thrt.lchild = thrt
            self.__driver.simulateVisionChange(
                "thrt_lchild",
                'target',
                "thrt"
                )
            # thrt.ltag = 1
            thrt.setProperty('ltag', 1)
            self.__driver.simulateAssignStatement(
                'thrt',
                thrt.__str__()
                )
            self.__driver.simulateVisionChange(
                "thrt",
                'value',
                '1,%s' % self.__thrt.getProperty('rtag', 0)
                )

        else:
            self.__driver.simulateExecuteStatement()

            self.__driver.simulateStatementBefore(6, locals())
            # thrt.lchild = bt
            self.__driver.simulateVisionChange(
                "thrt_lchild",
                "target",
                bt.getName()
                )
            # thrt.ltag = 1
            thrt.setProperty('ltag', 1)
            self.__driver.simulateVisionChange(
                "thrt",
                'value',
                '1,%s' % self.__thrt.getProperty('rtag', 0)
                )
            
            self.__driver.simulateStatementBefore(7, locals())
            self.__pre = thrt
            self.__driver.simulateVisionChange(
                "prepointer",
                'target',
                "thrt"
                )

            self.__driver.simulateStatementBefore(8, locals())
            self.inthread(bt)
            self.__driver.simulateFunctionReturn()

            self.__driver.simulateStatementBefore(9, locals())
            # pre.rchild=thrt
            self.__driver.simulateVisionChange(
                "%s_rchild" % self.__pre.getName(),
                'target',
                "thrt"
                )

            self.__pre.setProperty('rtag', 1)
            self.__driver.simulateVisionChange(
                self.__pre.getName(),
                'value',
                '%s,1' % self.__pre.getProperty('ltag', 0)
                )

            self.__driver.simulateStatementBefore(10, locals())
            # thrt.rchild = pre
            self.__driver.simulateVisionChange(
                "thrt_rchild",
                'target',
                self.__pre.getName()
                )

            # thrt.rtag = 1
            self.__driver.simulateVisionChange(
                "thrt",
                'value',
                '%s,1' % self.__thrt.getProperty('ltag', 0)
                )
            
        # 函数返回语句
        self.__driver.simulateStatementBefore(11, locals())

    def inthread(self, p):

        # 模拟入栈
        self.__driver.simulateFunctionCall(
                __srcCodeInthread__,
                locals()
                )

        self.__driver.simulateStatementBefore(2, locals())
        if p is not None:
            self.__driver.simulateExecuteStatement()
            _children = p.getChildren()
            if len(_children) == 0:
                _lchild = None
            else:
                _lchild = _children[0]
            if len(_children) < 2:
                _rchild = None
            else:
                _rchild = _children[1]
            # 选中 p
            self.__driver.simulateVisionChange(
                p.getName(),
                'options',
                {'fill':'#9932CC'}
                )

            self.__driver.simulateStatementBefore(3, locals())
            self.inthread(_lchild)
            self.__driver.simulateFunctionReturn()

            self.__driver.simulateStatementBefore(4, locals())
            if _lchild is None:
                self.__driver.simulateExecuteStatement()

                self.__driver.simulateStatementBefore(5, locals())
                p.setProperty('ltag', 1)
                self.__driver.simulateVisionChange(
                    p.getName(),
                    'value',
                    "1,%s" % p.getProperty('rtag', 0)
                    )

                # p.lchild = self.__pre
                self.__driver.simulateVisionChange(
                    "%s_lchild" % p.getName(),
                    'target',
                    self.__pre.getName()
                    )

            self.__driver.simulateStatementBefore(6, locals())
            try:
                _prerchild = self.__pre.getChildren()[1]
            except IndexError:
                _prerchild = None
            if _prerchild is None:
                self.__driver.simulateExecuteStatement()

                self.__driver.simulateStatementBefore(7, locals())
                self.__pre.setProperty('rtag', 1)
                self.__driver.simulateVisionChange(
                    self.__pre.getName(),
                    'value',
                    "%s,1" % self.__pre.getProperty('ltag', 0)
                    )
                
                # self.__pre.rchild = p
                self.__driver.simulateVisionChange(
                    "%s_rchild" % self.__pre.getName(),
                    'target',
                    p.getName()
                    )

            self.__driver.simulateStatementBefore(8, locals())
            self.__pre = p
            self.__driver.simulateVisionChange(
                "prepointer",
                'target',
                p.getName()
                )

            self.__driver.simulateStatementBefore(9, locals())
            self.inthread(_rchild)
            self.__driver.simulateFunctionReturn()

            self.__driver.simulateVisionChange(
                p.getName(),
                'options',
                {'fill':'#1E90FF'}
                )


        # 函数返回语句
        self.__driver.simulateStatementBefore(10, locals())

    def __initTree(self, treenode):
        """
        生成线索可视实体，遍历 List 格式的树，如果结点没有
        左孩子，那么生成左线索；没有右孩子，生成右线索。
        """
        if treenode is None:
            return

        _children = treenode.getChildren()
        try:
            _leftchild = _children[0]
            _ltag = 1
        except IndexError:
            _leftchild = None
            _ltag = 0
        try:
            _rightchild = _children[1]
            _rtag = 1
        except IndexError:
            _rightchild = None
            _rtag = 0

        nodename = treenode.getName()
        if _leftchild is None:
            _ltag = 0
            self.__driver.appendVisionNode(
                '',
                'relation',
                "%s_lchild" % nodename,
                source=nodename,
                rsanchor='w',
                target='',
                options={'dash':(3,8),'arrow':'last'},
                )
        if _rightchild is None:
            _rtag = 0
            self.__driver.appendVisionNode(
                '',
                'relation',
                "%s_rchild" % nodename,
                source=nodename,
                rsanchor='e',
                target='',
                options={'dash':(3,8),'arrow':'last'},
                )

        treenode.setValue('%s,%s' % (_ltag, _rtag))
        treenode.setProperty('ltag', _ltag)
        treenode.setProperty('rtag', _rtag)

        # 递归处理
        self.__initTree(_leftchild)
        self.__initTree(_rightchild)
