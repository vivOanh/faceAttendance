# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_qly_Sinhvien.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

from PyQt5.QtCore import Qt


class Ui_MainWindow(object):

    def __init__(self, idSubjectClass, nameSubject):
        self.idSubjectClass = idSubjectClass
        self.nameSubject = nameSubject



    def insertDataInTable(self, tablewidgetStudentInClass, tablewidgetStudentNotInClass):

        conn = sqlite3.connect('data.db')

        sqlSelectStudentInClass = "SELECT Sinhviens.maSV, hoDem, ten FROM Sinhviens INNER JOIN Lophocphan_Sinhviens " \
                                  "ON Sinhviens.maSV = Lophocphan_Sinhviens.maSV WHERE maLHP = '" + self.idSubjectClass + "';"
        sqlSelectStudentNotInClass = "SELECT DISTINCT Sinhviens.maSV, hoDem, ten FROM Sinhviens INNER JOIN Lophocphan_Sinhviens " \
                                     "ON Sinhviens.maSV = Lophocphan_Sinhviens.maSV WHERE NOT maLHP = '" + self.idSubjectClass + "';"

        resultStudentInClass = conn.execute(sqlSelectStudentInClass).fetchall()
        resultStudentNotInClass = conn.execute(sqlSelectStudentNotInClass).fetchall()


        conn.close()

        self.ds_svLhp.setRowCount(len(resultStudentInClass))
        for index_row, data_row in enumerate(resultStudentInClass):
            # print(index_row, data_row)
            for index_col, data_col in enumerate(data_row):
                # print(index_col, data_col)
                data = QtWidgets.QTableWidgetItem(str(data_col))
                data.setTextAlignment(Qt.AlignCenter)
                tablewidgetStudentInClass.setItem(index_row, index_col, data)

        self.ds_svchuathem.setRowCount(len(resultStudentNotInClass))
        for index_row, data_row in enumerate(resultStudentNotInClass):
            # print(index_row, data_row)
            for index_col, data_col in enumerate(data_row):
                # print(index_col, data_col)
                data = QtWidgets.QTableWidgetItem(str(data_col))
                data.setTextAlignment(Qt.AlignCenter)
                tablewidgetStudentNotInClass.setItem(index_row, index_col, data)

    def getStudentIdInClass(self):
        indexRow = self.ds_svLhp.currentRow()
        studentId = ""
        if indexRow == -1:
            indexRow = 0
        if self.ds_svLhp.rowCount():
            studentId = self.ds_svLhp.item(indexRow, 0).text()
        # print(studentId)
        return studentId

    def getStudentIdNotInClass(self):
        indexRow = self.ds_svchuathem.currentRow()
        if indexRow == -1:
            indexRow = 0
        studentId = self.ds_svchuathem.item(indexRow, 0).text()
        # print(studentId)
        return studentId

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1020, 531)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ds_svchuathem = QtWidgets.QTableWidget(self.centralwidget)
        self.ds_svchuathem.setGeometry(QtCore.QRect(10, 110, 450, 391))
        self.ds_svchuathem.setObjectName("ds_svchuathem")
        self.ds_svchuathem.setColumnCount(3)
        self.ds_svchuathem.setHorizontalHeaderLabels(['Mã sinh viên', 'Họ đệm', 'Tên'])
        self.ds_svchuathem.setColumnWidth(0, 110)
        self.ds_svchuathem.setColumnWidth(1, 200)
        self.ds_svchuathem.setColumnWidth(2, 100)


        self.ds_svLhp = QtWidgets.QTableWidget(self.centralwidget)
        self.ds_svLhp.setGeometry(QtCore.QRect(550, 110, 450, 391))
        self.ds_svLhp.setObjectName("ds_svLhp")
        self.ds_svLhp.setColumnCount(3)
        self.ds_svLhp.setHorizontalHeaderLabels(['Mã sinh viên', 'Họ đệm', 'Tên'])
        self.ds_svLhp.setColumnWidth(0, 110)
        self.ds_svLhp.setColumnWidth(1, 200)
        self.ds_svLhp.setColumnWidth(2, 100)


        self.btn_them = QtWidgets.QPushButton(self.centralwidget)
        self.btn_them.setGeometry(QtCore.QRect(460, 240, 90, 40))
        self.btn_them.setObjectName("btn_them")
        self.btn_xoa = QtWidgets.QPushButton(self.centralwidget)
        self.btn_xoa.setGeometry(QtCore.QRect(460, 300, 90, 40))
        self.btn_xoa.setObjectName("btn_xoa")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 60, 381, 40))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(550, 60, 381, 40))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 371, 30))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(460, 10, 431, 30))
        self.label_4.setObjectName("label_4")
        self.btn_thoat = QtWidgets.QPushButton(self.centralwidget)
        self.btn_thoat.setGeometry(QtCore.QRect(460, 370, 90, 40))
        self.btn_thoat.setObjectName("btn_thoat")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 893, 27))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # self.btn_xoa.clicked.connect(self.getStudentIdInClass)
        # self.btn_them.clicked.connect(self.getStudentIdNotInClass)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_them.setText(_translate("MainWindow", "Thêm >>"))
        self.btn_xoa.setText(_translate("MainWindow", "<<Xóa"))
        self.label.setText(_translate("MainWindow", "Danh sách sinh viên chưa có trong lớp học phần"))
        self.label_2.setText(_translate("MainWindow", "Danh sách sinh viên có trong lớp học phần"))
        self.label_3.setText(_translate("MainWindow", "Mã lớp học phần: "+self.idSubjectClass))
        self.label_4.setText(_translate("MainWindow", "Tên học phần: "+self.nameSubject))
        self.btn_thoat.setText(_translate("MainWindow", "Thoát"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow('201920503127001', 'Kỹ thuật lập trình')
    ui.setupUi(MainWindow)
    ui.insertDataInTable(ui.ds_svLhp, ui.ds_svchuathem)
    MainWindow.show()
    sys.exit(app.exec_())
