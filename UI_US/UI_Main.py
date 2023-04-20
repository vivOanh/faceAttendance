from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import sqlite3


class Ui_MainWindow(object):

    list_class = []
    list_class_show = []

    def __init__(self, teacher_id, teacher_name):
        self.teacher_id = teacher_id
        self.teacher_name = teacher_name
        conn = sqlite3.connect("data.db")
        sql_select_class = "SELECT maLHP FROM Lophocphans WHERE maGV = '"+str(self.teacher_id)+"'; "
        sql_select_id_name_class = "SELECT maLHP, tenHP FROM Lophocphans INNER JOIN Hocphans ON Lophocphans.maHP =" \
                                   " Hocphans.maHP WHERE Lophocphans.maGV = '"+str(self.teacher_id)+"';"
        result_id_name_class = conn.execute(sql_select_id_name_class)
        # print(result_id_name_class.fetchall())
        for item in result_id_name_class:
            temp = item[0] +" - "+ item[1]
            self.list_class_show.append(temp)

        result_class = conn.execute(sql_select_class)
        for item in result_class:
            self.list_class.append(item[0])
        conn.close()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 400)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 70, 500, 300))
        # print(self.list_class)
        self.listWidget.addItems(self.list_class_show)
        self.listWidget.setCurrentRow(0)

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.listWidget.setFont(font)
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 30, 250, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.btn_diemdanh = QtWidgets.QPushButton(self.centralwidget)
        self.btn_diemdanh.setGeometry(QtCore.QRect(570, 120, 180, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.btn_diemdanh.setFont(font)
        self.btn_diemdanh.setObjectName("btn_diemdanh")
        self.btn_thongtindiemdanh = QtWidgets.QPushButton(self.centralwidget)
        self.btn_thongtindiemdanh.setGeometry(QtCore.QRect(570, 190, 180, 40))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.btn_thongtindiemdanh.setFont(font)
        self.btn_thongtindiemdanh.setObjectName("btn_thongtindiemdanh")
        self.label_teacherName = QtWidgets.QLabel(self.centralwidget)
        self.label_teacherName.setGeometry(QtCore.QRect(520, 10, 201, 20))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_teacherName.setFont(font)
        self.label_teacherName.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_teacherName.setStyleSheet("color:blue;")
        self.label_teacherName.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_teacherName.setObjectName("label_teacherName")
        self.btn_logout = QtWidgets.QPushButton(self.centralwidget)
        self.btn_logout.setGeometry(QtCore.QRect(734, 10, 61, 23))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.btn_logout.setFont(font)
        self.btn_logout.setStyleSheet("border:none;\n"
"color:blue;\n"
"")
        self.btn_logout.setObjectName("btn_logout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DANH SÁCH LỚP HỌC PHẦN"))
        self.label.setText(_translate("MainWindow", "Danh sách lớp học phần"))
        self.btn_diemdanh.setText(_translate("MainWindow", "Điểm danh"))
        self.btn_thongtindiemdanh.setText(_translate("MainWindow", "Thông tin điểm danh"))
        self.label_teacherName.setText(_translate("MainWindow", self.teacher_name))
        self.btn_logout.setText(_translate("MainWindow", "Đăng xuất"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    UI = Ui_MainWindow('3','Vi Văn Oanh')
    UI.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())