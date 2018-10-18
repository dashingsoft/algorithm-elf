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
# @文件：baseAlgorithm.py
#
# @作者：赵俊德(jondy.zhao@gmail.com)
#
# @创建日期: 2009/07/10
#
# @文件说明
#
# 算法基类文档，提供了算法相关的数据结构设计说明，以及算法框
# 架，算法参数处理的接口实现。
#
# 如果你想自己增加新的算法，该文档是第一个必须要读，里面包含
# 了新增算法的详细步骤。
#

'''
    本文件是算法基类，任何算法都必须继承该类。该类提供了
    关于算法实现的基本功能。譬如根据字符串参数生成树等。

    对于有Python开发经验的人，可以在本程序框架范围内增加
    一些新的数据结构算法演示。

    增加新算法需要了解如下内容：

    * dsDriver 接口规范，参考 dsDriver.py 的模块文档。
    * dsVision 实体定义，参考 dsVisionEntity.py 的模块文档。

    * 算法支持的参数类型和结构。
    * 算法基类的框架和提供的对参数和实体的处理方法。
    * 增加新算法的场景。

    以上三项均参考本文档下面的说明。

    算法支持的参数包括下列类型，
        整数，
        数值，
        字符串，
        数组，              类 dsParameterArray
        树，                类 dsParameterTree
        图，                类 dsParameterGraph


    增加一个新的算法演示程序的步骤：

    1. 在配置文件中增加一个算法说明。

       在配置文件dsdefault.xml的<algorithmgroup>下增加一个
       子结点<algorithm>
       <root><algorithmgroup>
           <algorithm name="Display Name" class="Class Name">
                <description>算法说明</description>
                <description lang="jp">日文说明</description>
                <option>...</option>
                ...
           </algorithm>

       <description> 是算法的说明，可以使用 lang 属性绑定
       到不同的语言，一般第一个是默认值，不指定lang属性。

       <option> 是算法主函数需要用到的参数。

        例如：
        <algorithm name="hanoi" class="hanoi">
            <option>
                <name>numberOfPlate</name>
                <type>number</type>
                <value>3</value>
                <validation>
                int(value) &gt; 0 and int(value) &lt; 10
                </validation>
                <description>
                The number of plate is used in this algorithm.
                </description>
                <description lang="zh"> 中文说明 </description>
            </option>
        </algorithm>

        参数说明的元素 <description> 同样也可以使用 lang 属性。

        可以使用 <displayname lang="langcode"> 来说明参数的显
        示名称，如果没有displayname，那么在配置窗口直接显示
        name，如果displayname中没有对应的语言，那么使用
        displayname中的没有 lang 属性的值。如果 displayname中
        没有缺省语言对应的项，那么还是显示 name。

        可以使用 <validation> 来校验输入的值，必须是一条合法的
        python 语句，参数值可以使用变量 value 来引用，类型都是
        字符串。

        对于整数类型，还可以使用 <min> 和 <max> 标签。

        参数的类型：
        integer，整数，对应的输入控件 TixControl
        string，字符串，              TixLabelEntry
        number，数值，                TixLabelEntry
        enum，枚举列表，              TixComboBox
        tree, 字符串格式的树定义。    TixLabelEntry + Arrrow
        graph, 字符串格式的图定义。   TixControl + Arrrow
        array, 应用于链表等，数值元素只能是数值或者字符串。
                                      TixControl + Arrrow


    2. 在算法库中增加一个算法类。

    按照算法类模版编写算法类，放置在目录 algorithm 下面，
    算法命名规范：首字母小写，其他单词首字母大写的连续词组，
    例如 mergingSort

    算法类程序模版：

    算法文档说明部分用来对算法进行描述，在主窗口算法选择一个
    算法之后，这里的信息会显示在输出窗口。(现在改成从配置文件
    中取算法说明信息了)

    对于这部分的国际化，需要在算法的 po 文件中增加对应的项，
    然后合并到 mo 文件中。

    第一部分是导入语句，
    from dsException import dsError
    from baseAlgorithm import baseAlgorithm
    这个是必须导入的，后面可以导入是算法需要的其他模块。

    算法需要终止通过抛出异常 dsError，异常包括三个参数，
    第一个是错误代码，算法的错误代码统一为 -1, 第二个是
    格式字符串，第三个是列表类型，为格式字符串提供参数。
    详细定义参看文件 dsException.py

    第二部分是源代码常量部分，每一个算法的主函数使用名称
    __srcCodeMain__，其他函数使用 __srcCodeFunctioName__
    表示，其中 FunctionName 是函数的名称。

    每一条有效代码占一行，中间不换行
    每一条有效代码之前一行使用<n>来标示，从1开始顺序编号

    第三部分是外部接口函数 prepare ，并且符合下列模版：
    #def prepare(driver, configure):
        return nameAlgorithm(driver, configure)

    第四部分是算法类定义
    #class nameAlgorithm:
        ...

    定义方法 __init__

    定义方法 run
        用于启动主程序。

    定义方法 算法演示函数
        算法函数是按照下列规则将算法源程序翻译过来的Python代码，

        算法函数中Python代码不可包含除了算法函数中使用的局部
        变量，需要的局部变量使用类属性代替。

        算法中使用的局部变量在函数开始的时候必须初始化，初始
        化语句在其他任何语句之前。

        然后就是函数调用的模拟语句：

        FunctionCall 模拟语句，格式如下：
                self.__driver.simulateFunctionCall(
                    __srcCodeMain__,
                    locals()
                    )

                其中第一个参数是源代码，第二个参数局部变量，
                固定为locals()

                该模拟语句一般只用于算法函数的第一条语句，用
                于装载当前函数到实体视图。

        每一个语句前调用 BeforeCall 模拟语句，格式如下：
                 self.__driver.simulateStatementBefore(
                        3,             # 有效代码号
                        locals()
                        )

        第一个参数是指上面定义的源代码中标识行 <n> 的数值，除
        了这个参数需要变化之外，其他直接拷贝即可。

        每一个语句后根据语句的类型分别调用
        FunctionReturn 模拟语句
                self.__driver.simulateFunctionReturn()
                用于函数调用语句之后使用。

        AssignStatement 模拟语句，格式如下
                self.__deriver.simulateAssignStatement(
                        "n",
                        4
                        )
                该模拟语句用于赋值语句之后调用，第一个参数是
                参数的名称，第二个参数是参数的新值。
                第一个参数支持的格式，
                    一个字符串，表示一个变量的名称。
                    一个2个元素的 Turple，这时候有两种情况，
                    如果第二个元素是数值，那么表示数组的下标
                    如果第二个元素是文本，那么表示孩子的名称
                例如：
                self.__deriver.simulateAssignStatement(
                        ("plates", 3),
                        4
                        )
                表示赋值语句 plates[3] = 4

        ExecuteStatement 模拟语句，格式如下：
            self.__driver.simulateExecuteStatement()
            在除了函数调用，赋值等语句之后的每一条一般语句执
            行之后调用。

        对于实体的移动，使用下列模拟函数
        simulateVisionMove
        simulateVisionInsert
        simulateVisionRemove
        simulateVisionCopy
        simulateVisionChange

        注意：
        simulateVisionInsert 不可以连续调用，如果一定要这么
        做，中间插入 sleep 语句。

    4. 定义其他辅助类函数，内部函数使用双下划线开头。

    5. 增加多语言的支持：
        配置文件中算法说明和参数说明可以提供多语言支持，
        算法代码中的消息需要生成对应的 po 文件。
        方法：将这两部分的内容生成对应的 po 文件，合并到相应
        的dsAssitant.mo 中。

    内部约束：
        类的名字必须和文件名一致，命名规则: xxxAlgorithm
        全局变量和局部变量名称不能相同。
        保留的关键字：_g_, _gt_, _lt_, _ct1_, _ct2_ , _s_
        不能作为变量名称使用。
        VisionNode 类的实体名称必须保证唯一性，并且不能使用
        数字开头，应该是一个合法的变量名称。

下面是一个算法类示例
'''

import dsException
import dsParameter


class baseAlgorithm:
    """ 算法基类 """
    
    def __init__(self):
        pass

    def buildInteger(self, strpara, radix=10):
        _uparameter = dsParameter.dsParameter(
            ).validateConfigurePrameter(strpara)
        try:
            return int(_uparameter, radix)
        except ValueError, inst:
            # 不是一个合法的整数
            raise dsException.dsError(
                4001,
                self.__emsg(4001),
                _uparameter
                )

    def buildFloat(self, strpara):
        _uparameter = dsParameter.dsParameter(
            ).validateConfigurePrameter(strpara)
        try:
            return float(_uparameter)
        except ValueError, inst:
            # 不是一个合法的数值
            raise dsException.dsError(
                4002,
                self.__emsg(4002),
                _uparameter
                )

    def buildString(self, strpara):
        return dsParameter.dsParameter(
            ).validateConfigurePrameter(strpara)

    def buildArrayList(self, namepattern, strarray, start=0):
        return dsParameter.dsArray(
            namepattern,
            strarray,
            start
            )

    def buildTreeList(self, strtree):
        tree = dsParameter.dsTree('none', '')
        tree.build(strtree)
        return tree
    
    def buildGraphList (self, strgraph):
        graph = dsParameter.dsGraph()
        graph.build(strgraph)
        return graph

    def validateTreeString(self, value):
        """ 校验字符串格式的树参数 """
        return self.buildTreeList(value)

    def validateGraphString(self, value):
        """ 校验字符串格式的图参数 """
        return self.buildGraphList(value)

    def validateArrayString(self, value):
        return self.buildArrayList('v_{0}', value)

    def __emsg(self, ecode):
        """ 返回错误代码对应的消息格式字符串 """
        # 代码：4000
        # 参数：（）
        # 描述：保留信息。
        #
        if ecode == 4000:
            return ""

        # 代码：4001
        # 参数：(参数值, 基数)
        # 描述：转换参数为整数时候出错，非法的数值参数
        #
        if ecode == 4001:
            return ("the value '{1}' is invalid literal for integer")

        # 代码：4002
        # 参数：（参数值)
        # 描述：将参数值转换成为浮点数的时候出错
        #
        if ecode == 4002:
            return ("the value '{1}' is invalid literal for float")

        # 未知的错误代码
        assert False, "unknown error code %d" % ecode

if __name__ == "__main__":
    b = baseAlgorithm()
    b.buildTreeList("A:[B, C]; B:[D]; C:[E, F]; E:[G, H]; F:[I]")
    

