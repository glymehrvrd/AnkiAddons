# -*- coding: utf-8 -*-

import os
import sys
import sqlite3

# ----------------数据存储和读取-------------------

curpath = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))

# 数据库文件
datafile = os.path.join(curpath, "onlinedict.db").decode(
    sys.getfilesystemencoding())


def getCursor():
    conn = sqlite3.connect(datafile, isolation_level=None)
    conn.row_factory = sqlite3.Row
    return conn.cursor()

cursor = getCursor()

# 建表(配置表conf和词典数据表dict)
if len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='conf'").fetchall()) < 1:
    cursor.execute("CREATE TABLE conf (key text,value text)")
if len(cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dict'").fetchall()) < 1:
    cursor.execute("CREATE TABLE dict (key text,value text)")

# 配置读取


def getConfByKey(key):
    r = getCursor().execute(
        "SELECT value FROM conf WHERE key=?", (key,)).fetchone()
    if r:
        return r['value']
    return None


def setConfByKey(key, value):
    if getConfByKey(key):
        getCursor().execute(
            "UPDATE conf SET value=? WHERE key=?", (value, key))
    else:
        getCursor().execute(
            "INSERT INTO conf(key,value) VALUES(?,?)", (key, value))

# 词典数据读取


def getDictByKey(key):
    r = getCursor().execute(
        "SELECT value FROM dict WHERE key=?", (key,)).fetchone()
    if r:
        return r['value']
    return None


def setDictByKey(key, value):
    if getDictByKey(key):
        getCursor().execute(
            "UPDATE dict SET value=? WHERE key=?", (value, key))
    else:
        getCursor().execute(
            "INSERT INTO dict(key,value) VALUES(?,?)", (key, value))

# ----------------用来保存不方便访问的全局变量-------------------

globalVars = {}


# ----------------jinja2定制功能-------------------

from jinja2 import Environment

jinjaEnv = Environment()

# 将字符串变换成以该字符串为唯一元素的列表


def toList(s):
    if s == None:
        return []
    result = s
    if not isinstance(s, list):
        result = [s]
    return result

# 将toList(s)注册成jinja2模板中可用的过滤器
jinjaEnv.filters['toList'] = toList

# 将两个列表配对


def pair(l, r):
    left = toList(l)
    right = toList(r)
    result = []
    for i in range(min(len(left), len(right))):
        result.append((left[i], right[i]))
    return result

# 将pair(l,r)注册成jinja2模板中可用的全局函数
jinjaEnv.globals['pair'] = pair


# ----------------xml2json-------------------

# 将xml某个Element节点下子节点数据转换成json格式
#
# 注意：
#    1)输入参数必须是xml某个Element节点
#    2)返回结果是json字符串对应的数据结构，而不是json字符串
#    3)不考虑节点的属性，并且仅收集ELEMENT节点和TEXT节点的数据
#    4)仅考虑：非空TEXT节点和ELEMENT节点不出现在同一层次上
#            ,并且一旦出现了ELEMENT节点则忽略同一层次上的所有TEXT节点
# 调用范例：
#
# from xml.dom.minidom import parseString
#
# xml="......"
# dom=parseString(xml)
# js=xml2json(dom.documentElement)
#
def xml2json(node):
    js, _ = _xml2json(node)
    return js

# 参数node必须是ELEMENT节点
# 返回: node的节点值,node的标签值


def _xml2json(node):
    js = None             # node的节点值可能是：字符串、映射；而映射值则可能是列表、字符串、映射
    tag = node.tagName    # node标签
    for child in node.childNodes:
        if child.nodeType == child.ELEMENT_NODE:
            if not isinstance(js, dict):
                # 强制清除非映射数据,已经收集的同一层次的TEXT节点数据全部消失
                js = {}
            # 递归收集child的子节点数据
            value, key = _xml2json(child)
            if value == None:
                # 如果child没有节点数据，则跳过该子节点
                continue
            if js.has_key(key):
                # 如果tag对应有一个以上的节点，则映射值按列表的方式收集
                js[key] = toList(js[key])
                js[key].append(value)
            else:
                js[key] = value
        elif child.nodeType == child.TEXT_NODE and (not isinstance(js, dict)):
            # 如果还没有出现映射数据,则收集TEXT节点数据
            if js == None:
                js = ""
            js += child.nodeValue
    # node没有Element子节点，节点值是一个字符串；如果node同时没有非空TEXT节点，则返回None
    if isinstance(js, basestring):
        js = js.strip()
        if js == "":
            js = None
    return js, tag
