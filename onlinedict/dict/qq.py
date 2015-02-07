# -*- coding: utf-8 -*-

# 我的Anki插件
# 作者：混沌(youliang@chaoskey.com), http://blog.chaoskey.com

# 在线词典模块->QQ词典插件

import os
import httplib
import urllib
import json
import odutils
from odutils import jinjaEnv

# 当前引擎名(以文件名作为引擎名)
engine = os.path.basename(__file__).replace(".py", "")
# 引擎显示名
name = u"QQ词典"


class QQDictEngine:

    def __init__(self):
        self.engine = engine
        self.name = name
        # Html模板
        self.htmlTemplate = jinjaEnv.from_string(u'''<html>
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
<!-- 基本解释 -->
{% for lo in data.local if data.local %}
<div style="font-size: 14pt">【基本解释】</div>
<br />
<div style="font-size: 14pt">
        <!-- 单词 -->
        <font color="#808080"><b>{{lo.word}}</b></font>
        <!-- 音标 -->
        {% for ph in lo.pho if lo.pho %}[<font color="#009900">{{ph}}</font>]{% endfor %}
</div>
<!-- 解释 -->
{% for de in lo.des if lo.des %}
<div>&nbsp;&nbsp;&nbsp;&nbsp;{{de.p}}{{de.d}}</div>
{% endfor %}
<!-- 单词相关变形 -->
{% if lo.mor %}<br />
<div>
        {% for mo in lo.mor %}
        {{mo.c}}:　<font color="#008000">{{mo.m}}</font>
        {% endfor %}
</div>
{% endif %}
<!-- 同反义词 -->
{% if lo.syn or lo.ant %}<br />{% endif %}
{% if lo.syn %}
<div>
<font color="#4d00cc"><b>同义词</b></font>&nbsp;&nbsp;
        {% for sy in lo.syn %}
        {% for c in sy.c %}<font color="#008000">{{c}}</font>　{% endfor %}
        {% endfor %}
</div>
{% endif %}
{% if lo.ant %}
<div>
<font color="#4d00cc"><b>反义词</b></font>&nbsp;&nbsp;
        {% for an in lo.ant %}
        {% for c in an.c %}<font color="#008000">{{c}}</font>　{% endfor %}
        {% endfor %}
</div>
{% endif %}
<!-- 例句 -->
{% for se in lo.sen %}
{% if loop.first %}<br />{% endif %}
<div>
        <div style="color: #4d00cc; font-size: 14pt"><u>例句{% if se.p %}({{se.p}}){% endif %}:</u></div>
        {% for s in se.s %}
                <div style="color: #009999">&nbsp;&nbsp;&nbsp;&nbsp;{{s.es}}</div>
                <div style="color: #01259a">&nbsp;&nbsp;&nbsp;&nbsp;{{s.cs}}</div>
        {% endfor %}
</div>
{% endfor %}
<!-- 相关词组 -->
{% for p in lo.ph %}
{% if loop.first %}<br /><div style="font-size: 12.5pt">相关词组</div>{% endif %}
<div>&nbsp;&nbsp;&nbsp;&nbsp;<font color="#009999">{{p.phs}}</font>　　<font color="#01259a">{{p.phd}}</font></div>
{% endfor %}
{% endfor %}

<!-- 情景会话 -->
{% for dl in data.dlg if data.dlg %}
{% if loop.first %}<br /><div style="font-size: 14pt">【情景会话】</div>{% endif %}
<br />
<div style="color: #4d00cc; font-size: 14pt"><b>{{dl.t}}</b></div>
{% for c in dl.c %}
<div>{{c.n}}:{{c.es}}</div>
<div>&nbsp;&nbsp;&nbsp;&nbsp;{{c.cs}}</div>
{% endfor %}
{% endfor %}
</body>
</html>''')
        # 字段映射模板
        self.mappingTemplate = {u"单词": jinjaEnv.from_string(u"{{lo.word}}"),
                                u"音标": jinjaEnv.from_string(u"{% for ph in lo.pho if lo.pho %}[{{ph}}]{% endfor %}"),
                                u"解释": jinjaEnv.from_string(u"{% for de in lo.des if lo.des%}{% if not loop.first %}<br />{% endif %}{{de.p}}{{de.d}}{% endfor %}"),
                                u"例句": jinjaEnv.from_string(u"{% for se in lo.sen %}{% if not loop.first %}<br />{% endif %}{% for s in se.s %}{% if not loop.first %}<br />{% endif %}【例】{{s.es}}　{{s.cs}}{% endfor %}{% endfor %}"),
                                u"变形词": jinjaEnv.from_string(u"{% if lo.mor %}【变】{% for mo in lo.mor %}{{mo.c}}:<font color=\"#008000\">{{mo.m}}</font>　{% endfor %}{% endif %}"),
                                u"同义词": jinjaEnv.from_string(u"{% if lo.syn %}【同】{% for sy in lo.syn %}{% for c in sy.c %}<font color=\"#008000\">{{c}}</font>　{% endfor %}{% endfor %}{% endif %}"),
                                u"反义词": jinjaEnv.from_string(u"{% if lo.ant %}【反】{% for an in lo.ant %}{% for c in an.c %}<font color=\"#008000\">{{c}}</font>　{% endfor %}{% endfor %}{% endif %}"),
                                u"词组": jinjaEnv.from_string(u"{% for p in lo.ph %}{% if not loop.first %}<br />{% endif %}【词】<font color=\"#009999\">{{p.phs}}</font>　　<font color=\"#01259a\">{{p.phd}}</font>{% endfor %}"),
                                u"对话": jinjaEnv.from_string(u"{% for dl in dlg if dlg %}{% if loop.first %}<br /><div style=\"font-size: 14pt\">【情景会话】</div>{% endif %}<div style=\"color: #4d00cc; font-size: 12pt\"><b>{{dl.t}}</b></div>{% for c in dl.c %}<div>{{c.n}}:{{c.es}}</div><div>&nbsp;&nbsp;&nbsp;&nbsp;{{c.cs}}</div>{% endfor %}{% endfor %}")}
        # 显示字段的排序
        self.fieldSort = [
            u"单词", u"音标", u"解释", u"例句", u"变形词", u"同义词", u"反义词", u"词组", u"对话"]
        # 保存查询结果
        self.data = {}

    # QQ单词查询
    def query(self, word, forceQuery=False):
        if word == None or len(word.strip()) == 0:
            return
        # 如果不要求强制查询，则优先本地数据库中查询；否则，优先从网络上查询
        if not forceQuery:
            js = odutils.getDictByKey("dict_query_%s_%s" % (engine, word))
            if js:
                self.data = json.loads(js)
                return
        # ------从QQ网站上查询------
        conn = httplib.HTTPConnection('dict.qq.com')
        ok = False
        try:
            conn.request("GET", "/dict?%s" % urllib.urlencode({'q': word}))
            res = conn.getresponse()
            if res.status == 200:
                # ------获取响应数据------
                self.data = json.loads(res.read())
                odutils.setDictByKey("dict_query_%s_%s" %
                                     (engine, word), json.dumps(self.data))
                ok = True
        except:
            pass
        finally:
            conn.close()
        # 网络查询失败
        if not ok and forceQuery:
            js = odutils.getDictByKey("dict_query_%s_%s" % (engine, word))
            if js:
                self.data = json.loads(js)
                ok = True
        # 最终还是失败
        if not ok:
            self.data = {}

    # 生成用来渲染的Html
    def html(self):
        if self.data:
            return self.htmlTemplate.render(data=self.data)
        return u"请联网再试！"

    # 生成用于显示的字段的数据
    def maps(self):
        if not self.data.has_key("local"):
            return {}
        l = self.data["local"][0]
        d = self.data.get("dlg", [])
        rs = {}
        for k, t in self.mappingTemplate.iteritems():
            v = t.render(lo=l, dlg=d).strip()
            if v != "":
                rs[k] = v
        return rs

    # 获取指定的显示的字段数据
    def get(self, field):
        if not self.data.has_key("local"):
            return ""
        l = self.data["local"][0]
        d = self.data.get("dlg", [])
        t = self.mappingTemplate.get(field)
        if t:
            return t.render(lo=l, dlg=d).strip()
        return ""

qqEngine = QQDictEngine()

# 本模块的信息
#
#    'name'             查询引擎的显示名
#    'queryEngine'      查询引擎
DictInfo = {"name": name,
            'queryEngine': qqEngine}
