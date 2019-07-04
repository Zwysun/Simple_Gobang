# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'game_begin.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_gamebegin(object):
    def setupUi(self, gamebegin):
        gamebegin.setObjectName("gamebegin")
        gamebegin.setWindowModality(QtCore.Qt.NonModal)
        gamebegin.setEnabled(True)
        gamebegin.resize(400, 300)
        gamebegin.setMinimumSize(QtCore.QSize(400, 300))
        gamebegin.setMaximumSize(QtCore.QSize(400, 300))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(10)
        gamebegin.setFont(font)
        self.AI = QtWidgets.QPushButton(gamebegin)
        self.AI.setGeometry(QtCore.QRect(30, 190, 131, 71))
        self.AI.setObjectName("AI")
        self.label = QtWidgets.QLabel(gamebegin)
        self.label.setGeometry(QtCore.QRect(90, 40, 241, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(gamebegin)
        self.label_2.setGeometry(QtCore.QRect(140, 120, 141, 41))
        self.label_2.setObjectName("label_2")
        self.human = QtWidgets.QPushButton(gamebegin)
        self.human.setGeometry(QtCore.QRect(230, 190, 131, 71))
        self.human.setObjectName("human")

        self.retranslateUi(gamebegin)
        QtCore.QMetaObject.connectSlotsByName(gamebegin)

    def retranslateUi(self, gamebegin):
        _translate = QtCore.QCoreApplication.translate
        gamebegin.setWindowTitle(_translate("gamebegin", "五子棋"))
        self.AI.setText(_translate("gamebegin", "人机对战"))
        self.label.setText(_translate("gamebegin", "欢 迎 使 用 五 子 棋"))
        self.label_2.setText(_translate("gamebegin", "请选择游戏模式"))
        self.human.setText(_translate("gamebegin", "局域网联机"))

