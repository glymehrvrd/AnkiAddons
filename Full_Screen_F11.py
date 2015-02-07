# -*- coding: utf-8 -*-
# Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# This plugin adds the ability to toggle full screen mode. It adds an item to
# the tools menu.
#

from aqt import mw
from PyQt4.QtGui import *
from PyQt4.QtCore import *


def onFullScreen():
    mw.setWindowState(mw.windowState() ^ Qt.WindowFullScreen)

action = QAction("Full Screen", mw)
mw.connect(action, SIGNAL("triggered()"), onFullScreen)
action.setShortcut("F11")

mw.form.menuTools.addAction(action)
