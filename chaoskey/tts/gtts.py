# -*- coding: utf-8 -*-

# 我的Anki插件
# 作者：混沌(youliang@chaoskey.com), http://blog.chaoskey.com

# TTS功能模块->谷歌TTS引擎

from anki.utils import stripHTML
from aqt import mw
from aqt.qt import QAction,SIGNAL

import os,re,subprocess,urllib
from subprocess import Popen, PIPE, STDOUT
from urllib import quote_plus

from comm import utils

#langs
langs = {'ar':u'العربية', #Arabic
         'ca':u'català', #Catalan
         'zh':u'中文', #Chinese
         'cs':u'český', #Czech
         'da':u'dansk', #Danish
         'de':u'Deutsch', #German
         'el':u'ελληνικά', #Greek
         'en':u'English', #English
         'es':u'español', #Spanish
         'fi':u'suomi', #Finnish
         'fr':u'français', #French
         'hu':u'magyar', #Hungarian
         'is':u'Icelandic', #Icelandic
         'it':u'italiano', #Italian
         'ja':u'日本語', #Japanese
         'ko':u'한국의', #Korean
         'nl':u'Nederlands', #Dutch
         'no':u'norsk', #Norwegian
         'pl':u'polski', #Polish
         'pt':u'português', #Portuguese
         'ro':u'român', #Romanian
         'ru':u'русский', #Russian
         'hr':u'hrvatski', #Croatian
         'sr':u'српски', #Serbian
         'sk':u'slovenčina', #Slovak
         'sq':u'shqiptar', #Albanian
         'sv':u'svenska', #Swedish
         'tr':u'Türk', #Turkish
         'id':u'Indonesia', #Indonesian
         'lv':u'Latvijas', #Latvian
         'vi':u'Việt', #Vietnamese
         'af':u'Afrikaans'} #Afrikaans

# ------------------谷歌TTS初始化-------------------------------------

# Google TTS 地址
googleTTS = 'http://translate.google.com/translate_tts'

# 获取代理
proxies = urllib.getproxies()
if len(proxies)>0 and "http" in proxies:
    proxStr = re.sub("http:", "http_proxy:", proxies['http'])
    googleTTS = proxStr + "/" + googleTTS

# 设置播放进程的启动信息
si = subprocess.STARTUPINFO()
try:
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
except:
    # python2.7+
    si.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW

# 谷歌TTS引擎
class GoogleEngine:
    def __init__(self):
        self.subproc=None
    
    def play(self,text,lang):
        if lang not in langs.keys():
            return False
        text = re.sub("\[sound:.*?\]", "", stripHTML(text.replace("\n", "")).encode('utf-8'))
        address = googleTTS+'?tl='+lang+'&q='+ quote_plus(text)        
        if subprocess.mswindows:
            param = ['mplayer.exe', '-ao', 'win32', '-slave', '-user-agent', "'Mozilla/5.0'", address]
            self.subproc=subprocess.Popen(param, startupinfo=si, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        else:
            param = ['mplayer', '-slave', '-user-agent', "'Mozilla/5.0'", address]
            self.subproc=subprocess.Popen(param, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        # 等待播放完成，并确定成功与否
        code=self.subproc and self.subproc.stdout and 'No stream found to handle url' not in self.subproc.stdout.read()
        self.subproc=None
        return code

    def stop(self):
        if self.subproc:
            self.subproc.kill()
            self.subproc=None

googleEngine=GoogleEngine()

# ------------------UI菜单构建---------------------------------------

# 本模块的信息
TTSInfo = {'name': u"谷歌TTS",
           'ttsEngine':googleEngine}

# 有待连接到上一级菜单的控件
googleTTSAction = QAction(TTSInfo["name"], mw)
googleTTSAction.setCheckable(True)
TTSInfo.update({"action":googleTTSAction})

# 控件事件响应
mw.connect(googleTTSAction, SIGNAL("triggered()"),lambda value=os.path.basename(__file__).replace(".py", ""): utils.setConfByKey("tts_engine",value))

