# import the main window object (mw) from ankiqt
from aqt import mw
# import all of the Qt GUI library
from aqt.qt import *

import sys
import os
modulespath = os.path.dirname(__file__) + os.sep + "onlinedict"
sys.path.insert(0, modulespath)

import onlinedict.dictmain
