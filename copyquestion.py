# -*- coding: utf-8 -*-

from aqt import mw
from anki.hooks import wrap, addHook, remHook
from aqt.qt import *
from aqt.utils import openHelp, showInfo

# auto copy question to clipboard
from aqt.reviewer import Reviewer

import win32clipboard

def onShowQuestion():
    card = mw.reviewer.card
    if not card:
        showInfo('Not in review now!')
        return

    word = card.note().values()[0].strip()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(word)
    win32clipboard.CloseClipboard()


addHook("showQuestion", onShowQuestion)
