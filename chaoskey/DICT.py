# -*- coding: utf-8 -*-

# 我的Anki插件
# 作者：混沌(youliang@chaoskey.com), http://blog.chaoskey.com

# 在线词典模块

import os,sys,json

from aqt import mw
from anki.hooks import wrap,addHook,remHook
from aqt.utils import saveGeom, restoreGeom
from aqt.qt import *
from aqt.utils import openHelp
from BeautifulSoup import BeautifulSoup

import forms as forms
from comm import onLoad,onSwitch,utils

# ------------------在线词典引擎自动加载-----------------------------------
DictInfos={}
modulespath = os.path.dirname(__file__)+"\\dict\\"
sys.path.insert(0, modulespath)
modulesfiles = os.listdir(modulespath)
for f in modulesfiles:
        name = f.split('.')
        if len(name) > 1 and name[1] == 'py' and name[0] != '__init__':
                module = __import__(f.replace(".py", ""))
                if hasattr(module, 'DictInfo'):
                        DictInfos.update({name[0]:module.DictInfo})

# ------------------在线词典对话框------------------
#  UI成员变量 :
#       self.frm
#       self.editor
#  数据成员变量 :
#       self.word		查询对象
#       self.engines	        在线词典引擎
#       self.engineIndex	指示当前词典引擎
#       self.queryEngine        当前查询引擎
#       self.modelFields	当前笔记类型的有效字段
#       self.mapping            当前词典字段到当前笔记类型字段的映射
#  动态控件成员变量 :
#       self.mapwidget		
class DictDialog(QDialog):

        def __init__(self,editor):
                self.timer=None
                # 绑定ＵＩ
                QDialog.__init__(self, editor.parentWindow, Qt.Window)
                self.editor=editor
                self.frm=forms.DictDialog.Ui_DictDialog()
                self.frm.setupUi(self)

                # 组合按钮的本地化修正
                self.frm.buttonBox.button(QDialogButtonBox.Help).setText(_("Help"))
                self.frm.buttonBox.button(QDialogButtonBox.Close).setText(_("Close"))
                
                # 初始化数据
                self.initData()
                
                # 设置字段对应布局
                self.setupMappingFrame()
                # 设置当前词典引擎
                self.setupDictEngine()

                # 显示当前查询对象
                self.showWordEdit()
                # 显示当前字段对应
                self.showMapping()
                # 显示查询结果
                self.showQueryResult()

                # 这个信号不能放在ＵＩ类中，否则会提前触发导致不可料想的后果
                self.connect(self.frm.dictEngine, SIGNAL("currentIndexChanged(int)"), self.changeDictEngine)
                # 父窗口关闭时，也要关闭本窗口
                self.connect(editor.parentWindow,SIGNAL("finished(int)"), lambda code: self.reject())  #父窗口是笔记编辑(添加)窗口的情形
                editor.parentWindow.closeEvent = wrap(editor.parentWindow.closeEvent, lambda event: self.reject(), "after") #父窗口是笔记浏览器窗口的情形
                # 鼠标进入下端文本显示区域后，再离开超过5秒，显示完整的结果
                self.frm.dictHtml.leaveEvent = wrap(self.frm.dictHtml.leaveEvent, lambda event: self.startTimer(None,5000), "before")
                self.frm.dictHtml.enterEvent = wrap(self.frm.dictHtml.enterEvent, lambda event: self.stopTimer(), "after")
                
        def initData(self):
                # 词典引擎列表
                self.engines=DictInfos.keys()
                # 确定当前词典引擎名，及对应的查询引擎
                engine=utils.getConfByKey("dict_engine")
                if not engine:
                        self.engineIndex=0
                        engine=self.engines[self.engineIndex]
                        utils.setConfByKey("dict_engine",engine)
                else:
                        self.engineIndex=self.engines.index(engine)
                self.queryEngine=DictInfos[engine]["queryEngine"]
                # 引擎的显示字段和当前笔记类型的字段
                engineFields=self.queryEngine.fieldSort
                self.modelFields=[_("<Ignore>")]
                self.modelFields.extend([v["name"] for v in self.editor.note.model()['flds']])
                # 建立引擎字段到记类型字段的映射
                _mapping=utils.getConfByKey("dict_mapping_%s_%s"%(engine,self.editor.note.model()['name']))
                if _mapping :
                        self.mapping=json.loads(_mapping)
                else:
                        minlen=min(len(engineFields),len(self.modelFields)-1)
                        _mapping=range(minlen)
                        _mapping.extend([-1]*(len(engineFields)-minlen))
                        self.mapping=_mapping
                        #utils.setConfByKey("dict_mapping_%s_%s"%(engine,self.editor.note.model()['name']),json.dumps(self.mapping))
                # 确定默认的查询的目标(单词),并且获取查询数据
                self.word=self.editor.note.fields[0].strip()
                self.queryEngine.query(self.word)

        def setupMappingFrame(self):
                self.frm.mappingArea.setContentsMargins(0,0,0,0)
                self.mapwidget = None

        def setupDictEngine(self):
                self.frm.dictEngine.addItems([DictInfos[e]["name"] for e in self.engines])
                self.frm.dictEngine.setCurrentIndex(self.engineIndex)

        def showWordEdit(self):
                self.frm.wordEdit.setText(self.word)
     
        def showQueryResult(self,field=None):
                self.stopTimer()
                if field :
                        title=field
                        html="<div style='line-height: normal; font-family: arial; font-size: 10pt'>%s</div>"%self.queryEngine.get(field)
                else:
                        title=self.queryEngine.name
                        html=self.queryEngine.html()
                if self.frm.dictHtml.toHtml()==html:
                        return
                self.frm.dictGroup.setTitle(title)
                self.frm.dictHtml.setHtml(html)
                # 几何尺寸自适应调整
                desktop=QApplication.desktop()
                if self.frameSize().height()<desktop.frameSize().height() or (self.x()>0 and self.frameGeometry().right()<desktop.geometry().right()) :
                        # 根据文本内容进行自适应调整
                        self.show()
                        deltaHeight=int(self.frm.dictHtml.document().size().height())-self.frm.dictHtml.height()
                        self.resize(self.width(),self.height()+deltaHeight)
                        # 由于超屏幕边界而进行自适应调整
                        bottom=self.frameGeometry().bottom()
                        desktopBottom=desktop.geometry().bottom()
                        if bottom>desktopBottom:
                                y=self.y()-bottom+desktopBottom
                                if y<0:
                                        y=0
                                self.move(self.x(),y)                
         
        def showMapping(self):
                if self.mapwidget:
                        self.frm.mappingArea.removeWidget(self.mapwidget)
                        self.mapwidget.deleteLater()
                self.mapwidget = QWidget()
                self.frm.mappingArea.addWidget(self.mapwidget)
                grid = QGridLayout(self.mapwidget)
                self.mapwidget.setLayout(grid)
                grid.setMargin(3)
                grid.setSpacing(4)
                engineFields=self.queryEngine.fieldSort
                for num in range(len(engineFields)):
                        label=QLabel("<b>%s</b>" %engineFields[num])
                        grid.addWidget(label, num, 0)
                        grid.addWidget(QLabel(_("<b>map to</b>")), num, 1)
                        comboBox = QComboBox(self.mapwidget)
                        comboBox.setStyleSheet("background-color: rgb(243, 243, 243);")
                        comboBox.addItems(self.modelFields)
                        if num>=len(self.mapping):
                                self.mapping.append(-1)
                        comboBox.setCurrentIndex(self.mapping[num]+1)
                        grid.addWidget(comboBox, num, 2)
                        # 在字段映射区左边字段上停留超过2秒，显示对应字段的结果
                        label.enterEvent = wrap(label.enterEvent, lambda event,field=engineFields[num]: self.startTimer(field,2000), "after")
                        label.leaveEvent = wrap(label.leaveEvent, lambda event: self.stopTimer(), "before")
                        self.connect(comboBox, SIGNAL("currentIndexChanged(int)"), lambda selected,n=num: self.changeMappingNum(selected-1,n))

        # 延时调用self.showQueryResult(...)
        def startTimer(self,field,sec):
                if self.timer==None:
                        self.timer=QTimer()
                self.timer.setSingleShot(True) # 单定时
                self.connect(self.timer, SIGNAL("timeout()"), lambda field=field: self.showQueryResult(field))
                self.timer.start(sec)

        # 提前终止定时器
        def stopTimer(self):
                if self.timer==None:
                        return
                if self.timer.isActive():
                        self.timer.stop()
                self.timer=None

        def changeMappingNum(self, selected,n):
                # 注销这段代码，是因为允许词典的多个字段映射到笔记的同一个字段中
##                try:
##                        if selected>-1:
##                                index=self.mapping.index(selected)
##                                self.mapping[index] = self.mapping[n]
##                except ValueError:
##                        pass
                self.mapping[n]=selected
                self.showMapping()

        def helpRequested(self):
                openHelp("FileImport")

        def changeDictEngine(self,selected):
                self.engineIndex=selected
                engine=self.engines[self.engineIndex]
                utils.setConfByKey("dict_engine",engine)
                self.queryEngine=DictInfos[engine]["queryEngine"]
                self.queryEngine.query(self.word)
                # 建立引擎字段到记类型字段的映射
                _mapping=utils.getConfByKey("dict_mapping_%s_%s"%(engine,self.editor.note.model()['name']))
                if _mapping :
                        self.mapping=json.loads(_mapping)
                else:
                        engineFields=self.queryEngine.fieldSort
                        minlen=min(len(engineFields),len(self.modelFields)-1)
                        _mapping=range(minlen)
                        _mapping.extend([-1]*(len(engineFields)-minlen))
                        self.mapping=_mapping
                        #utils.setConfByKey("dict_mapping_%s_%s"%(engine,self.editor.note.model()['name']),json.dumps(self.mapping))
                self.showMapping()
                self.showQueryResult()
        
        def onQuery(self):
                self.word=self.frm.wordEdit.text().strip()
                # 优先从网络上查询，查询失败则试图中本地数据库中查询
                self.queryEngine.query(self.word,True)
                self.showMapping()
                self.showQueryResult()

        def doMerge(self):
                engine=self.queryEngine.engine
                utils.setConfByKey("dict_mapping_%s_%s"%(engine,self.editor.note.model()['name']),json.dumps(self.mapping))
                engineFields=self.queryEngine.fieldSort
                for i in range(len(engineFields)):
                        fieldIndex=self.mapping[i]
                        if fieldIndex==-1:
                                continue
                        html=self.editor.note.fields[fieldIndex]
                        _html=(''.join(BeautifulSoup(html).findAll(text=True))).strip()
                        if fieldIndex==0 and _html!="":
                                continue
                        text=self.queryEngine.get(engineFields[i]).strip()
                        if text!="":
                                if _html=="":
                                    html=text
                                else:
                                    html+="<br />"+text
                                html = unicode(BeautifulSoup(html))
                                self.editor.note.fields[fieldIndex]=html
                self.editor.loadNote()
        
        def waitClose(self):
                self.exec_()
                # 对话框关闭时，必须停止内置定时器
                self.stopTimer()

# 确保此窗体的唯一性
dlg=None
def openDictDialog(editor):
        global dlg
        if dlg:
                # 查询关键词相同，跳过
                if dlg.word==editor.note.fields[0].strip():
                        return
                # 试图关闭当前对话框，关闭失败则跳过
                dlg.stopTimer()
                if not dlg.close():
                        return
        # 打开新的查询对话框
        dlg = DictDialog(editor)
        dlg.setWindowIcon(QIcon(":/icons/contents.png"))
        dlg.waitClose()
        dlg=None

def onlineDictButton(editor):
        dictButton = QPushButton(editor.widget)
        dictButton.setFixedHeight(20)
        dictButton.setFixedWidth(20)
        dictButton.setCheckable(True)
        dictButton.setIcon(QIcon(":/icons/contents.png"))
        dictButton.setToolTip(_("&Online Dict"))
        dictButton.setShortcut(_("Ctrl+O"))
        dictButton.setAutoDefault(False)
        dictButton.setFocusPolicy(Qt.NoFocus)
        dictButton.setStyle(editor.plastiqueStyle)
        dictButton.connect(dictButton, SIGNAL("clicked()"), lambda editor=editor: openDictDialog(editor))
        editor.iconsBox.addWidget(dictButton)


class ContextQuery(QDialog):
        def __init__(self):
                QDialog.__init__(self, None, Qt.Window)
                self.setWindowTitle(u"在线词典")
                self.connect(self, SIGNAL("finished(int)"), self._onQueryFinished)

                vbox = QVBoxLayout()
                vbox.setMargin(0)
                self.web = QTextBrowser()
                vbox.addWidget(self.web)
                self.setLayout(vbox)

                restoreGeom(self, "context_query")

        def showQueryResult(self,text):
                # 确定当前词典引擎名，及对应的查询引擎
                engine=utils.getConfByKey("dict_engine")
                if not engine:
                        engine=DictInfos.keys()[0]
                        utils.setConfByKey("dict_engine",engine)
                queryEngine=DictInfos[engine]["queryEngine"]
                queryEngine.query(text)
                self.web.setHtml(queryEngine.html())
                # 几何尺寸自适应调整
                desktop=QApplication.desktop()
                if self.frameSize().height()<desktop.frameSize().height() or (self.x()>0 and self.frameGeometry().right()<desktop.geometry().right()) :
                        # 根据文本内容进行自适应调整
                        self.show()
                        deltaHeight=int(self.web.document().size().height())-self.web.height()
                        self.resize(self.width(),self.height()+deltaHeight)
                        # 由于超屏幕边界而进行自适应调整
                        bottom=self.frameGeometry().bottom()
                        desktopBottom=desktop.geometry().bottom()
                        if bottom>desktopBottom:
                                y=self.y()-bottom+desktopBottom
                                if y<0:
                                        y=0
                                self.move(self.x(),y)

        def _onQueryFinished(self, ok):
                saveGeom(self, "context_query")

contextQuery=None

def closeContextQuery():
        global contextQuery
        if contextQuery:
                contextQuery.close()
                contextQuery=None

def slotContextQuery(text):
        closeContextQuery()        
        global contextQuery
        contextQuery=ContextQuery()
        contextQuery.showQueryResult(text)

def addQueryAction(self,menu):
        selectedText=self.selectedText()
        if selectedText and len(selectedText.strip())>1:
                #p=menu.addAction(_("Query"))
                p=menu.addAction(u"单词查询")
                p.connect(p, SIGNAL("triggered()"), lambda text=selectedText:slotContextQuery(text))

def load():
        addHook("setupEditorButtons", onlineDictButton)
        addHook("AnkiWebView.contextMenuEvent", addQueryAction)

def unload():
        remHook("setupEditorButtons", onlineDictButton)
        remHook("AnkiWebView.contextMenuEvent", addQueryAction)
# ------------------UI菜单构建---------------------------------------

# 本模块的信息
ModuleInfo = {'name': u'在线词典'}

plugName=os.path.basename(__file__).replace(".py", "")

# 添加功能开关
action=QAction(ModuleInfo["name"], mw)
action.setCheckable(True)
action.connect(action, SIGNAL("triggered()"),lambda:onSwitch(load,unload,action,plugName))
ModuleInfo.update({"action":action})

# 功能加载
onLoad(load,action,plugName)
