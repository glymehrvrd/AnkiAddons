# -*- coding: utf-8 -*-

from aqt import mw
from anki.hooks import wrap, addHook, remHook
from aqt.qt import *
from aqt.utils import openHelp, showInfo

# change defaultease to the highest memory state
from aqt.reviewer import Reviewer
import subprocess

# define a new hotkey to answer with the highest memry state
saShortcut = QShortcut(QKeySequence("c"), mw)


def onFastTranslate():
    p = subprocess.Popen(['xclip', '-i'], stdin=subprocess.PIPE)
    p.communicate(mw.reviewer.card.note().fields[0])


def load():
    saShortcut.connect(saShortcut, SIGNAL("activated()"), onFastTranslate)


def unload():
    saShortcut.disconnect(saShortcut, SIGNAL("activated()"), onFastTranslate)

load()
