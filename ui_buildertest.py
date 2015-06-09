# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'literature_mapper_dialog_base.ui'
#
# Created: Tue Jun 09 12:00:40 2015
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

class Ui_LiteratureMapperDialogBase(object):
    def setupUi(self, LiteratureMapperDialogBase):
        LiteratureMapperDialogBase.setObjectName(_fromUtf8("LiteratureMapperDialogBase"))
        LiteratureMapperDialogBase.resize(348, 304)
        self.button_box = QtGui.QDialogButtonBox(LiteratureMapperDialogBase)
        self.button_box.setGeometry(QtCore.QRect(-50, 220, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setObjectName(_fromUtf8("button_box"))
        self.lineEdit_APIKey = QtGui.QLineEdit(LiteratureMapperDialogBase)
        self.lineEdit_APIKey.setGeometry(QtCore.QRect(30, 50, 261, 20))
        self.lineEdit_APIKey.setObjectName(_fromUtf8("lineEdit_APIKey"))
        self.lineEdit_UserID = QtGui.QLineEdit(LiteratureMapperDialogBase)
        self.lineEdit_UserID.setGeometry(QtCore.QRect(30, 110, 261, 20))
        self.lineEdit_UserID.setObjectName(_fromUtf8("lineEdit_UserID"))
        self.label = QtGui.QLabel(LiteratureMapperDialogBase)
        self.label.setGeometry(QtCore.QRect(30, 30, 46, 13))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(LiteratureMapperDialogBase)
        self.label_2.setGeometry(QtCore.QRect(30, 90, 121, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lineEdit_CollectionKey = QtGui.QLineEdit(LiteratureMapperDialogBase)
        self.lineEdit_CollectionKey.setGeometry(QtCore.QRect(30, 170, 261, 20))
        self.lineEdit_CollectionKey.setObjectName(_fromUtf8("lineEdit_CollectionKey"))
        self.label_3 = QtGui.QLabel(LiteratureMapperDialogBase)
        self.label_3.setGeometry(QtCore.QRect(30, 150, 121, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.retranslateUi(LiteratureMapperDialogBase)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), LiteratureMapperDialogBase.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), LiteratureMapperDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(LiteratureMapperDialogBase)

    def retranslateUi(self, LiteratureMapperDialogBase):
        LiteratureMapperDialogBase.setWindowTitle(_translate("LiteratureMapperDialogBase", "Literature Mapper", None))
        self.label.setText(_translate("LiteratureMapperDialogBase", "API Key", None))
        self.label_2.setText(_translate("LiteratureMapperDialogBase", "User or Group ID", None))
        self.label_3.setText(_translate("LiteratureMapperDialogBase", "Collection Key", None))

