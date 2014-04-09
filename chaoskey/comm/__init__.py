# -*- coding: utf-8 -*-

# 我的Anki插件
# 作者：混沌(youliang@chaoskey.com), http://blog.chaoskey.com

from aqt import mw
from aqt.qt import *
from comm.reader import Reader
from comm.tts import TTSSpeaker
from comm import utils

# 功能加载
def onLoad(_load,_action,_name):
    switch=utils.getConfByKey('ck_switch_%s'%_name)
    switch=eval(switch) if switch else False
    if switch:
        _action.setChecked(switch)
        _load()

# 功能开关控制
def onSwitch(_load,_unload,_action,_name):
    checked=_action.isChecked()
    utils.setConfByKey('ck_switch_%s'%_name,str(checked))
    if checked:
        _load()
    else:
        _unload()

# Anki提供的该函数不满足我的要求，故修改后单独列出
def wrap(old, new, pos="after"):
    "Override an existing function."
    def repl(*args, **kwargs):
        if pos == "after":
            old(*args, **kwargs)
            return new(*args, **kwargs)
        elif pos == "before":
            new(*args, **kwargs)
            return old(*args, **kwargs)
        else:
            return new(old, *args, **kwargs)
    return repl

# 学习模式(在插件系统加载前,mw已经持有一个Reviewer实例)
studyMode=mw.reviewer
#阅读模式
readMode=Reader(mw)

speaker=TTSSpeaker()
defaultVoice=speaker.voiceName()
speaker.daemon=False
speaker.start()

def mwClose(force=False):
    speaker.kill()    

mw.onClose= wrap(mw.onClose, mwClose,pos="before")
