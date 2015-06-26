# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'table_interface.ui'
#
# Created: Fri Jun 26 16:22:35 2015
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

class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName(_fromUtf8("dialog"))
        dialog.resize(533, 300)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialog.sizePolicy().hasHeightForWidth())
        dialog.setSizePolicy(sizePolicy)
        self.verticalLayoutWidget = QtGui.QWidget(dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 511, 281))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableWidget_Zotero = QtGui.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget_Zotero.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidget_Zotero.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget_Zotero.setRowCount(0)
        self.tableWidget_Zotero.setColumnCount(5)
        self.tableWidget_Zotero.setObjectName(_fromUtf8("tableWidget_Zotero"))
        item = QtGui.QTableWidgetItem()
        self.tableWidget_Zotero.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_Zotero.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_Zotero.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_Zotero.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_Zotero.setHorizontalHeaderItem(4, item)
        self.verticalLayout.addWidget(self.tableWidget_Zotero)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_Save = QtGui.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Save.sizePolicy().hasHeightForWidth())
        self.pushButton_Save.setSizePolicy(sizePolicy)
        self.pushButton_Save.setObjectName(_fromUtf8("pushButton_Save"))
        self.horizontalLayout.addWidget(self.pushButton_Save)
        self.buttonBox = QtGui.QDialogButtonBox(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(_translate("dialog", "Literature Mapper", None))
        self.tableWidget_Zotero.setSortingEnabled(True)
        item = self.tableWidget_Zotero.horizontalHeaderItem(0)
        item.setText(_translate("dialog", "Key", None))
        item = self.tableWidget_Zotero.horizontalHeaderItem(1)
        item.setText(_translate("dialog", "Year", None))
        item = self.tableWidget_Zotero.horizontalHeaderItem(2)
        item.setText(_translate("dialog", "Author", None))
        item = self.tableWidget_Zotero.horizontalHeaderItem(3)
        item.setText(_translate("dialog", "Title", None))
        item = self.tableWidget_Zotero.horizontalHeaderItem(4)
        item.setText(_translate("dialog", "Geometry", None))
        self.pushButton_Save.setToolTip(_translate("dialog", "Send Changes to Zotero", None))
        self.pushButton_Save.setText(_translate("dialog", "Save to Zotero", None))

