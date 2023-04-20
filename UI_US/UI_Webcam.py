from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import sys
from simple_facerec import SimpleFacerec
import sqlite3
import time


def TimeToString(time=time.localtime(time.time())):
    day = str(time.tm_mday)
    month = str(time.tm_mon)
    return day + "/" + month

# Encode faces from a folder
#   201920503127001     202110503190005     201920503127005


class Ui_MainWindow(object):
    def __init__(self, maLHP):
        self.maLHP = maLHP
        super().__init__()
        self.sfr = SimpleFacerec()
        self.sfr.load_encoding_images("images", self.maLHP)
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        self.MAINWINDOW = QtWidgets.QMainWindow()
        self.setupUi(self.MAINWINDOW)


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(820, 400)
        MainWindow.setMaximumSize(QtCore.QSize(900, 400))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        MainWindow.setFont(font)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.Vietnamese, QtCore.QLocale.Vietnam))

        self.student_name = ""
        self.student_id = ""
        self.check_start = False
        self.id_students = []
        self.ngayHoc = TimeToString()


        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.out_cam = QtWidgets.QLabel(self.centralwidget)
        self.out_cam.setGeometry(QtCore.QRect(20, 10, 550, 365))
        self.out_cam.setFrameShape(QtWidgets.QFrame.Box)
        self.out_cam.setLineWidth(5)
        self.out_cam.setText("")
        self.out_cam.setAlignment(QtCore.Qt.AlignCenter)
        self.out_cam.setObjectName("out_cam")
        self.gddd_batdau = QtWidgets.QPushButton(self.centralwidget)
        self.gddd_batdau.setGeometry(QtCore.QRect(640, 200, 131, 41))
        self.gddd_batdau.setObjectName("gddd_batdau")
        self.gddd_ketthuc = QtWidgets.QPushButton(self.centralwidget)
        self.gddd_ketthuc.setGeometry(QtCore.QRect(640, 270, 131, 41))
        self.gddd_ketthuc.setObjectName("gddd_ketthuc")
        self.gddd_thoat = QtWidgets.QPushButton(self.centralwidget)
        self.gddd_thoat.setGeometry(QtCore.QRect(640, 330, 131, 41))
        self.gddd_thoat.setObjectName("gddd_batdau")
        self.gddd_msv = QtWidgets.QLabel(self.centralwidget)
        self.gddd_msv.setGeometry(QtCore.QRect(580, 50, 300, 22))
        self.gddd_msv.setObjectName("gddd_msv")
        self.gddd_hoten = QtWidgets.QLabel(self.centralwidget)
        self.gddd_hoten.setGeometry(QtCore.QRect(580, 110, 300, 22))
        self.gddd_hoten.setObjectName("gddd_hoten")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 820, 27))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        # self.gddd_thoat.clicked.connect()
        self.capture = cv2.VideoCapture(0)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.display_frame)
        self.timer.timeout.connect(self.Update_name_id)
        self.timer.start(60)

        self.gddd_batdau.clicked.connect(self.Start)
        self.gddd_ketthuc.clicked.connect(self.End)

        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def Start(self):
        # print(self.check_start)
        self.check_start = True
        # print(TimeToString())
        print(self.student_id)

    def End(self):
        self.check_start = False
        for item in self.id_students:
            if item:
                sql_insert_diemdanhs = "INSERT INTO Diemdanhs(maLHP, maSV, ngayHoc, diemdanh) " \
                                       "VALUES('" + self.maLHP + "','" + item + "','" + self.ngayHoc + "','x');"
                conn = sqlite3.connect('data.db')
                result_check = conn.execute("SELECT maSV FROM Diemdanhs WHERE maLHP = '"+self.maLHP+"' AND maSV = '"+item+"' AND ngayHoc = '"+self.ngayHoc+"'")
                if len(result_check.fetchall()) == 0:
                    conn.execute(sql_insert_diemdanhs)
                    conn.commit()
                # print(sql_insert_diemdanhs)


    def Update_name_id(self):
        self.gddd_msv.setText("Mã sinh viên: "+self.student_id)
        self.gddd_hoten.setText("Họ tên: "+self.student_name)

    def display_frame(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            location_face = self.face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
            # Detect Faces
            if self.check_start:
                self.student_id, self.student_name = self.sfr.detect_known_faces(frame)
                if self.student_id not in self.id_students:
                    self.id_students.append(self.student_id)

            for (x, y, w, h) in location_face:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(image)
            self.out_cam.setPixmap(pixmap)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Giao diện điểm danh"))
        self.gddd_batdau.setText(_translate("MainWindow", "Bắt đầu"))
        self.gddd_ketthuc.setText(_translate("MainWindow", "Kết thúc"))
        self.gddd_thoat.setText(_translate("MainWindow", "Thoát"))
        self.gddd_msv.setText(_translate("MainWindow", "Mã sinh viên: "))
        self.gddd_hoten.setText(_translate("MainWindow", "Họ tên: "))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    giaodiendiemdanh = Ui_MainWindow("202110503190005")
    giaodiendiemdanh.MAINWINDOW.show()
    sys.exit(app.exec_())