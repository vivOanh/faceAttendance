from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import sqlite3
import sys
import pandas as pd
import time

from PyQt5.QtWidgets import QFileDialog


class Ui_MainWindow(object):
    def __init__(self, ma_lhp, teacher_name, subject_name):
        self.col = 0
        self.row = 0

        self.maLHP = ma_lhp
        self.teacher_name = teacher_name
        self.subject_name = subject_name

        self.conn = sqlite3.connect("data.db")
        self.list_lable = ['Mã sinh viên', 'Họ đệm', 'Tên']

        sql_select_day = "SELECT ngayHoc FROM Thoikhoabieu_Lophocphans WHERE maLHP = '" + str(self.maLHP)+"';"
        sql_select_sinhviens = "SELECT Sinhviens.maSV, hoDem, ten FROM Sinhviens  INNER JOIN Lophocphan_Sinhviens ON " \
                               "Sinhviens.maSV = Lophocphan_Sinhviens.maSV WHERE Lophocphan_Sinhviens.maLHP = '"+str(self.maLHP)+"' " \
                                "ORDER BY ten;"
        # self.thongtin_diemdanh = conn.execute(sql_select_sinhviens)
        cursor_day = self.conn.execute(sql_select_day)
        self.list_day = []
        for item in cursor_day:
            self.list_day.append(item[0])
            self.list_lable.append(item[0])
        self.list_lable.append("Số tiết nghỉ")
        labelsInDF = self.list_day
        # labelsInDF.append("Tổng số tiết nghỉ")
        # print(self.list_lable)

        sql_count_studentsInClass = "SELECT maSV FROM Lophocphan_Sinhviens WHERE maLHP = '"+str(self.maLHP)+"';"
        cursor_numRow = self.conn.execute(sql_count_studentsInClass)
        self.col = len(self.list_lable)
        self.row = len(cursor_numRow.fetchall())

        self.df = pd.read_sql(sql_select_sinhviens, self.conn, index_col='maSV')
        for item in labelsInDF:
            self.df[item] = None

        sql_tiet_hoc = "SELECT tietHoc FROM Thoikhoabieu_Lophocphans WHERE maLHP = '" + self.maLHP + "';"
        tiet_hoc = self.conn.execute(sql_tiet_hoc).fetchone()[0]
        so_tiet_1_buoi = len(tiet_hoc.split(","))

    #   Đánh số đi học
        for number_index, index in enumerate(self.df.index):
            for number_columns, columns in enumerate(self.df.columns):
                sql_check_attendance = "SELECT maSV, ngayHoc FROM Diemdanhs WHERE maLHP = '" + str(self.maLHP) + "'" \
                        " AND maSV = '" + index + "' AND ngayHoc = '" + columns + "' AND diemdanh = 'x';"
                idAndDate = self.conn.execute(sql_check_attendance)
                # print(idAndDate.fetchone())
                if not idAndDate.fetchone() and columns in labelsInDF:
                    # print(index, columns)
                    self.df.loc[index, columns] = str(so_tiet_1_buoi)+'k'

        if len(self.conn.execute(sql_tiet_hoc).fetchall()):

            list_stn = []
            for index in self.df.index:
                so_buoi_nghi = 0
                for data_col in labelsInDF:
                    if self.df.loc[index, data_col] != None:
                        so_buoi_nghi += 1
                list_stn.append(str(so_tiet_1_buoi * so_buoi_nghi))
            self.df["Tổng số tiết nghỉ"] = list_stn

        self.conn.close()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 600)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 120, 1350, 500))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(self.row)
        self.tableWidget.setColumnCount(self.col)
        self.tableWidget.setHorizontalHeaderLabels(self.list_lable)

        self.tableWidget.setColumnWidth(0, 120)
        self.tableWidget.setColumnWidth(1, 180)

        for i in range(3, self.col - 1):
            self.tableWidget.setColumnWidth(i, 50)

        self.label_malophocphan = QtWidgets.QLabel(self.centralwidget)
        self.label_malophocphan.setGeometry(QtCore.QRect(20, 40, 400, 30))
        self.label_malophocphan.setObjectName("label_malophocphan")
        self.label_giaoviengiangday = QtWidgets.QLabel(self.centralwidget)
        self.label_giaoviengiangday.setGeometry(QtCore.QRect(20, 10, 400, 30))
        self.label_giaoviengiangday.setObjectName("label_giaoviengiangday")
        self.label_tenhocphan = QtWidgets.QLabel(self.centralwidget)
        self.label_tenhocphan.setGeometry(QtCore.QRect(20, 70, 400, 30))
        self.label_tenhocphan.setObjectName("label_tenhocphan")

        self.btn_exportFile = QtWidgets.QPushButton(self.centralwidget)
        self.btn_exportFile.setGeometry(QtCore.QRect(800, 75, 160, 40))
        self.btn_exportFile.setObjectName("btn_exportFile")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 27))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.ShowDataFrame(self.tableWidget)

        self.btn_exportFile.clicked.connect(self.ExportFile)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def ExportFile(self):
        import os
        fpath = os.getcwd()
        path = os.path.join(fpath, 'File_Export')
        os.chdir(path)
        fileName = f"{self.subject_name}_{self.maLHP}.xlsx"
        self.df = self.df.rename(columns={'maSV': 'Mã sinh viên'})
        self.df = self.df.rename(columns={'hoDem': 'Họ đệm'})
        self.df = self.df.rename(columns={'ten': 'Tên'})

        self.df.to_excel(fileName)
        os.chdir(fpath)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Thông tin điểm danh"))
        self.label_giaoviengiangday.setText(_translate("MainWindow", "Giáo viên giảnh dạy: "+self.teacher_name))
        self.label_malophocphan.setText(_translate("MainWindow", "Mã lớp học phần: "+self.maLHP))
        self.label_tenhocphan.setText(_translate("MainWindow", "Tên học phần: "+self.subject_name))
        self.btn_exportFile.setText(_translate("MainWindow", "Xuất file Excel"))

    def ShowDataFrame(self, tableWidget):
        for number_index, index in enumerate(self.df.index):
            # print(number_index, index)
            data = QtWidgets.QTableWidgetItem(index)
            data.setTextAlignment(Qt.AlignCenter)
            tableWidget.setItem(number_index, 0, data)
            for number_columns, columns in enumerate(self.df.columns):
                # print(number_columns, self.df.loc[index, columns])
                data = QtWidgets.QTableWidgetItem(self.df.loc[index, columns])
                # data.setTextAlignment(Qt.AlignCenter)
                tableWidget.setItem(number_index, number_columns+1, data)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    UI = Ui_MainWindow('201920503127005', 'Vi Văn Oanh', 'Trí Tuệ Nhân Tạo')
    UI.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())
