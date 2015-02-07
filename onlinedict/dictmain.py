# -*- coding: utf-8 -*-

import os
import sys
import json

from aqt import mw
from anki.hooks import wrap, addHook, remHook
from aqt.utils import saveGeom, restoreGeom
from aqt.qt import *
from aqt.utils import openHelp, showInfo

import dictform
import odutils

# ------------------在线词典引擎自动加载-----------------------------------
DictInfos = {}
modulespath = os.path.dirname(__file__) + os.sep + "dict"
sys.path.insert(0, modulespath)
modulesfiles = os.listdir(modulespath)

for f in modulesfiles:
    name = f.split('.')
    if len(name) > 1 and name[1] == 'py' and name[0] != '__init__':
        module = __import__(f.replace(".py", ""))
        if hasattr(module, 'DictInfo'):
            DictInfos.update({name[0]: module.DictInfo})


class DictRetriver(QThread):

    def __init__(self, queryEngine, word):
        QThread.__init__(self)
        self.queryEngine = queryEngine
        self.word = word

    def run(self):
        # 确定默认的查询的目标(单词),并且获取查询数据
        self.queryEngine.query(self.word)
        self.emit(SIGNAL('sign_updateUi'))


class DictDialog(QDialog):

    def __init__(self, word):
        # 绑定ＵＩ
        QDialog.__init__(self, None, Qt.Window)
        self.word = word
        self.frm = dictform.Ui_OnlineDict()
        self.frm.setupUi(self)
        # 初始化数据
        self.initData()
        # 设置当前词典引擎
        self.setupDictEngine()
        # 显示查询结果
        self.queryAndShowResult()
        # 这个信号不能放在ＵＩ类中，否则会提前触发导致不可料想的后果
        self.connect(self.frm.comboBox, SIGNAL(
            "currentIndexChanged(int)"), self.changeDictEngine)

    def initData(self):
        # 词典引擎列表
        self.engines = DictInfos.keys()
         # 确定当前词典引擎名，及对应的查询引擎
        engine = odutils.getConfByKey("dict_engine")
        if not engine:
            self.engineIndex = 0
            engine = self.engines[self.engineIndex]
            odutils.setConfByKey("dict_engine", engine)
        else:
            self.engineIndex = self.engines.index(engine)
        self.queryEngine = DictInfos[engine]["queryEngine"]

    def setupDictEngine(self):
        self.frm.comboBox.addItems(
            [DictInfos[e]["name"] for e in self.engines])
        self.frm.comboBox.setCurrentIndex(self.engineIndex)

    def changeDictEngine(self, selected):
        self.engineIndex = selected
        engine = self.engines[self.engineIndex]
        odutils.setConfByKey("dict_engine", engine)
        self.queryEngine = DictInfos[engine]["queryEngine"]
        self.queryAndShowResult()

    def queryAndShowResult(self):
        self.frm.textBrowser.setHtml('loading...')
        self.retriver = DictRetriver(self.queryEngine, self.word)
        self.connect(self.retriver, SIGNAL("sign_updateUi"), self.updateUi)
        self.retriver.start()

    def updateUi(self):
        html = self.queryEngine.html()
        if self.frm.textBrowser.toHtml() == html:
            return
        self.frm.textBrowser.setHtml(html)
        self.frm.textBrowser.zoomIn(8)

dlg = None
# 查询


def onShowDict():
    card = mw.reviewer.card
    if not card:
        showInfo('Not in review now!')
        return

    word = card.note().values()[0].strip()
    global dlg
    if dlg:
        # 查询关键词相同，跳过
        if dlg.word == word:
            return
        # 试图关闭当前对话框，关闭失败则跳过
        if not dlg.close():
            return
    # 打开新的查询对话框
    dlg = DictDialog(word)
    dlg.setWindowIcon(QIcon(":/icons/contents.png"))
    dlgExitShortcut = QShortcut(QKeySequence("5"), dlg)
    dlgExitShortcut.connect(
        dlgExitShortcut, SIGNAL("activated()"), dlg, SLOT("close()"))
    dlg.exec_()
    dlg = None

odShortcut = QShortcut(QKeySequence("5"), mw)


def load():
    odShortcut.connect(odShortcut, SIGNAL("activated()"), onShowDict)


def unload():
    odShortcut.disconnect(odShortcut, SIGNAL("activated()"), onShowDict)

load()
