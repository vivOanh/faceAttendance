# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_fix_subjectclass.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

from PyQt5.QtCore import Qt


class Ui_MainWindow(object):

    def __init__(self, idSubjectClass, nameSubject, nameTeacher):
        self.idSubjectClass = idSubjectClass
        self.nameSubjectClass = {}
        self.nameTeacher = {}
        conn = sqlite3.connect('data.db')
        sql_select_name_subject_class = "SELECT tenHP, maHP FROM Hocphans"
        self.nameSubjectClass = conn.execute(sql_select_name_subject_class).fetchall()
        self.nameSubjectClass = dict((key, val) for key, val in self.nameSubjectClass)

        sql_select_name_teacher = "SELECT hoTenGV, maGV FROM Taikhoans WHERE quyen = 'us'"
        self.nameTeacher = conn.execute(sql_select_name_teacher).fetchall()
        self.nameTeacher = dict((key, val) for key, val in self.nameTeacher)

        self.indexSubjectClass = None
        for index, key in enumerate(self.nameSubjectClass):
            if key == nameSubject:
                self.indexSubjectClass = index

        self.indexNameTeacher = None
        for index, key in enumerate(self.nameTeacher):
            if key == nameTeacher:
                self.indexNameTeacher = index

        conn.close()

    def getData(self):
        idSubjectClass = self.ip_maLHP.text()
        subjectName = self.cbox_tenHP.currentData(0)
        teacherName = self.cbox_tenGV.currentData(0)
        # print(idSubjectClass, self.nameSubjectClass[subjectName], self.nameTeacher[teacherName])
        return idSubjectClass, self.nameSubjectClass[subjectName], self.nameTeacher[teacherName]

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 500)
        MainWindow.setMaximumSize(QtCore.QSize(800, 500))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.cbox_tenHP = QtWidgets.QComboBox(self.centralwidget)
        self.cbox_tenHP.setGeometry(QtCore.QRect(210, 210, 500, 40))
        self.cbox_tenHP.setObjectName("cbox_tenHP")
        for index, keyval in enumerate(self.nameSubjectClass):
            self.cbox_tenHP.insertItem(index, keyval)
        self.cbox_tenHP.setCurrentIndex(self.indexSubjectClass)

        self.ip_maLHP = QtWidgets.QLineEdit(self.centralwidget)
        self.ip_maLHP.setGeometry(QtCore.QRect(210, 120, 500, 40))
        self.ip_maLHP.setObjectName("ip_maLHP")
        self.ip_maLHP.setText(self.idSubjectClass)
        self.ip_maLHP.setFocusPolicy(Qt.NoFocus)

        self.cbox_tenGV = QtWidgets.QComboBox(self.centralwidget)
        self.cbox_tenGV.setGeometry(QtCore.QRect(210, 300, 500, 40))
        self.cbox_tenGV.setObjectName("cbox_tenGV")
        for index, keyval in enumerate(self.nameTeacher):
            self.cbox_tenGV.insertItem(index, keyval)
        self.cbox_tenGV.setCurrentIndex(self.indexNameTeacher)

        self.lb_malhp = QtWidgets.QLabel(self.centralwidget)
        self.lb_malhp.setGeometry(QtCore.QRect(30, 120, 160, 40))
        self.lb_malhp.setObjectName("lb_malhp")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 210, 160, 40))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 300, 160, 40))
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 20, 800, 60))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.btn_suaLHP = QtWidgets.QPushButton(self.centralwidget)
        self.btn_suaLHP.setGeometry(QtCore.QRect(280, 380, 200, 50))
        self.btn_suaLHP.setObjectName("btn_suaLHP")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 27))
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
        self.lb_malhp.setText(_translate("MainWindow", "Mã lớp học phần"))
        self.label_2.setText(_translate("MainWindow", "Tên học phần"))
        self.label_3.setText(_translate("MainWindow", "Mã giáo viên"))
        self.label.setText(_translate("MainWindow", "SỬA THÔNG TIN  LỚP HỌC PHẦN"))
        self.btn_suaLHP.setText(_translate("MainWindow", "Sửa"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow('20221IT6021007', 'Cơ sở dữ liệu', 'Vi Văn Oanh')
    ui.setupUi(MainWindow)
    ui.getData()
    MainWindow.show()
    sys.exit(app.exec_())
