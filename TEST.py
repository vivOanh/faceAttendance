from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lb_images = QtWidgets.QLabel(self.centralwidget)
        self.lb_images.setGeometry(QtCore.QRect(230, 100, 100, 100))
        self.lb_images.setFrameShape(QtWidgets.QFrame.Box)
        self.lb_images.setFrameShadow(QtWidgets.QFrame.Plain)
        self.lb_images.setText("")
        self.lb_images.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_images.setObjectName("lb_images")
        self.btnSelectFile = QtWidgets.QPushButton(self.centralwidget)
        self.btnSelectFile.setGeometry(QtCore.QRect(230, 240, 101, 41))
        self.btnSelectFile.setObjectName("btnSelectFile")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.btnSelectFile.clicked.connect(self.putImage)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnSelectFile.setText(_translate("MainWindow", "chon file"))

    def putImage(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(filter='(*.png);;(*.jpg)')
        self.pixmap = QtGui.QPixmap(fname[0])
        self.lb_images.setPixmap(self.pixmap)
        fpath = os.getcwd()
        path = os.path.join(fpath, 'indata')
        os.chdir(path)
        image = cv2.imread(fname[0])
        cv2.imwrite('demo.png', image)
        os.chdir(fpath)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
