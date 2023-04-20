# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_add_subject.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 533)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lb_title = QtWidgets.QLabel(self.centralwidget)
        self.lb_title.setGeometry(QtCore.QRect(0, 10, 700, 60))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lb_title.setFont(font)
        self.lb_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_title.setObjectName("lb_title")
        self.lb_mhp = QtWidgets.QLabel(self.centralwidget)
        self.lb_mhp.setGeometry(QtCore.QRect(90, 100, 180, 35))
        self.lb_mhp.setObjectName("lb_mhp")
        self.lb_thp = QtWidgets.QLabel(self.centralwidget)
        self.lb_thp.setGeometry(QtCore.QRect(90, 180, 180, 35))
        self.lb_thp.setObjectName("lb_thp")
        self.lb_stc = QtWidgets.QLabel(self.centralwidget)
        self.lb_stc.setGeometry(QtCore.QRect(90, 260, 180, 35))
        self.lb_stc.setObjectName("lb_stc")
        self.lb_hkd = QtWidgets.QLabel(self.centralwidget)
        self.lb_hkd.setGeometry(QtCore.QRect(90, 340, 180, 35))
        self.lb_hkd.setObjectName("lb_hkd")
        self.ip_mahocphan = QtWidgets.QLineEdit(self.centralwidget)
        self.ip_mahocphan.setGeometry(QtCore.QRect(70, 140, 500, 35))
        self.ip_mahocphan.setObjectName("ip_mahocphan")
        self.ip_tenhocphan = QtWidgets.QLineEdit(self.centralwidget)
        self.ip_tenhocphan.setGeometry(QtCore.QRect(70, 220, 500, 35))
        self.ip_tenhocphan.setObjectName("ip_tenhocphan")
        self.ip_sotinchi = QtWidgets.QLineEdit(self.centralwidget)
        self.ip_sotinchi.setGeometry(QtCore.QRect(70, 300, 500, 35))
        self.ip_sotinchi.setObjectName("ip_sotinchi")
        self.ip_hockyday = QtWidgets.QLineEdit(self.centralwidget)
        self.ip_hockyday.setGeometry(QtCore.QRect(70, 380, 500, 35))
        self.ip_hockyday.setObjectName("ip_hockyday")
        self.btn_themhocphan = QtWidgets.QPushButton(self.centralwidget)
        self.btn_themhocphan.setGeometry(QtCore.QRect(220, 440, 251, 51))
        self.btn_themhocphan.setObjectName("btn_themhocphan")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 27))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lb_title.setText(_translate("MainWindow", "THÊM HỌC PHẦN"))
        self.lb_mhp.setText(_translate("MainWindow", "Mã học phần"))
        self.lb_thp.setText(_translate("MainWindow", "Tên học phần"))
        self.lb_stc.setText(_translate("MainWindow", "Số tín chỉ"))
        self.lb_hkd.setText(_translate("MainWindow", "Học kì dạy"))
        self.btn_themhocphan.setText(_translate("MainWindow", "Thêm học phần"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())