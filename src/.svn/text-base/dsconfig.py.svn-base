# -*- coding: utf-8 -*-
#
#############################################################
#                                                           #
#      版权所有 2009 - 2010 德新软件公司。保留全部权利。    #
#                                                           #
#      数据结构算法助手                                     #
#                                                           #
#      版本区间：1.2.1 -                                    #
#                                                           #
#############################################################

"""
 * @文件：dsconfig.py
 *
 * @作者：赵俊德(jondy.zhao@gmail.com)
 *
 * @创建日期: 2010/03/10
 *
 * @文件说明：
 *
 *   配置参数接口。
 *
"""

import os
import codecs
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import fromstring


class AlgorithmConfigure(object):
    """算法配置类。 """

    def __init__(self, filename):
        self.__xmltree = ElementTree()
        self.__filename = os.path.splitext(filename)[0] + ".cfg"
        if not os.path.exists(self.__filename):
            f = codecs.open(self.__filename, "w", encoding='utf-8')
            f.write("<root></root>")
            f.close()
        self.__xmltree.parse(self.__filename)
        self.__data = {"vars":[], "options":{}}

    def get(self):
        """设置算法的配置信息，包括参数初始化和可见对象的显示选项。

        特别要注意检查参数的类型是否属于可以识别的类型。

        """
        self.__data.clear()
        self.__data = {"vars":[], "options":{}}
        for _para in self.__xmltree.findall("variable"):
            _name = _para.find("name").text
            _text = _para.find("value").text
            if _text is None: _text = ""
            _type = _para.find("type")
            _options = {}
            for (k, v) in _para.items():
                try:
                    if k == "watch":
                        _value = v
                    else:
                        _value = eval(v, {}, {})
                except Exception:
                    _value = v
                _options[k] = _value
            _value = [_type.text, _text, _options]
            self.__data["vars"].append([_name, _value])
        return self.__data

    def write(self):
        self.__xmltree.getroot().clear()
        for _para in self.__data["vars"]:
            _name = _para[0]
            _type = _para[1][0].capitalize()
            _value = _para[1][1]
            _options = _para[1][2]
            _node = fromstring(
                "<variable><name>{0}</name>"
                "<type>{1}</type><value>{2}</value>"
                "</variable>".format(_name, _type, _value)
                )
            for k, v in _options.iteritems():
                _node.set(k, v)
            self.__xmltree.getroot().append(_node)

        self.__xmltree.write(self.__filename, "utf-8")


if __name__ == "__main__":
    _configure = AlgorithmConfigure("data/px.paf")
    _data = _configure.get()
    print _data

    #_data["vars"].append([u'c', ['Integer', u'0', {}]])
    #_data["vars"].append([u'd', ['String', u'123', {}]])
    #_configure.write()

