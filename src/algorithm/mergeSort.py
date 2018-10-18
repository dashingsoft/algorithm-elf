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
归并排序演示程序。
"""

from baseAlgorithm import baseAlgorithm

__srcCodeMain__ = ("mergeSort",
"""
<1>
procedure mergeSort(var r, r1:listtype; s,t:integer);
{本算法对r[s..t]中的记录进行2-路归并排序，使r[s..t]中记录\
按照关键字有序}
BEGIN
<2>
    IF s=t
<3>
        THEN r1[s] := r[s];
    ELSE BEGIN
<4>
        mergeSort(r, r2, s, ( s + t ) / 2 );
<5>
        mergeSort(r, r2, ( s + t ) / 2 + 1, t );
<6>
        merge(r2, s, ( s + t ) / 2, t, r1);
    END
<7>
END; {mergeSort}
""")

__srcCodeMerge__ = ("merge",
"""
<1>
procedure merge(rs:listtype; s,m,n:integer; var rn:listtype);
{已知r[s..m]和r[m+1..n]分别按照关键字有序，本算法将他们归并\
成为一个有序序列并存放在rs[s..n]中}
BEGIN
<2>
    i := s; j := m + 1; k := s - 1;
<3>
    WHILE ( i <= m ) AND ( j <= n ) DO
    BEGIN
<4>
        k := k + 1;
<5>
        IF rs[i].key <= rs[j].key THEN
        BEGIN
<6>
            rn[k] := rs[i];
<7>
            i := i + 1;
        ELSE
<8>
            rn[k] := rs[j];
<9>
            j := j + 1;
        END; {if}
<10>
        IF i <= m THEN
<11>
            rn[k+1..n] := rs[i..m];
        {将r[s..m]或者r[m+1..n]中的剩余记录复制到r2中}
<12>
        IF j <= n THEN
<13>
            rn[k+1..n] := rs[j..n];
    END; {while}
<14>
END; {merge}
""")

def prepare(driver, configure):
    """ 外部调用统一接口 """
    return mergeSortAlgorithm(driver, configure)

class mergeSortAlgorithm(baseAlgorithm):

    def __init__(self, driver, configure):

        self.__configure = configure
        self.__driver = driver
        self.__level = 0

        # 从配置文件读取初始数据
        self._ra_ = self.buildArrayList(
            'node{0}',
            configure['r']
            )
        self._r_ = self._ra_.getIntList()
        self._s_ = 0
        self._t_ = len(self._r_) - 1
        self._r1_ = range(len(self._r_))
        self._r2_ = range(len(self._r_))

        _data = {
             "r":self._r_,
             "r1":self._r1_,
             "s":self._s_,
             "t":self._t_,
             "r2":self._r2_,
             }

        # 初始化驱动
        self.__driver.initializeDriver(
            __srcCodeMain__,
            _data,
            layout='queue',
            direction='down',
            canchor='w',
            left=40,
            padx=10,
            pady=10,
            cellwidth=400,
            cellheight=80,
            )

        # 增加实体
        self.__driver.appendVisionNode(
            '__TOP__',
            'container',
            'r',
            anchor='nw',
            layout='queue',
            direction='right',
            cellwidth=40,
            cellheight=40,
            title='r',
            tanchor='w',
            txoffset=-20,
            )
        self.__driver.appendVisionNode(
            '__TOP__',
            'container',
            'r1',
            anchor='nw',
            layout='queue',
            direction='right',
            cellwidth=40,
            cellheight=40,
            title='r1',
            tanchor='w',
            txoffset=-20,
            )
        self.__driver.watchParameter(
            'r',
            self._ra_,
            )
        for i in range(len(self._r1_)):
            self.__driver.appendVisionNode(
                'r1',
                'node',
                'r%dnode%d' % (self.__level, i),
                shape='diamond',
                value=str(self._r1_[i]),
                vanchor='center',
                options={'width':1,'outline':'black','fill':'#1E90FF'},
                )

        # 添加完成，启动重画
        self.__driver.enableVisionRefresh()

        # 指向第一条语句
        self.__driver.simulateStatementBefore(1, log=False)

    def run(self):

        # 模拟函数第一次调用
        self.__driver.simulateStatementBefore(1)

        self.mergeSoft(
            self._r_,
            self._r1_,
            self._s_,
            self._t_
            )

    def mergeSoft(self, r, r1, s, t):
        """ 归并排序 """
        # 初始化变量，增加实体
        self.__level += 1
        r2 = self.__addVisionNode(r, s, t)

        # 模拟入栈
        self.__driver.simulateFunctionCall(
                __srcCodeMain__,
                locals()
                )

        # 模拟语句执行  if s = t
        self.__driver.simulateStatementBefore(2,locals())

        if s == t:
            self.__driver.simulateExecuteStatement()

            # 模拟语句执行 r1[s] := r[s]
            self.__driver.simulateStatementBefore(3,locals())
            r1[s] = r[s]
            self.__driver.simulateAssignStatement(
                ("r1", s),
                r1.__str__()
                )
            
            # 增加模拟动作，修改可视视图
            self.__driver.simulateVisionCopy(
                "node%d" % s,
                "r%dnode%d" % (self.__level - 1, s),
                ('value',)
                )

        else:
            # if s=t 的模拟结束语句
            self.__driver.simulateExecuteStatement()

            # 模拟函数调用
            self.__driver.simulateStatementBefore(4,locals())

            self.mergeSoft(
                    r,
                    r2,
                    s,
                    (s + t) / 2
                    )
            self.__driver.simulateFunctionReturn()
            self.__driver.simulateAssignStatement(
                "r2",
                r2.__str__()
                )

            # 模拟函数调用
            self.__driver.simulateStatementBefore(5,locals())
            self.mergeSoft(
                    r,
                    r2,
                    (s + t) / 2 + 1,
                    t
                    )
            self.__driver.simulateFunctionReturn()
            self.__driver.simulateAssignStatement(
                "r2",
                r2.__str__()
                )

            # 模拟语句执行函数调用
            self.__driver.simulateStatementBefore(6,locals())
            self.merge(
                    r2,
                    s,
                    ( s + t ) / 2,
                    t,
                    r1
                    )
            self.__driver.simulateFunctionReturn()
            self.__driver.simulateAssignStatement(
                "r1",
                r1.__str__()
                )

        # 移除实体 "r%dnode%d" % (self.__level, i),
        self.__driver.simulateVisionRemove(
                "r2_%d" % self.__level
                )
        # 函数返回语句
        self.__level -= 1
        self.__driver.simulateStatementBefore(7, locals())

    def merge(self, rs, s, m, n, rn):
        """  归并列表 """
        i = j = k = 0

        # 模拟入栈
        self.__driver.simulateFunctionCall(
                __srcCodeMerge__,
                locals()
                )

        # 模拟语句执行 i := s; j := m + 1; k := s - 1
        self.__driver.simulateStatementBefore(2, locals())
        i = s
        self.__driver.simulateAssignStatement("i", i)

        j = m + 1
        self.__driver.simulateAssignStatement("j", j)

        k = s - 1
        self.__driver.simulateAssignStatement("k", k)

        self.__driver.simulateStatementBefore(3, locals())
        while i <= m and j <= n:
            self.__driver.simulateExecuteStatement()

            self.__driver.simulateStatementBefore(4,locals())
            k = k + 1
            self.__driver.simulateAssignStatement("k", k)

            self.__driver.simulateStatementBefore(5,locals())
            if rs[i] < rs[j]:
                self.__driver.simulateExecuteStatement()

                self.__driver.simulateStatementBefore(
                        6,
                        locals()
                        )
                rn[k] = rs[i]
                self.__driver.simulateAssignStatement(
                    ("rn", k),
                    rn.__str__()
                    )
                # 可视实体相当于从 r2 -> r1
                self.__driver.simulateVisionCopy(
                        "r%dnode%d" % (self.__level, i),
                        "r%dnode%d" % (self.__level - 1, k),
                        ('value',)
                        )

                self.__driver.simulateStatementBefore(
                        7,
                        locals()
                        )
                i = i + 1
                self.__driver.simulateAssignStatement("i", i)

            else:
                self.__driver.simulateExecuteStatement()

                self.__driver.simulateStatementBefore(
                        8,
                        locals()
                        )
                rn[k] = rs[j]
                self.__driver.simulateAssignStatement(
                    ("rn", k),
                    rn.__str__()
                    )
                # 可视实体相当于从 r2 -> r1
                self.__driver.simulateVisionCopy(
                        "r%dnode%d" % (self.__level, j),
                        "r%dnode%d" % (self.__level - 1, k),
                        ('value',)
                        )

                self.__driver.simulateStatementBefore(
                        9,
                        locals()
                        )
                j = j + 1
                self.__driver.simulateAssignStatement("j", j)

        self.__driver.simulateStatementBefore(10, locals())
        if i <= m:
            self.__driver.simulateExecuteStatement()

            self.__driver.simulateStatementBefore(11,locals())
            rn[k+1:n+1] = rs[i:m+1]
            for _index in range(k+1, n+1):
                self.__driver.simulateAssignStatement(
                        ("rn", _index),
                        rn.__str__()
                        )
            # 可视实体相当于从 r2 -> r1
            for _index in range(k+1, n+1):
               self.__driver.simulateVisionCopy(
                    "r%dnode%d" % (self.__level, i + _index - k - 1),
                    "r%dnode%d" % (self.__level - 1, _index),
                    ('value',)
                    )

        self.__driver.simulateStatementBefore(12, locals())
        if j <= n:
            self.__driver.simulateExecuteStatement()

            self.__driver.simulateStatementBefore(13,locals())
            rn[k+1:n+1] = rs[j:n+1]
            for _index in range(k+1, n+1):
                self.__driver.simulateAssignStatement(
                        ("rn", _index),
                        rn.__str__()
                        )
            # 可视实体相当于从 r2 -> r1
            for _index in range(k+1, n+1):
               self.__driver.simulateVisionCopy(
                    "r%dnode%d" % (self.__level, j + _index - k - 1),
                    "r%dnode%d" % (self.__level - 1, _index),
                    ('value',)
                    )

        # 函数返回语句
        self.__driver.simulateStatementBefore(14, locals())

    def __addVisionNode(self, r, s, t):

        self.__driver.disableVisionRefresh()
        
        _rname = 'r2_%d' % (self.__level)
        self.__driver.simulateVisionInsert(
            '__TOP__',
            'container',
            _rname,
            anchor='nw',            
            layout='queue',
            direction='right',
            cellwidth=40,
            cellheight=40,
            title=_rname,
            tanchor='w',
            txoffset=-20,
            )
        
        _r2 = []
        for i in range(len(r)):
            if i >= s and i <= t:
                _value = '0'
            else:
                _value = '-'
            _r2.append(_value)
            self.__driver.simulateVisionInsert(
                _rname,
                'node',
                'r%dnode%d' % (self.__level, i),
                shape='rectangle',
                value=_value,
                vanchor='center',
                options={'fill':'#1E90FF'},
                )

        self.__driver.appendVisionNode(
            '',
            'pointer',
            's%d' % (self.__level),
            target="r%dnode%d" % (self.__level, s),
            anchor='s',
            xoffset=0,
            yoffset=15,
            title='s',
            txoffset=10,
            tyoffset=10,
            options={'arrow':'last'}
            )
        self.__driver.appendVisionNode(
            '',
            'pointer',
            't%d' % (self.__level),
            target="r%dnode%d" % (self.__level, t),
            anchor='n',
            xoffset=0,
            yoffset=-15,
            title='t',
            txoffset=10,
            tyoffset=-10,
            options={'arrow':'last'}
            )

        self.__driver.enableVisionRefresh()
        
        return _r2

