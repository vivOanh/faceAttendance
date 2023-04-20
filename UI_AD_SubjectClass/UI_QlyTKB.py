from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

from PyQt5.QtCore import Qt


class Ui_MainWindow(object):

    def insert_data_in_tablewidget(self, tablewidget, maLHP):
        conn = sqlite3.connect('data.db')
        sql_select_acc = "SELECT * FROM Thoikhoabieu_Lophocphans WHERE maLHP = '"+maLHP+"'"
        self.result_acc = conn.execute(sql_select_acc)
        self.num_acc = len(conn.execute(sql_select_acc).fetchall())

        self.tableWidget.setRowCount(self.num_acc)

        for index_row, data_row in enumerate(self.result_acc):
            # print(index_row, data_row)
            for index_col, data_col in enumerate(data_row):
                # print(index_col, data_col)
                data = QtWidgets.QTableWidgetItem(str(data_col))
                data.setTextAlignment(Qt.AlignCenter)
                tablewidget.setItem(index_row, index_col, data)
        conn.close()

    def GetDataInFocusRow(self):
        index = self.tableWidget.currentRow()
        id = self.tableWidget.item(index, 0).text()
        maLHP = self.tableWidget.item(index, 1).text()
        ngayHoc = self.tableWidget.item(index, 2).text()
        tietHoc = self.tableWidget.item(index, 3).text()
        phongHoc = self.tableWidget.item(index, 4).text()
        print(id ,maLHP, ngayHoc, tietHoc, phongHoc)
        return id, maLHP, ngayHoc, tietHoc, phongHoc

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 90, 750, 400))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)

        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Mã lớp học phần','Ngày học', 'Tiết học', 'Phòng học'])
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 250)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 150)

        self.btn_them = QtWidgets.QPushButton(self.centralwidget)
        self.btn_them.setGeometry(QtCore.QRect(800, 80, 180, 40))
        self.btn_them.setObjectName("btn_them")
        self.btn_sua = QtWidgets.QPushButton(self.centralwidget)
        self.btn_sua.setGeometry(QtCore.QRect(800, 200, 180, 40))
        self.btn_sua.setObjectName("btn_sua")
        self.btn_xoa = QtWidgets.QPushButton(self.centralwidget)
        self.btn_xoa.setGeometry(QtCore.QRect(800, 320, 180, 40))
        self.btn_xoa.setObjectName("btn_xoa")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 771, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.btn_thoat = QtWidgets.QPushButton(self.centralwidget)
        self.btn_thoat.setGeometry(QtCore.QRect(800, 440, 180, 40))
        self.btn_thoat.setObjectName("btn_thoat")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.btn_sua.clicked.connect(self.GetDataInFocusRow)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ỨNG DỤNG ĐIỂM DANH BẰNG KHUÔN MẶT"))
        self.btn_them.setText(_translate("MainWindow", "Thêm"))
        self.btn_sua.setText(_translate("MainWindow", "Sửa"))
        self.btn_xoa.setText(_translate("MainWindow", "Xóa"))
        self.label.setText(_translate("MainWindow", "QUẢN LÝ THỜI KHÓA BIỂU"))
        self.btn_thoat.setText(_translate("MainWindow", "Thoát"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.insert_data_in_tablewidget(ui.tableWidget, '201920503127001')
    MainWindow.show()
    sys.exit(app.exec_())