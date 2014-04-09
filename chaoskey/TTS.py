# -*- coding: utf-8 -*-

# 我的Anki插件
# 作者：混沌(youliang@chaoskey.com), http://blog.chaoskey.com

# TTS功能模块

from anki import sound
from aqt import mw
from aqt.qt import *

import sys,re,os,thread
import threading

from comm import onLoad,onSwitch,wrap,studyMode,readMode,utils
from comm.utils import globalVars

# 相邻的同种语言合并
def appendList(k,v,l):
    if l==None:
        return
    last=len(l)-1
    if last>=0 and l[last][0]==k:
        l[last][1]+=v
    else:
        l.append([k,v])


# 将英文与其它语言分离，保存在外部列表：split
def langEnSplit(text,other,split):
    #搜索连续的英文字符串（至少要两个英文字母连续）
    start=0
    end=len(text)
    it=re.finditer("[\x20-\x7e][\x20-\x7e]+",text)
    for m in it:
        # 确定前一段是否是非英文字符串
        o=""
        if m.start()>start:
            o=text[start:m.start()].strip()
        start=m.end()
        # 当前英文字符串（不能全由非字母组成,比如："--------!#+-"不认为是英文字符串）
        en=m.group().strip()
        if re.sub("[^a-zA-Z]","",en).strip()=="":
            o=o+en
            en=""
        # 提取到的非英文部分
        if len(o)>0:
            appendList(other,o,split)
        # 提取到的英文部分
        if len(en)>0:
            appendList("en",en,split)
    # 尾部剩余部分必然是非英文部分
    if start<end:
        o=text[start:end]
        appendList(other,o,split)

# 按正则表达式对应匹配的语言分离
def langSplit(text,langs,regexp=None):
    split=[]
    try:
        if regexp==None :
            if len(langs)<2:
                appendList(langs[0],text,split)
                return split
            if langs[0]=="en":
                # 试图分离纯英文部分
                langEnSplit(text,langs[1],split)
            return split
        rs=re.findall(regexp,text)
        for r in rs:
            if isinstance(r,basestring):
                # 只有一个分组的情况
                if len(langs)>1 and langs[0]=="en" :
                    # 试图分离纯英文部分
                    langEnSplit(r,langs[1],split)
                else:
                    appendList(langs[0],r,split)
            else:
                for i in range(len(r)):
                    if i<len(langs):
                        appendList(langs[i],r[i],split)
    except re.sre_compile.error , e:
        sys.stderr.write(u"你写的正则表达式：\"%s\",语法错误：%s。\n"%(regexp,e))
    return split

# ------------------TTS引擎自动加载-----------------------------------
TTSInfos={}
modulespath = os.path.dirname(__file__)+"\\tts\\"
sys.path.insert(0, modulespath)
modulesfiles = os.listdir(modulespath)
for f in modulesfiles:
        name = f.split('.')
        if len(name) > 1 and name[1] == 'py' and name[0] != '__init__':
                module = __import__(f.replace(".py", ""))
                if hasattr(module, 'TTSInfo'):
                        TTSInfos.update({name[0]:module.TTSInfo})

# 将变量TTSInfos作为全局变量保存
globalVars["TTSInfos"]=TTSInfos

# TTS播放器
class TTSPlayer(threading.Thread):
    def __init__(self,tospeak):
        threading.Thread.__init__(self)
        self.stoping=False
        self.tospeak=tospeak
        self.ttsEngine=None
    
    def run(self):
        _engine=utils.getConfByKey("tts_engine") # 默认TTS引擎
        for item in self.tospeak:
            # 待读文本
            text = ''.join(item.findAll(text=True))
            # 语种
            lang = item.get('lang',"zh")
            # 确定TTS引擎
            engine = item.get('engine',_engine)
            if not engine:
                continue
            self.ttsEngine=TTSInfos[engine]["ttsEngine"]
            # 文本切割
            for r in langSplit(text,lang.split("-"),item.get('regexp')):
                if self.stoping:
                    # 接受到停止命令
                    return
                self.ttsEngine.play(r[1], r[0])
        
    def stop(self):
        self.stoping=True
        if self.ttsEngine:
            self.ttsEngine.stop()
            self.ttsEngine=None


# 保证单个TTS播放器
player=None
def playTTS(text):
    # 在启动新的TTS播放器前，必须清除老的
    global player
    if player:
        player.stop()
    player=TTSPlayer(getTTSHTML(text))
    player.start()

def getTTSHTML(html):
    from BeautifulSoup import BeautifulSoup        
    soup = BeautifulSoup(html)
    
    tospeakhtml = []        
    for htmltag in soup('tts'):
        text = ''.join(htmltag.findAll(text=True)) #get all the text from the tag and stips html
        if text == None or text == '' or text.isspace():
            continue #skip empty tags
        tospeakhtml.append(htmltag)
    return tospeakhtml

# ------------------事件响应及处理-----------------------------------
def ttsAutoRead(toread):
    # 如果已经有发音，则不执行TTS
    if not sound.hasSound(toread):
        playTTS(toread)

# 提问后响应
def OnQuestion(self):
    ttsAutoRead(self.card.q())

# 回答后响应
def OnAnswer(self):
    # 在显示答案前清除老的TTS播放器
    global player
    if player:
        player.stop()
        player=None
    ttsAutoRead(self.card.a())

# 按键响应
def newKeyHandler(self, evt):
    pkey = evt.key()
    if (self.state == 'answer' or self.state == 'question'):
        if (pkey == Qt.Key_F3):
            playTTS(self.card.q())  
        elif (self.state=='answer' and pkey == Qt.Key_F4):
            playTTS(self.card.a()) 
    evt.accept()

oldStudyKeyHandler=studyMode._keyHandler
oldReadKeyHandler=readMode._keyHandler

oldStudyShowQuestion=studyMode._showQuestion
oldStudyShowAnswer=studyMode._showAnswer
oldReadShowAnswer=readMode._showReader

# 在原来nextCard函数调用前插入代码
def onNextCard(k=3):
    # 在下一张卡片出现前清除老的TTS播放器
    global player
    if player:
        player.stop()
        player=None

oldStudyNextCard=studyMode.nextCard
oldReadNextCard=readMode.nextCard


# ------------------UI菜单构建---------------------------------------

# 本模块的信息
ModuleInfo = {'name': u'TTS引擎'}

# 有待连接到上一级菜单的子菜单
ttsMenu = QMenu(u"%s配置"%ModuleInfo["name"], mw)
ttsMenu.setEnabled(False)
ModuleInfo.update({"menu":ttsMenu})

# TTS引擎选择列表
ttsGroup = QActionGroup(mw)
ttsEngine=utils.getConfByKey("tts_engine")
if not ttsEngine:
        ttsEngine=TTSInfos.keys()[0]
        utils.setConfByKey("tts_engine",ttsEngine)
for k,v in TTSInfos.iteritems():
        if v.has_key("action"):
                ttsGroup.addAction(v["action"])
                if k==ttsEngine:
                        v["action"].setChecked(True)
                ttsMenu.addAction(v["action"])

# 继续加载子菜单(如果有的话)
ttsMenu.addSeparator()
for k,v in TTSInfos.iteritems():
        if v.has_key("menu"):
                ttsMenu.addMenu(v["menu"])

def load():
    if not ttsMenu.isEnabled():
        ttsMenu.setEnabled(True)

    if hasattr(mw.col,"sched") and mw.col.sched and mw.state!="deckBrowser":
        mw.moveToState("deckBrowser")

    studyMode._keyHandler = wrap(studyMode._keyHandler, lambda evt:newKeyHandler(studyMode,evt), "before")
    readMode._keyHandler = wrap(readMode._keyHandler, lambda evt:newKeyHandler(readMode,evt), "before")

    studyMode._showQuestion = wrap(studyMode._showQuestion, lambda s=studyMode:OnQuestion(s), "after")
    studyMode._showAnswer  = wrap(studyMode._showAnswer, lambda s=studyMode:OnAnswer(s), "after")
    readMode._showReader  = wrap(readMode._showReader, lambda s=readMode:OnAnswer(s), "after")

    studyMode.nextCard  = wrap(studyMode.nextCard, onNextCard, "before")
    readMode.nextCard  = wrap(readMode.nextCard, onNextCard, "before")

def unload():
    if ttsMenu.isEnabled():
        ttsMenu.setEnabled(False)

    if hasattr(mw.col,"sched") and mw.col.sched and mw.state!="deckBrowser":
        mw.moveToState("deckBrowser")

    studyMode._keyHandler=oldStudyKeyHandler
    readMode._keyHandler=oldReadKeyHandler

    studyMode._showQuestion=oldStudyShowQuestion
    studyMode._showAnswer=oldStudyShowAnswer
    readMode._showReader=oldReadShowAnswer

    studyMode.nextCard=oldStudyNextCard
    readMode.nextCard=oldReadNextCard

plugName=os.path.basename(__file__).replace(".py", "")

# 添加功能开关
action=QAction(ModuleInfo["name"], mw)
action.setCheckable(True)
action.connect(action, SIGNAL("triggered()"),lambda:onSwitch(load,unload,action,plugName))
ModuleInfo.update({"action":action})

# 功能加载
onLoad(load,action,plugName)
