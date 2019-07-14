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

"""
 * @文件：dsException.py
 *
 * @作者：赵俊德(jondy.zhao@gmail.com)
 *
 * @日期：2010/06/03
 *
 * @文件说明：
 *
 * 该文件已经被废止，从1.2.1版本之后不再使用。
 *
 * -------------------------------------------
 *
 * @作者：赵俊德(jondy.zhao@gmail.com)
 *
 * @创建日期: 2009/07/02
 *
 * @文件说明：
 *
 *    自定义异常，设置了异常处理的方式。
 *
 *    异常处理机制：
 *
 *    1. 程序启动过程的异常，直接抛出异常，终止应用程序。
 *
 *    2. 检查 License 过程中的异常。
 *        未知错误抛出异常，
 *        已知的错误返回错误信息。
 *
 *    3. 类 Application 初始化异常。
 *
 *    4. 程序退出之后的异常。
 *        譬如释放对象发现是 NoneType，算法线程没有被终止等。
 *
 *    每一个功能类或者模块都分配一定的错误代码，这个模块的
 *    出现的已知异常都通过抛出相应的错误代码来完成，每一个
 *    错误代码都有对应的错误信息格式字符串和必要的参数列表，
 *    上一层功能模块根据错误代码决定如何使用下层的错误信息。
 *
 *    对于未知的异常，每一层都不加处理。只在 dsMain.py 的
 *    相关顶层功能中处理。顶层函数会打印出 traceback 中的
 *    信息，从而得到出错的文件和代码行数。如果下一层加以
 *    处理之后，那么，处理部分的代码将覆盖真正出错的代码信
 *    息。
 *
 *    错误代码是一个 6 位整数，每一个模块分配 1,000 个代码。
 *
 *                        编号          范围          状态
 *    dsException          0            000 - 999       *
 *    dsMain               1          1,000 - 1,999     *
 *    dsConfigure          2          2,000 - 2,999     *
 *    dsDriver             3          3,000 - 3,999     *
 *    baseAlgorithm        4          4,000 - 4,999     *
 *    dsVisionEntity       5          5,000 - 5,999     *
 *    dsParameter          6          6,000 - 6,999     *
 *    dsCodeEntity         7
 *    dsStackEntity        8
 *    dsCodeView           9
 *    dsVisionView        10   
"""
if __debug__:
    import sys
    from traceback import print_exc, extract_tb


class dsError(Exception):
    """
    自定义异常，主要用于一般错误信息的处理。
    """
    def __init__(self, ecode, emsg="", *args):
        """
        ecode, 错误代码，每一个错误消息都有对应的代码。
        emsg,  错误消息的格式字符串。如果为 None，则自动
               根据错误代码取对应的字符串。
        *args, 格式字符串需要的参数，依次列出全部的参数
               如果没有需要的参数，那么省略第三个参数，例如
               rasie dsError(5, 'Second Error')
        """
        assert isinstance(ecode, int), ecode
        assert (isinstance(emsg, basestring) or
                    emsg is None), emsg
        if emsg is None:
            emsg = self.__emsg(ecode)
        Exception.__init__(self, emsg, *args)
        self.__ecode = ecode

    def ecode(self):
        return self.__ecode

    def __str__(self):
        try:
            if len(self.args) == 0:
                return ""
            elif len(self.args) == 1:
                return self.args[0].__str__()
            elif len(self.args) == 2:
                return self.args[0].format(self.args[1])
            elif len(self.args) >= 3:
                return self.args[0].format(*self.args[1:])
        except Exception, inst:
            if __debug__: print_exc(file=sys.stdout)
            return self.args.__str__()

    def __emsg(self, ecode):
        """ 返回错误代码对应的消息格式字符串 """
        # 代码：0
        # 参数：（）
        # 描述：特殊错误代码，没有任何错误信息。
        #
        if ecode == 0:
            return ""

        # 未知的错误代码
        assert False, "unknown error code %d" % ecode


if __name__ == "__main__":

    # 调试代码
    print "--------------------------"
    print 'dsError(0, "first")'
    _e = dsError(0, "first")
    print _e
    print _e.args
    print

    print "--------------------------"
    print 'dsError(0, "one{0}", 1)'
    _e = dsError(0, "one{0}", 1)
    print _e
    print _e.args
    print

    print "--------------------------"
    print 'dsError(0, "two{0}", (2))'
    _e = dsError(0, "tow{0}", (2))
    print _e
    print _e.args
    print

    print "--------------------------"
    print 'dsError(0, "three{0}", "s")'
    _e = dsError(0, "three{0}", "s")
    print _e
    print _e.args
    print

    print "--------------------------"
    print 'dsError(0, "first", 1, 2, 3)'
    _e = dsError(0, "first", 1, 2, 3)
    print _e
    print _e.args
    print

    print "--------------------------"
    print 'dsError(0, "first{0}", 4, 5, 6)'
    _e = dsError(0, "first{0}", 4, 5, 6)
    print _e
    print _e.args
    print

    print "--------------------------"
    print 'dsError(0, "second{0}{1}{2}", 7, 8, 9)'
    _e = dsError(0, "second{0}{1}{2}", 7, 8, 9)
    print _e
    print _e.args
    print

    print "--------------------------"
    print "dsError(0)"
    _e = dsError(0)
    print _e
    print _e.args
    print

    print "--------------------------"
    print 'dsError(0, "Expected Error:{0},{1}", (1,"3"))'
    _e = dsError(0, "Expected Error:{0},{1}", (1,"3"))
    print _e
    print _e.args
    print

    print "--------------------------"
    print 'dsError("a", "Assert Error")'
    try:
        _e = dsError("a", "Assert Error")
        print _e
        print _e.args
    except AssertionError, inst:
        print "Expected AssertionError:"
        print_exc(file=sys.stdout)
    print