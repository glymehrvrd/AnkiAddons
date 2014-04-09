# -*- coding: utf-8 -*-

# 我的Anki插件
# 作者：混沌(youliang@chaoskey.com), http://blog.chaoskey.com

# 在线词典模块->爱词霸词典插件

import os,httplib, urllib,json
from xml.dom.minidom import parseString
import odutils
from odutils import jinjaEnv

# 当前引擎名(以文件名作为引擎名)
engine=os.path.basename(__file__).replace(".py", "")
# 引擎显示名
name=u"爱词霸词典"

# 引擎类
class IcibaDictEngine:
        def __init__(self):
                self.engine=engine
                self.name=name
                # 引擎的Html模板
                self.htmlTemplate=jinjaEnv.from_string(u'''<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf8">
	<style type="text/css">
	* {
                margin:0;
                padding:0;
                font-family: arial;
                color: black;
                line-height: normal;
        }
	</style>
</head>
<body>
{% if data.key %}
<div style="font-size: 14pt">
        <!-- 单词 -->
        <font color="#808080"><b>{{data.key}}</b></font>
        <!-- 音标 -->
        {% for ps in data.ps|toList if data.ps %}[<font color="#009900">{{ps}}</font>]{% endfor %}
</div>	
<!-- 解释 -->
{% for l,r in pair(data.pos,data.acceptation) %}
<div>&nbsp;&nbsp;&nbsp;&nbsp;{{l}}{{r}}</div>
{% endfor %}

<!-- 例句 -->
{% for s in data.sent|toList if data.sent %}
{% if loop.first %}<br /><div><div style="color: #4d00cc; font-size: 14pt"><u>例句:</u></div>{% endif %}
        <div style="color: #000000">&nbsp;&nbsp;&nbsp;&nbsp;{{s.orig}}</div>
        <div style="color: #01259a">&nbsp;&nbsp;&nbsp;&nbsp;{{s.trans}}</div>
{% if loop.last %}</div>{% endif %}
{% endfor %}        
{% endif %}
</body>
</html>''')
                # 显示字段的映射模板
                self.mappingTemplate={u"单词":jinjaEnv.from_string(u"{% if data.key %}{{data.key}}{% endif %}"),
                              u"音标":jinjaEnv.from_string(u"{% for p in data.ps|toList if data.ps %}[{{p}}]{% endfor %}"),
                              u"音频":jinjaEnv.from_string(u"{% for p in data.pron|toList if data.pron %}{% if not loop.first %}<br />{% endif %}{{p}}{% endfor %}"),
                              u"解释":jinjaEnv.from_string(u"{% for l,r in pair(data.pos,data.acceptation) %}{% if not loop.first %}<br />{% endif %}{{l}}{{r}}{% endfor %}"),
                              u"例句":jinjaEnv.from_string(u"{% if data.sent %}{% for s in data.sent|toList %}{% if not loop.first %}<br />{% endif %}【例】{{s.orig}}　{{s.trans}}{% endfor %}{% endif %}")}
                # 显示字段的排序
                self.fieldSort=[u"单词",u"音标",u"音频",u"解释",u"例句"]
                # 保存查询结果
                self.data={}
                        
        # 爱词霸单词查询
        def query(self,word,forceQuery=False):
                if word==None or word.strip()=="":
                        return
                # 如果不要求强制查询，则优先本地数据库中查询；否则，优先从网络上查询
                if not forceQuery:
                        js=odutils.getDictByKey("dict_query_%s_%s"%(self.engine,word))
                        if js:
                                self.data=json.loads(js)
                                return
                # ------从爱词霸网站上查询------
                conn = httplib.HTTPConnection('dict-co.iciba.com')
                params = urllib.urlencode({'w': word, 'key':'6B1B4E9C16D04965F2E0732E3498C756'})
                headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
                ok=False
                try:
                        conn.request("GET", "/api/dictionary.php?"+params,None, headers) 
                        res = conn.getresponse()
                        if res.status==200:
                                # ------提取XML数据------
                                self.data=odutils.xml2json(parseString(res.read()).documentElement)
                                odutils.setDictByKey("dict_query_%s_%s"%(self.engine,word),json.dumps(self.data))
                                ok=True
                except:
                        pass
                finally:
                        conn.close()
                # 网络查询失败
                if not ok and forceQuery:
                        js=odutils.getDictByKey("dict_query_%s_%s"%(self.engine,word))
                        if js:
                                self.data=json.loads(js)
                                ok=True
                # 最终还是失败
                if not ok :
                        self.data={}
        
        # 生成用来渲染的Html
        def html(self):
                if self.data:
                        return self.htmlTemplate.render(data=self.data)
                return u"请联网再试！"
        
        # 生成用于显示的字段的数据
        def maps(self):
                rs={}
                for k,t in self.mappingTemplate.iteritems():
                        v=t.render(data=self.data).strip()
                        if v!="":
                                rs[k]=v
                return rs

        # 获取指定的显示的字段数据
        def get(self,field):
                t=self.mappingTemplate.get(field)
                if t :
                        return t.render(data=self.data).strip()
                return ""

icibaEngine=IcibaDictEngine()

# 本模块的信息
#
#    'name'             查询引擎的显示名
#    'queryEngine'      查询引擎
DictInfo = {"name":name,
            'queryEngine':icibaEngine}


