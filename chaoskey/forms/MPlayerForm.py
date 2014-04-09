# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\MPlayerForm.ui'
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

class Ui_mplayerForm(object):
    def setupUi(self, mplayerForm):
        mplayerForm.setObjectName(_fromUtf8("mplayerForm"))
        mplayerForm.resize(400, 293)
        self.verticalLayout = QtGui.QVBoxLayout(mplayerForm)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.mplayerFrame = QtGui.QFrame(mplayerForm)
        self.mplayerFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.mplayerFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.mplayerFrame.setObjectName(_fromUtf8("mplayerFrame"))
        self.verticalLayout.addWidget(self.mplayerFrame)
        self.seekSlider = QtGui.QSlider(mplayerForm)
        self.seekSlider.setOrientation(QtCore.Qt.Horizontal)
        self.seekSlider.setObjectName(_fromUtf8("seekSlider"))
        self.verticalLayout.addWidget(self.seekSlider)
        self.controlFrame = QtGui.QFrame(mplayerForm)
        self.controlFrame.setMaximumSize(QtCore.QSize(16777215, 50))
        self.controlFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.controlFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.controlFrame.setObjectName(_fromUtf8("controlFrame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.controlFrame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.playButton = QtGui.QPushButton(self.controlFrame)
        self.playButton.setObjectName(_fromUtf8("playButton"))
        self.horizontalLayout.addWidget(self.playButton)
        self.pauseButton = QtGui.QPushButton(self.controlFrame)
        self.pauseButton.setObjectName(_fromUtf8("pauseButton"))
        self.horizontalLayout.addWidget(self.pauseButton)
        self.stopButton = QtGui.QPushButton(self.controlFrame)
        self.stopButton.setObjectName(_fromUtf8("stopButton"))
        self.horizontalLayout.addWidget(self.stopButton)
        self.muteButton = QtGui.QPushButton(self.controlFrame)
        self.muteButton.setObjectName(_fromUtf8("muteButton"))
        self.horizontalLayout.addWidget(self.muteButton)
        self.volumeSlider = QtGui.QSlider(self.controlFrame)
        self.volumeSlider.setMaximumSize(QtCore.QSize(50, 16777215))
        self.volumeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeSlider.setObjectName(_fromUtf8("volumeSlider"))
        self.horizontalLayout.addWidget(self.volumeSlider)
        self.verticalLayout.addWidget(self.controlFrame)

        self.retranslateUi(mplayerForm)
        QtCore.QObject.connect(self.playButton, QtCore.SIGNAL(_fromUtf8("clicked()")), mplayerForm.playPlayer)
        QtCore.QObject.connect(self.pauseButton, QtCore.SIGNAL(_fromUtf8("clicked()")), mplayerForm.pausePlayer)
        QtCore.QObject.connect(self.stopButton, QtCore.SIGNAL(_fromUtf8("clicked()")), mplayerForm.stopPlayer)
        QtCore.QObject.connect(self.seekSlider, QtCore.SIGNAL(_fromUtf8("sliderMoved(int)")), mplayerForm.seekSliderMoved)
        QtCore.QObject.connect(self.volumeSlider, QtCore.SIGNAL(_fromUtf8("sliderMoved(int)")), mplayerForm.volumeSliderMoved)
        QtCore.QObject.connect(self.muteButton, QtCore.SIGNAL(_fromUtf8("clicked()")), mplayerForm.mutePlayer)
        QtCore.QMetaObject.connectSlotsByName(mplayerForm)

    def retranslateUi(self, mplayerForm):
        mplayerForm.setWindowTitle(_translate("mplayerForm", "Form", None))
        self.playButton.setText(_translate("mplayerForm", "play", None))
        self.pauseButton.setText(_translate("mplayerForm", "pause", None))
        self.stopButton.setText(_translate("mplayerForm", "stop", None))
        self.muteButton.setText(_translate("mplayerForm", "mute", None))

