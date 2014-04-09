# -*- coding: utf-8 -*-

from aqt import mw
from anki.hooks import wrap,addHook,remHook
from aqt.qt import *
from aqt.utils import openHelp, showInfo

# change defaultease to the highest memory state
from aqt.reviewer import Reviewer

def _mydefaultEase(self):
    return self.mw.col.sched.answerButtons(self.card)
Reviewer._defaultEase = _mydefaultEase

# define a new hotkey to answer with the highest memry state
saShortcut=QShortcut(QKeySequence("6"), mw)

def onSmartAnswer():
    card = mw.reviewer.card
    if not card:
        showInfo('Not in review now!')
        return
    easebutton = mw.col.sched.answerButtons(card)
    mw.reviewer._answerCard(easebutton)

def load():
    saShortcut.connect(saShortcut, SIGNAL("activated()"), onSmartAnswer)

def unload():
    saShortcut.disconnect(saShortcut, SIGNAL("activated()"), onSmartAnswer)

load()