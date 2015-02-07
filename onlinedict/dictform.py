# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dictform.ui'
#
# Created: Fri Aug 16 12:58:49 2013
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_OnlineDict(object):

    def setupUi(self, OnlineDict):
        OnlineDict.setObjectName(_fromUtf8("OnlineDict"))
        OnlineDict.setWindowModality(QtCore.Qt.WindowModal)
        OnlineDict.resize(698, 524)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            OnlineDict.sizePolicy().hasHeightForWidth())
        OnlineDict.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtGui.QVBoxLayout(OnlineDict)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textBrowser = QtGui.QTextBrowser(OnlineDict)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.gridLayout.addWidget(self.textBrowser, 4, 0, 1, 3)
        self.label = QtGui.QLabel(OnlineDict)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(OnlineDict)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout.addWidget(self.comboBox, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)

        self.retranslateUi(OnlineDict)
        QtCore.QMetaObject.connectSlotsByName(OnlineDict)

    def retranslateUi(self, OnlineDict):
        OnlineDict.setWindowTitle(_translate("OnlineDict", "Dialog", None))
        self.label.setText(_translate("OnlineDict", "Dictionary:", None))
