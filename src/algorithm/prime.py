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

from baseAlgorithm import baseAlgorithm

__srcCodeMain__ = ( "prime",
"""
<1>
procedure minispantree_prime(gn:adjmatrix; u0:vtxptr);
{从 u0 出发构造网 gn 的最小生成树，按普利姆算法输出生成树上\
的各条边}
BEGIN
<2>
    FOR v := 1 TO vtxnum DO
    BEGIN
<3>
        IF v <> u0 THEN
           WITH closedge[v] DO
           BEGIN
<4>
               vex := u0;
<5>
               lowcost := gn[u0, v]
           END
    END {end of for}

<6>
    closedge[u0].lowcost := 0; {辅助数组初始化}

<7>
    FOR i := 1 to vtxnum - 1 DO
    BEGIN
<8>
        k := minimum(closedge)
<9>
        write(closedge[k].vex, k); {输出生成树各边}
<10>
        closedge[k].lowcost :=0; {顶点 k 并入 U 集}
<11>
        FOR v := 1 TO vtxnum DO
<12>
            IF gn[k, v] < closedge[v].lowcost THEN
            BEGIN
<13>
                closedge[v].lowcost := gn[k,v ];
<14>
                closedge[v].vex := k;
            END {end of if}
    END {end of for}
<15>
END {end of minispantree_prime}
""")

def prepare(driver, configure):
    """ 外部调用统一接口 """
    return primeAlgorithm(driver, configure)

class primeAlgorithm(baseAlgorithm):

    def __init__(self, driver, configure):

        self.__configure = configure
        self.__driver = driver

        # 读取配置文件，定义主函数传入参数
        self.__gn = self.buildGraphList(configure["gn"])
        self.__u0 = self.buildString(configure["u0"])

        self.__nodenames = self.__gn.getNodes()
        self.__vtxnum = len(self.__nodenames)

        # 设定堆栈数据
        _data = {
            "u0":self.__u0,
            "v":None,
            "i":None,
            "k":None,
            "closedge":None
            }

        # 初始化驱动
        self.__driver.initializeDriver(
            __srcCodeMain__,
            _data,
            layout='none',
            )

        # 设定可视实体
        self.__driver.appendVisionNode(
            '__TOP__',
            'container',
            'graph',
            layout='star',
            top=100,            
            padx=10,
            pady=10,
            )
        self.__driver.appendVisionNode(
            '__TOP__',
            'container',
            'closedge',
            layout='queue',
            direction='right',
            canchor='center',
            cellwidth=60,
            cellheight=60,
            title="closedge",
            tanchor='w',
            txoffset=-60,
            left=40,
            anchor='nw',
            height=100,
            padx=10,
            pady=10,
            )
        self.__driver.appendVisionNode(
            'closedge',
            'node',
            'closedge_0',
            shape='rectangle',
            value="Vew,Lowcost",
            vdirection='vertical',
            title='legend',
            tyoffset=-10,
            tanchor='n',
            options={'fill':'#BDB76B'},
            padx=4,
            )

        for i in range(self.__vtxnum):
            self.__driver.appendVisionNode(
                'closedge',
                'node',
                "closedge_%s" % self.__nodenames[i],
                title=self.__nodenames[i],
                tanchor='n',
                tyoffset=-10,
                shape='rectangle',
                value="None,None",
                vdirection='vertical',
                options={'fill':'#1E90FF'},
                padx=2
                )

        # 将边中每一个 weight，变成可见实体的 title
        _edges = self.__gn.getEdges()
        for eg in _edges:
            self.__gn.setEdgeProperty(
                eg[0],
                eg[1],
                'title',
                self.__gn.getEdgeProperty(
                    eg[0],
                    eg[1],
                    'weight',
                    '0'
                    )
                )
        self.__driver.watchParameter(
            'graph',
            self.__gn
            )

        # 添加完成，启动重画
        self.__driver.enableVisionRefresh()

        # 指向第一条语句
        self.__driver.simulateStatementBefore(1, log=False)

    def run(self):

        # 模拟函数第一次调用
        self.__driver.simulateStatementBefore(1)

        # 调用算法主函数
        self.prime(
            self.__gn,
            self.__u0
            )

    def prime(self, _gn, u0):

        # 初始化局部变量
        v = None
        closedge = {}
        i = None
        k = None

        # 模拟入栈
        self.__driver.simulateFunctionCall(
                __srcCodeMain__,
                locals()
                )

        # 选中 u0
        self.__driver.simulateVisionChange(
                u0,
                'options',
                {'fill':'#9932CC'}
                )

        # 循环初始化
        self.__driver.simulateStatementBefore(2, locals())
        for v in range(self.__vtxnum):
            _nodename = self.__nodenames[v]
            self.__driver.simulateAssignStatement(
                "v",
                _nodename
                )

            self.__driver.simulateStatementBefore(3, locals())
            if not _nodename == u0:
                self.__driver.simulateExecuteStatement()

                self.__driver.simulateStatementBefore(4, locals())
                _weight = self.__getWeight(_gn, u0, _nodename)
                closedge[_nodename] ={
                    "vex":u0,
                    "lowcost":_weight
                    }
                self.__driver.simulateAssignStatement(
                    "closedge",
                    closedge.__str__()
                    )
                self.__driver.simulateVisionChange(
                    "closedge_%s" % _nodename,
                    "value",
                    "%s,None" %u0
                    )
                self.__driver.simulateStatementBefore(5, locals())
                self.__driver.simulateAssignStatement(
                    "closedge",
                    closedge.__str__()
                    )
                self.__driver.simulateVisionChange(
                    "closedge_%s" % _nodename,
                    "value",
                    "%s,%s" % (u0, _weight)
                    )
            else:
                self.__driver.simulateStatementBefore(6, locals())
                closedge[_nodename] = {"vex":u0, "lowcost":0}
                self.__driver.simulateAssignStatement(
                    "closedge",
                    closedge.__str__()
                    )
                self.__driver.simulateVisionChange(
                    "closedge_%s" % u0,
                    "value",
                    "%s,None" % u0
                    )

        self.__driver.simulateStatementBefore(7, locals())
        for i in range(self.__vtxnum - 1):
            self.__driver.simulateAssignStatement(
                "i",
                self.__nodenames[i]
                )

            self.__driver.simulateStatementBefore(8, locals())
            k = self.__minimum(closedge)
            self.__driver.simulateAssignStatement("k", k)
            # 选中 k
            self.__driver.simulateVisionChange(
                k,
                "options",
                {'fill':'#9932CC'}
                )

            self.__driver.simulateStatementBefore(9, locals())
            self.__write(closedge[k]["vex"], k)
            self.__driver.simulateExecuteStatement()

            self.__driver.simulateStatementBefore(10, locals())
            closedge[k]["lowcost"] = 0
            self.__driver.simulateAssignStatement(
                    "closedge",
                    closedge.__str__()
                    )
            self.__driver.simulateVisionChange(
                    "closedge_%s" % k,
                    "value",
                    "%s,%d" % (closedge[k]["vex"], 0)
                    )

            self.__driver.simulateStatementBefore(11, locals())
            for v in range(self.__vtxnum):
                _nodename = self.__nodenames[v]
                self.__driver.simulateAssignStatement(
                    "v",
                    _nodename
                    )
                _weight = self.__getWeight(_gn, k, _nodename)
                self.__nodelowcost = closedge[_nodename]["lowcost"]

                self.__driver.simulateStatementBefore(12, locals())
                if ((_weight is not None) and
                     (self.__nodelowcost is None
                      or _weight < self.__nodelowcost)):
                     self.__driver.simulateExecuteStatement()

                     self.__driver.simulateStatementBefore(13, locals())
                     closedge[_nodename]["lowcost"] = _weight
                     self.__driver.simulateAssignStatement(
                         "closedge",
                         closedge.__str__()
                         )
                     self.__driver.simulateVisionChange(
                         "closedge_%s" % _nodename,
                         "value",
                         "%s,%d" % (closedge[_nodename]["vex"], _weight)
                         )
                     self.__driver.simulateStatementBefore(14, locals())
                     closedge[_nodename]["vex"] = k
                     self.__driver.simulateAssignStatement(
                         "closedge",
                         closedge.__str__()
                         )
                     self.__driver.simulateVisionChange(
                         "closedge_%s" % _nodename,
                         "value",
                         "%s,%d" % (k, _weight)
                         )

        # 函数返回语句
        self.__driver.simulateStatementBefore(15, locals())

    def __getWeight(self, gn, u, v):
        """ 得到两个结点的权值，如果不存在两个结点的连线，返回 None """
        try:
            _value = gn.getEdgeProperty(u, v, 'weight', None)
        except:
            return None

        if _value is not None:
            return int(_value)

        return None

    def __minimum(self, closedge):
        """ 返回最小边"""
        _key = None
        _value = None
        for k, p in closedge.iteritems():
            if not (p["lowcost"] is None or p["lowcost"] == 0):
                if _value is None:
                    _value = p["lowcost"]
                    _key = k
                elif p["lowcost"] < _value:
                    _value = p["lowcost"]
                    _key = k
        return _key

    def __write(self, u, v):
        self.__driver.simulateOutput("(%s,%s)" % (u, v))
        # 显示选中的边
        _name = self.__gn.getEdgeName(u, v)
        self.__driver.simulateVisionChange(
                _name,
                'options',
                {'width':2}
                )

if __name__ == "__main__":
    pass
