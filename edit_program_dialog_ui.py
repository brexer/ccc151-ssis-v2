# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit_program_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_editProgramDialog(object):
    def setupUi(self, editProgramDialog):
        if not editProgramDialog.objectName():
            editProgramDialog.setObjectName(u"editProgramDialog")
        editProgramDialog.resize(300, 190)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(editProgramDialog.sizePolicy().hasHeightForWidth())
        editProgramDialog.setSizePolicy(sizePolicy)
        editProgramDialog.setMinimumSize(QSize(300, 190))
        editProgramDialog.setMaximumSize(QSize(300, 190))
        editProgramDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(editProgramDialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(editProgramDialog)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_11 = QFrame(self.widget)
        self.frame_11.setObjectName(u"frame_11")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(2)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_11.sizePolicy().hasHeightForWidth())
        self.frame_11.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setFamilies([u"Verdana"])
        self.frame_11.setFont(font)
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.dialog_comboBox_4 = QComboBox(self.frame_11)
        self.dialog_comboBox_4.setObjectName(u"dialog_comboBox_4")
        self.dialog_comboBox_4.setGeometry(QRect(110, 90, 91, 31))
        self.dialog_lineEdit_7 = QLineEdit(self.frame_11)
        self.dialog_lineEdit_7.setObjectName(u"dialog_lineEdit_7")
        self.dialog_lineEdit_7.setGeometry(QRect(110, 50, 161, 31))
        self.dialog_lineEdit_6 = QLineEdit(self.frame_11)
        self.dialog_lineEdit_6.setObjectName(u"dialog_lineEdit_6")
        self.dialog_lineEdit_6.setGeometry(QRect(110, 10, 161, 31))
        self.label_27 = QLabel(self.frame_11)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setGeometry(QRect(10, 10, 101, 31))
        font1 = QFont()
        font1.setFamilies([u"Verdana"])
        font1.setPointSize(10)
        self.label_27.setFont(font1)
        self.label_28 = QLabel(self.frame_11)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setGeometry(QRect(10, 50, 101, 31))
        self.label_28.setFont(font1)
        self.label_35 = QLabel(self.frame_11)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setGeometry(QRect(10, 90, 101, 31))
        self.label_35.setFont(font1)
        self.editProgramButton = QPushButton(self.frame_11)
        self.editProgramButton.setObjectName(u"editProgramButton")
        self.editProgramButton.setGeometry(QRect(160, 130, 111, 31))
        font2 = QFont()
        font2.setFamilies([u"Verdana"])
        font2.setPointSize(10)
        font2.setBold(True)
        self.editProgramButton.setFont(font2)

        self.verticalLayout_2.addWidget(self.frame_11)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(editProgramDialog)

        QMetaObject.connectSlotsByName(editProgramDialog)
    # setupUi

    def retranslateUi(self, editProgramDialog):
        editProgramDialog.setWindowTitle(QCoreApplication.translate("editProgramDialog", u"Edit Program", None))
        self.label_27.setText(QCoreApplication.translate("editProgramDialog", u"Program Code", None))
        self.label_28.setText(QCoreApplication.translate("editProgramDialog", u"Program Name", None))
        self.label_35.setText(QCoreApplication.translate("editProgramDialog", u"College Code", None))
        self.editProgramButton.setText(QCoreApplication.translate("editProgramDialog", u"Edit Program", None))
    # retranslateUi

