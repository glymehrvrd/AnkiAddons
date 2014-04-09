# -*- coding: utf-8 -*-

# 我的Anki插件
# 作者：混沌(youliang@chaoskey.com), http://blog.chaoskey.com

from aqt import mw
from aqt.qt import Qt
from anki.utils import json,ids2str
from anki.hooks import runHook,remHook
from anki.sound import playFromText, clearAudioQueue
from aqt.utils import getBase
from anki.sound import stripSounds
from aqt.reviewer import Reviewer
import re

readQuery={"all":"deck:current card:1",
    "all_task":"deck:current card:1",
    "new":"deck:current is:new",
    "learn":"deck:current is:learn",
    "due":"deck:current is:due",
    "review":"deck:current is:review card:1",
    "marked":"deck:current tag:marked card:1",
    "leech":"deck:current tag:leech card:1",
    "added":"deck:current added:1",
    "rated":"deck:current rated:1",
    "rated2":"deck:current rated:1:1"
}

class Reader(Reviewer):
    "Manage reviews.  Maintains a separate state."

    def __init__(self, mw):
        Reviewer.__init__(self,mw)
        self.readType="all"
        self.readLimit=-1
        self.autoPlay=False
        self.speed=2  #(1-10)
        remHook("leech",self.onLeech)

    def show(self):
        self.cards=mw.col.findCards(readQuery.get(self.readType,"deck:current card:1")) 
        if self.readLimit>-1:
            self.cards=self.cards[:self.readLimit]
        self.did=self.mw.col.decks.selected() #当前牌组
        self.deck=self.mw.col.decks.get(self.did)
        self.curr_index=0 #当前阅读卡牌在self.cards中的位置
        self.curr_cid=self.deck.get('%s_cid'%self.readType)
        if self.curr_cid in self.cards:
            self.curr_index=self.cards.index(self.curr_cid)
        elif not self.cards:
            self.curr_cid=None
        else:
            self.curr_cid=self.cards[self.curr_index]
        self._first = True

        # 用不到成员变量
        self.cardQueue=[]
        self.hadCardQueue = False
        self._answeredIds = []
        self.typeCorrect = None

        Reviewer.show(self)

    def lastCard(self):
        pass

    def cleanup(self):
        pass

    def nextCard(self,nav=0):
        if not (hasattr(mw,"col") and mw.col and hasattr(mw.col,"getCard") and mw.col.getCard):
            return
        if not (self.cards and len(self.cards)>0):
            self.curr_index=0
            self.curr_cid=None
        elif nav==1:
            self.curr_index=0
            self.curr_cid=self.cards[self.curr_index]
        elif nav==2:
            self.curr_index-=1
            if self.curr_index<0:
                self.curr_index=0
                self.curr_cid=None
            else:
                self.curr_cid=self.cards[self.curr_index]
        elif nav==3:
            self.curr_index+=1
            if self.curr_index>len(self.cards)-1:
                self.curr_index=0
                self.curr_cid=None
            else:
                self.curr_cid=self.cards[self.curr_index]
        elif nav==4:
            self.curr_index=len(self.cards)-1
            self.curr_cid=self.cards[self.curr_index]
        self.card=None
        if self.curr_cid:
            self.card=self.mw.col.getCard(self.curr_cid)
        self.save()
        clearAudioQueue()
        if not self.card:
            self.autoPlay=False
            self.mw.moveToState("overview")
            return
        self.card.startTimer()
        if self._first:
            # we recycle the webview periodically so webkit can free memory
            self._initWeb()
        else:
            self._showReader()

    def _initWeb(self):
        self._first = 0
        self._bottomReady = False
        base = getBase(self.mw.col)
        # main window
        self.web.stdHtml(self._revHtml, self._styles(),
            loadCB=lambda x: self._showReader(),
            head=base)
        # show answer / ease buttons
        self.bottom.web.show()
        self.bottom.web.stdHtml(
            self._bottomHTML(),
            self.bottom._css + self._bottomCSS,
        loadCB=lambda x: self._showReaderButton())

    def _mungeQA(self, buf):
        #return mungeQA(self.mw.col, buf)   # <2.0.10
        #return self.mw.col.media.escapeImages(mungeQA(buf)) # >=2.0.10

        #将上述两个版本差异综合为
        txt = self.mw.col.media.escapeImages(buf)
        txt = stripSounds(txt)
        # osx webkit doesn't understand font weight 600
        txt = re.sub("font-weight: *600", "font-weight:bold", txt)
        return txt


    def _showQuestion(self):
        pass
    
    def _showReader(self):
        self._first=False
        self.state = "answer"
        self.typedAnswer = None
        c = self.card
        # grab the question and play audio
        if c.isEmpty():
            a = _("""\
The front of this card is empty. Please run Tools>Maintenance>Empty Cards.""")
        else:
            a = c.a()
        if (hasattr(self,"_autoplay") and self._autoplay(c)) or (hasattr(self,"autoplay") and self.autoplay(c)):   
            playFromText(a)
        # render & update bottom
        a = self._mungeQA(a)
        klass = "card card%d" % (c.ord+1)
        self.web.eval("_updateQA(%s, false, '%s');" % (json.dumps(a), klass))
        self._toggleStar()
        if self._bottomReady:
            self._showReaderButton()
        runHook('showReader')

    def _showAnswer(self):
        pass

    def _answerCard(self, ease):
        pass

    def _catchEsc(self, evt):
        pass

    def _showAnswerHack(self):
        pass
    
    def _showReaderHack(self):
        self.bottom.web.eval("py.link('nav3');")

    def _keyHandler(self, evt):
        key = unicode(evt.text())
        if (key == " " or evt.key() in (Qt.Key_Return, Qt.Key_Enter)):
            self._showReaderHack()
        elif key in ("1", "2", "3", "4"):
            self.nextCard(int(key))
        elif key == "5":
            self.autoPlay=(not self.autoPlay)
            self.nextCard(3)
        elif key == "6" and self.autoPlay:
            if self.speed<10:
                self.speed+=1
        elif key == "7" and self.autoPlay:
            if self.speed>1:
                self.speed-=1
        else:
            Reviewer._keyHandler(self, evt)

    def _linkHandler(self, url):
        if url.startswith("nav"): 
            key=int(url[3:])
            if key==5:
                self.autoPlay=(not self.autoPlay)
                self.nextCard(3)
            elif key==6 and self.autoPlay:
                if self.speed<10:
                    self.speed+=1
            elif key==7 and self.autoPlay:
                if self.speed>1:
                    self.speed-=1
            else:
                self.nextCard(key)
        else:
            Reviewer._linkHandler(self, url)

    def typeAnsFilter(self, buf):
        pass

    def typeAnsQuestionFilter(self, buf):
        pass

    def typeAnsAnswerFilter(self, buf):
        pass

    def _contentForCloze(self, txt, idx):
        pass

    def calculateOkBadStyle(self):
        pass

    def ok(self, a):
        pass

    def bad(self, a):
        pass

    def applyStyle(self, testChar, correct, wrong):
        pass

    def correct(self, a, b):
        pass

    def _bottomHTML(self):
        return """
<table width=100%% cellspacing=0 cellpadding=0>
<tr>
<td align=left width=50 valign=top class=stat>
<br>
<button title="%(editkey)s" onclick="py.link('edit');">%(edit)s</button></td>
<td align=center valign=top id=middle>
</td>
<td width=50 align=right valign=top class=stat><span id=time class=stattxt>
</span><br>
<button onclick="py.link('more');">%(more)s &#9662;</button>
</td>
</tr>
</table>
<script>
var time = 0;
var maxTime = 0;
$(function () {
updateTime();
setInterval(function () { time += 1; updateTime() }, 1000);
});

var updateTime = function () {
    if (!maxTime) {
        return;
    }
    if (maxTime == time) {
        py.link("nav3");
        time=0
    } 
}

function showReader(txt,maxTime_) {
  $("#middle")[0].innerHTML = txt;
  $("#defnav").focus();
  time = 0;
  maxTime = maxTime_;
}
</script>
""" % dict(edit=_("Edit"),
           editkey=_("Shortcut key: %s") % "E",
           more=_("More"), time=self.card.timeTaken()/1000)

    def _showAnswerButton(self):
        pass

    def _showReaderButton(self):
        self._bottomReady = True
        self.bottom.web.setFocus()

        default = '3' #默认焦点在“下一张”
        navButtonList=(('1', _("First")),('2', _("Previous"),), ('3', _("Next")), ('4', _("Last")), ('5',"<font color='green'><b>"+_("Play")+"</b></font>"))
        if self.autoPlay:
            navButtonList=(('5', "<font color='red'><b>"+_("Stop")+"</b></font>"), ('6', _("Slower")), ('7', _("Faster")))
        if self.readType=="task":
            default='n'
            navButtonList=(('n', _("Next Task")),)
            
        def but(i, label,text=""):
            if i == default:
                extra = "id=defnav"
            else:
                extra = ""
            return '''
<td  align=center>%s<br /><button %s title="%s" onclick='py.link("nav%s");'>\
%s</button></td>''' % (text,extra, _("Shortcut key: %s") % i, i, label)
        buf = "<table cellpading=0 cellspacing=0><tr>"
        for k, label in navButtonList:
            text=""
            if k=="1":
                text="1"
            elif k=="2" and self.curr_index>0:
                text=str(self.curr_index)
            elif k=="3" and self.curr_index<len(self.cards)-1:
                text=str(self.curr_index+2)
            elif k=="4":
                text=str(len(self.cards))
            elif self.autoPlay and k=="5":
                text=str(self.curr_index+1)
            buf += but(k, label,text)
        buf += "</tr></table>"
        script = """
<script>$(function () { $("#defnav").focus(); });</script>"""
        middle=buf + script
    
        self.bottom.web.eval("showReader(%s,%d);" % (json.dumps(middle),(self.speed if (self.autoPlay and self.readType!="task")  else 0)))

    def _showEaseButtons(self):
        pass

    def _remaining(self):
        return ""

    def _defaultEase(self):
        return 3

    def _answerButtonList(self):
        pass

    def _answerButtons(self):
        pass

    def _buttonTime(self, i):
        pass

    def onLeech(self, card):
        pass

    def save(self):
        if self.readType=="task":
            return
        
        if self.curr_cid==None and not self.deck.has_key("%s_cid"%self.readType):
            return
        if self.curr_cid==None:
            self.deck.pop("%s_cid"%self.readType)
        else:
            self.deck["%s_cid"%self.readType]=self.curr_cid
        self.mw.col.decks.update(self.deck)
        self.mw.col.decks.flush()
