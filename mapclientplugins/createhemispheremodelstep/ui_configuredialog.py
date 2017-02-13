# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/configuredialog.ui'
#
# Created: Mon Feb 13 15:39:28 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ConfigureDialog(object):
    def setupUi(self, ConfigureDialog):
        ConfigureDialog.setObjectName("ConfigureDialog")
        ConfigureDialog.resize(418, 303)
        self.gridLayout = QtGui.QGridLayout(ConfigureDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.configGroupBox = QtGui.QGroupBox(ConfigureDialog)
        self.configGroupBox.setTitle("")
        self.configGroupBox.setObjectName("configGroupBox")
        self.formLayout = QtGui.QFormLayout(self.configGroupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label0 = QtGui.QLabel(self.configGroupBox)
        self.label0.setObjectName("label0")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label0)
        self.lineEdit0 = QtGui.QLineEdit(self.configGroupBox)
        self.lineEdit0.setObjectName("lineEdit0")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit0)
        self.label = QtGui.QLabel(self.configGroupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.elementsAroundLineEdit = QtGui.QLineEdit(self.configGroupBox)
        self.elementsAroundLineEdit.setObjectName("elementsAroundLineEdit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.elementsAroundLineEdit)
        self.elementsUpLineEdit = QtGui.QLineEdit(self.configGroupBox)
        self.elementsUpLineEdit.setObjectName("elementsUpLineEdit")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.elementsUpLineEdit)
        self.elementsAlongStemLineEdit = QtGui.QLineEdit(self.configGroupBox)
        self.elementsAlongStemLineEdit.setObjectName("elementsAlongStemLineEdit")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.elementsAlongStemLineEdit)
        self.radiusLineEdit = QtGui.QLineEdit(self.configGroupBox)
        self.radiusLineEdit.setEnabled(False)
        self.radiusLineEdit.setObjectName("radiusLineEdit")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.radiusLineEdit)
        self.stemLengthLineEdit = QtGui.QLineEdit(self.configGroupBox)
        self.stemLengthLineEdit.setEnabled(False)
        self.stemLengthLineEdit.setObjectName("stemLengthLineEdit")
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.stemLengthLineEdit)
        self.label_2 = QtGui.QLabel(self.configGroupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtGui.QLabel(self.configGroupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtGui.QLabel(self.configGroupBox)
        self.label_4.setEnabled(False)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtGui.QLabel(self.configGroupBox)
        self.label_5.setEnabled(False)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_5)
        self.gridLayout.addWidget(self.configGroupBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ConfigureDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(ConfigureDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ConfigureDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ConfigureDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ConfigureDialog)

    def retranslateUi(self, ConfigureDialog):
        ConfigureDialog.setWindowTitle(QtGui.QApplication.translate("ConfigureDialog", "ConfigureDialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label0.setText(QtGui.QApplication.translate("ConfigureDialog", "identifier:  ", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ConfigureDialog", "#Elements Around:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ConfigureDialog", "#Elements Up:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ConfigureDialog", "#Element Along Stem:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ConfigureDialog", "Radius:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("ConfigureDialog", "Stem Length:", None, QtGui.QApplication.UnicodeUTF8))

