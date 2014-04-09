# -*- coding: utf-8 -*-

# 我的Anki插件
# 作者：混沌(youliang@chaoskey.com), http://blog.chaoskey.com

# TTS功能模块->自动选择TTS引擎(基于gtts.py和sapi5.py)

from aqt import mw
from aqt.qt import QAction,SIGNAL

from comm import utils
from comm.utils import globalVars

import os

# ------------------优先执行谷歌TTS，如果网络异常，则执行本地TTS----------

class AutoEngine:
        def __init__(self):
                self.googleEngine=None
                self.sapi5Engine=None
        
        def play(self,text,lang):
                ttsInfos=globalVars["TTSInfos"]
                self.googleEngine=ttsInfos["gtts"]["ttsEngine"]
                self.sapi5Engine=ttsInfos["sapi5"]["ttsEngine"]
                if not self.googleEngine.play(text,lang):
                        self.sapi5Engine.play(text, lang)
                self.googleEngine=None
                self.sapi5Engine=None
        
        def stop(self):
                if self.googleEngine:
                        self.googleEngine.stop()
                        self.googleEngine=None
                if self.sapi5Engine:
                        self.sapi5Engine.stop()
                        self.sapi5Engine=None

autoEngine=AutoEngine()


# ------------------UI菜单构建---------------------------------------

# 本模块的信息
TTSInfo = {'name': u"自动选择(谷歌TTS优先)",
           'ttsEngine':autoEngine}

# 有待连接到上一级菜单的控件
autoAction = QAction(TTSInfo["name"], mw)
autoAction.setCheckable(True)
TTSInfo.update({"action":autoAction})

# 控件事件响应
mw.connect(autoAction, SIGNAL("triggered()"),lambda value=os.path.basename(__file__).replace(".py", ""): utils.setConfByKey("tts_engine",value))


