# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import sys
import win32api
import win32con
import ui2 as main
import until
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon


class LOGIN_UI(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(517, 412)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.card = QtWidgets.QLineEdit(self.centralwidget)
        self.card.setObjectName("card")
        self.verticalLayout.addWidget(self.card)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 517, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(self.abcd)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "登录"))

    # 登陆成功0
    # 没有卡返回1
    # 超过两台设备2
    # 过期返回3
    def abcd(self):
        global res
        res = until.denglu(self.card.text(), until.get_baseboard_sn())
        if res == 0:
            widget2.show()
            widget.close()
        if res == 1:
            win32api.MessageBox(0, "卡不存在", "消息提示", win32con.MB_OK)
        if res == 2:
            win32api.MessageBox(0, "超过两台设备登录", "消息提示", win32con.MB_OK)
        if res == 3:
            win32api.MessageBox(0, "已经过期", "消息提示", win32con.MB_OK)


if __name__ == '__main__':
    sys.setrecursionlimit(10 ** 9)
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QMainWindow()
    widget2 = QtWidgets.QMainWindow()
    ui = LOGIN_UI()
    ui2 = main.Ui_MainWindow()
    ui.setupUi(widget)
    ui2.setupUi(widget2)
    widget.setWindowIcon(QIcon(until.get_resource_path('./pic/icon1.ico')))
    widget2.setWindowIcon(QIcon(until.get_resource_path('./pic/icon1.ico')))
    widget.show()
    sys.exit(app.exec_())