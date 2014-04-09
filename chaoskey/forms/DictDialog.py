# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\DictDialog.ui'
#
# Created: Mon May 13 16:44:53 2013
#      by: PyQt4 UI code generator 4.10
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
        return _(text)
except AttributeError:
    def _translate(context, text, disambig):
        return _(text)

class Ui_DictDialog(object):
    def setupUi(self, DictDialog):
        DictDialog.setObjectName(_fromUtf8("DictDialog"))
        DictDialog.resize(490, 260)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DictDialog.sizePolicy().hasHeightForWidth())
        DictDialog.setSizePolicy(sizePolicy)
        DictDialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.verticalLayout = QtGui.QVBoxLayout(DictDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.queryFrame = QtGui.QFrame(DictDialog)
        self.queryFrame.setMaximumSize(QtCore.QSize(16777215, 43))
        self.queryFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.queryFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.queryFrame.setObjectName(_fromUtf8("queryFrame"))
        self.horizontalLayout2 = QtGui.QHBoxLayout(self.queryFrame)
        self.horizontalLayout2.setObjectName(_fromUtf8("horizontalLayout2"))
        self.wordEdit = QtGui.QLineEdit(self.queryFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wordEdit.sizePolicy().hasHeightForWidth())
        self.wordEdit.setSizePolicy(sizePolicy)
        self.wordEdit.setMinimumSize(QtCore.QSize(250, 0))
        self.wordEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.wordEdit.setBaseSize(QtCore.QSize(0, 0))
        self.wordEdit.setMaxLength(1200)
        self.wordEdit.setObjectName(_fromUtf8("wordEdit"))
        self.horizontalLayout2.addWidget(self.wordEdit)
        self.queryButton = QtGui.QPushButton(self.queryFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.queryButton.sizePolicy().hasHeightForWidth())
        self.queryButton.setSizePolicy(sizePolicy)
        self.queryButton.setMaximumSize(QtCore.QSize(40, 16777215))
        self.queryButton.setObjectName(_fromUtf8("queryButton"))
        self.horizontalLayout2.addWidget(self.queryButton)
        self.dictLabel = QtGui.QLabel(self.queryFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dictLabel.sizePolicy().hasHeightForWidth())
        self.dictLabel.setSizePolicy(sizePolicy)
        self.dictLabel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.dictLabel.setObjectName(_fromUtf8("dictLabel"))
        self.horizontalLayout2.addWidget(self.dictLabel)
        self.dictEngine = QtGui.QComboBox(self.queryFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dictEngine.sizePolicy().hasHeightForWidth())
        self.dictEngine.setSizePolicy(sizePolicy)
        self.dictEngine.setMinimumSize(QtCore.QSize(120, 0))
        self.dictEngine.setStyleSheet(_fromUtf8("background-color: rgb(243, 243, 243);"))
        self.dictEngine.setObjectName(_fromUtf8("dictEngine"))
        self.horizontalLayout2.addWidget(self.dictEngine)
        self.verticalLayout.addWidget(self.queryFrame)
        self.mappingGroup = QtGui.QGroupBox(DictDialog)
        self.mappingGroup.setObjectName(_fromUtf8("mappingGroup"))
        self.horizontalLayout3 = QtGui.QHBoxLayout(self.mappingGroup)
        self.horizontalLayout3.setObjectName(_fromUtf8("horizontalLayout3"))
        self.mappingArea = QtGui.QVBoxLayout()
        self.mappingArea.setObjectName(_fromUtf8("mappingArea"))
        self.horizontalLayout3.addLayout(self.mappingArea)
        self.mergeButton = QtGui.QPushButton(self.mappingGroup)
        self.mergeButton.setMaximumSize(QtCore.QSize(80, 16777215))
        self.mergeButton.setDefault(False)
        self.mergeButton.setObjectName(_fromUtf8("mergeButton"))
        self.horizontalLayout3.addWidget(self.mergeButton)
        self.verticalLayout.addWidget(self.mappingGroup)
        self.dictGroup = QtGui.QGroupBox(DictDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dictGroup.sizePolicy().hasHeightForWidth())
        self.dictGroup.setSizePolicy(sizePolicy)
        self.dictGroup.setObjectName(_fromUtf8("dictGroup"))
        self.horizontalLayout1 = QtGui.QHBoxLayout(self.dictGroup)
        self.horizontalLayout1.setObjectName(_fromUtf8("horizontalLayout1"))
        self.dictHtml = QtGui.QTextBrowser(self.dictGroup)
        self.dictHtml.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.dictHtml.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.dictHtml.setObjectName(_fromUtf8("dictHtml"))
        self.horizontalLayout1.addWidget(self.dictHtml)
        self.verticalLayout.addWidget(self.dictGroup)
        self.buttonBox = QtGui.QDialogButtonBox(DictDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Help)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.dictLabel.setBuddy(self.dictEngine)

        self.retranslateUi(DictDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DictDialog.reject)
        QtCore.QObject.connect(self.wordEdit, QtCore.SIGNAL(_fromUtf8("returnPressed()")), DictDialog.onQuery)
        QtCore.QObject.connect(self.queryButton, QtCore.SIGNAL(_fromUtf8("clicked()")), DictDialog.onQuery)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("helpRequested()")), DictDialog.helpRequested)
        QtCore.QObject.connect(self.mergeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), DictDialog.doMerge)
        QtCore.QMetaObject.connectSlotsByName(DictDialog)
        DictDialog.setTabOrder(self.wordEdit, self.queryButton)
        DictDialog.setTabOrder(self.queryButton, self.dictEngine)
        DictDialog.setTabOrder(self.dictEngine, self.mergeButton)
        DictDialog.setTabOrder(self.mergeButton, self.dictHtml)
        DictDialog.setTabOrder(self.dictHtml, self.buttonBox)

    def retranslateUi(self, DictDialog):
        DictDialog.setWindowTitle(_translate("DictDialog", "Online Dict", None))
        self.queryButton.setText(_translate("DictDialog", "Query", None))
        self.dictLabel.setText(_translate("DictDialog", "Dict", None))
        self.mappingGroup.setTitle(_translate("DictDialog", "Field mapping", None))
        self.mergeButton.setText(_translate("DictDialog", "&Merge", None))
        self.dictGroup.setTitle(_translate("DictDialog", "Online Dict", None))
        self.dictHtml.setHtml(_translate("DictDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))

