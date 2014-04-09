# -*- coding: utf-8 -*-

# 我的Anki插件
# 作者：混沌(youliang@chaoskey.com), http://blog.chaoskey.com

# TTS功能模块->本地TTS(SAPI 5)引擎

from aqt import mw
from aqt.qt import QMenu,QAction,QActionGroup,SIGNAL

import os

from comm import utils,speaker,defaultVoice

#langids
langids = {'401':u'ar_العربية', #Arabic   (Saudi   Arabia)
           '801':u'ar_العربية', #Arabic   (Iraq)
           'c01':u'ar_العربية', #Arabic   (Egypt)
           '1001':u'ar_العربية',#Arabic   (Libya)
           '1401':u'ar_العربية',#Arabic   (Algeria)
           '1801':u'ar_العربية',#Arabic   (Morocco)
           '1c01':u'ar_العربية',#Arabic   (Tunisia)
           '2001':u'ar_العربية',#Arabic   (Oman)
           '2401':u'ar_العربية',#Arabic   (Yemen)
           '2801':u'ar_العربية',#Arabic   (Syria)
           '2c01':u'ar_العربية',#Arabic   (Jordan)
           '3001':u'ar_العربية',#Arabic   (Lebanon)
           '3401':u'ar_العربية',#Arabic   (Kuwait)
           '3801':u'ar_العربية',#Arabic   (U.A.E.)
           '3c01':u'ar_العربية',#Arabic   (Bahrain)
           '4001':u'ar_العربية',#Arabic   (Qatar)
           '403':u'ca_català', #Catalan
           '404':u'zh_中文', #Chinese  (Taiwan   Region)
           '804':u'zh_中文', #Chinese  (PRC)
           'c04':u'zh_中文', #Chinese  (Hong   Kong   SAR,   PRC)
           '1004':u'zh_中文',#Chinese  (Singapore)
           '405':u'cs_český', #Czech
           '406':u'da_dansk', #Danish
           '407':u'de_Deutsch', #German   (Standard)
           '807':u'de_Deutsch', #German   (Swiss)
           'c07':u'de_Deutsch', #German   (Austrian)
           '1007':u'de_Deutsch',#German   (Luxembourg)
           '1407':u'de_Deutsch',#German   (Liechtenstein)
           '408':u'el_ελληνικά', #Greek
           '409':u'en_English', #English  (United   States)
           '809':u'en_English', #English  (United   Kingdom)
           'c09':u'en_English', #English  (Australian)
           '1009':u'en_English',#English  (Canadian)
           '1409':u'en_English',#English  (New   Zealand)
           '1809':u'en_English',#English  (Ireland)
           '1c09':u'en_English',#English  (South   Africa)
           '2009':u'en_English',#English  (Jamaica)
           '2409':u'en_English',#English  (Caribbean)
           '2809':u'en_English',#English  (Belize)
           '2c09':u'en_English',#English  (Trinidad)
           '40a':u'es_español', #Spanish  (Traditional   Sort)
           '80a':u'es_español', #Spanish  (Mexican)
           'c0a':u'es_español', #Spanish  (Modern   Sort)
           '100a':u'es_español',#Spanish  (Guatemala)
           '140a':u'es_español',#Spanish  (Costa   Rica)
           '180a':u'es_español',#Spanish  (Panama)
           '1c0a':u'es_español',#Spanish  (Dominican   Republic)
           '200a':u'es_español',#Spanish  (Venezuela)
           '240a':u'es_español',#Spanish  (Colombia)
           '280a':u'es_español',#Spanish  (Peru)
           '2c0a':u'es_español',#Spanish  (Argentina)
           '300a':u'es_español',#Spanish  (Ecuador)
           '340a':u'es_español',#Spanish  (Chile)
           '380a':u'es_español',#Spanish  (Uruguay)
           '3c0a':u'es_español',#Spanish  (Paraguay)
           '400a':u'es_español',#Spanish  (Bolivia)
           '440a':u'es_español',#Spanish  (El   Salvador)
           '480a':u'es_español',#Spanish  (Honduras)
           '4c0a':u'es_español',#Spanish  (Nicaragua)
           '500a':u'es_español',#Spanish  (Puerto   Rico)
           '40b':u'fi_suomi', #Finnish
           '40c':u'fr_français', #French   (Standard)
           '80c':u'fr_français', #French   (Belgian)
           'c0c':u'fr_français', #French   (Canadian)
           '100c':u'fr_français',#French   (Swiss)
           '140c':u'fr_français',#French   (Luxembourg)
           '40e':u'hu_magyar', #Hungarian
           '40f':u'is_Icelandic', #Icelandic
           '410':u'it_italiano', #Italian  (Standard)
           '810':u'it_italiano', #Italian  (Swiss)
           '411':u'ja_日本語', #Japanese
           '412':u'ko_한국의', #Korean
           '812':u'ko_한국의', #Korean   (Johab)
           '413':u'nl_Nederlands', #Dutch    (Standard)
           '813':u'nl_Nederlands', #Dutch    (Belgian)
           '414':u'no_norsk', #Norwegian(Bokmal)
           '814':u'no_norsk', #Norwegian(Nynorsk)
           '415':u'pl_polski', #Polish
           '416':u'pt_português', #Portuguese(Brazilian)
           '816':u'pt_português', #Portuguese(Standard)
           '418':u'ro_român', #Romanian
           '419':u'ru_русский', #Russian
           '41a':u'hr_hrvatski', #Croatian
           '81a':u'sr_српски', #Serbian  (Latin)
           'c1a':u'sr_српски', #Serbian  (Cyrillic)
           '41b':u'sk_slovenčina', #Slovak
           '41c':u'sq_shqiptar', #Albanian
           '41d':u'sv_svenska', #Swedish
           '81d':u'sv_svenska', #Swedish  (Finland)
           '41f':u'tr_Türk', #Turkish
           '421':u'id_Indonesia', #Indonesian
           '426':u'lv_Latvijas', #Latvian
           '42a':u'vi_Việt', #Vietnamese
           '436':u'af_Afrikaans'} #Afrikaans

# ------------------本地TTS初始化-------------------------------------

# 本地已安装的TTS引擎列表
voices={}
for v in speaker.voices():
        name=v.GetAttribute("Name")
        langid=v.GetAttribute("Language").split(";")[0]
        lang=langids.get(langid)
        if not lang:
                lang=u"other_其他"
        if voices.has_key(lang):
                voices[lang].append(name)
        else:
                voices[lang]=[name]

# 初始化各种语言的默认引擎
for k,v in voices.iteritems():
        k=k.split("_")[0]
        voice=utils.getConfByKey("tts_sapi5_%s"%k)
        if (not voice) or (voice not in v):
                if defaultVoice in v :
                        voice=defaultVoice
                else:
                        voice=v[0]
                utils.setConfByKey("tts_sapi5_%s"%k,voice)

# ------------------执行本地TTS-------------------------------------

class SAPI5Engine:
        def play(self,text,lang):
                voice=utils.getConfByKey("tts_sapi5_%s"%lang)
                if voice:
                        speaker.play(text,voice)
                return False

        def stop(self):
                speaker.clear()

sapi5Engine=SAPI5Engine()

# ------------------UI菜单构建---------------------------------------

# 本模块的信息
TTSInfo = {'name': u"本地TTS(SAPI 5)",
           'ttsEngine':sapi5Engine}

# 有待连接到上一级菜单的控件
sapi5Action = QAction(TTSInfo["name"], mw)
sapi5Action.setCheckable(True)
TTSInfo.update({"action":sapi5Action})

# 控件事件响应
mw.connect(sapi5Action, SIGNAL("triggered()"),lambda value=os.path.basename(__file__).replace(".py", ""): utils.setConfByKey("tts_engine",value))

# 有待连接到上一级菜单的配置菜单
sapi5Menu = QMenu(u"%s的选择"%TTSInfo["name"], mw)
TTSInfo.update({"menu":sapi5Menu})

# 自动挂载配置子菜单
for k,v in voices.iteritems():
        k,z=k.split("_")
        sapi5Menu.addSeparator();
        selectGroup = QActionGroup(mw)
        for name in v:
                action = QAction("%s %s"%(z,name), mw)
                action.setCheckable(True)
                mw.connect(action, SIGNAL("triggered()"),lambda key="tts_sapi5_%s"%k,value=name: utils.setConfByKey(key,value))

                selectGroup.addAction(action)
                voice=utils.getConfByKey("tts_sapi5_%s"%k)
                if voice and name==voice:
                        action.setChecked(True)
        
                sapi5Menu.addAction(action)
