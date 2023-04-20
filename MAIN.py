from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import sqlite3
import time

from UI_US import UI_Main, UI_Webcam, UI_Login, UI_TB_Login, UI_SHOW_INFO, UI_Notification_Nodate, UI_NotificationLogout
from UI_AD import UI_AccAD, UI_MainAdmin, UI_SubjectAd, UI_SubjectClass_ad, UI_ListStudent
from UI_AD_Account import UI_add_acc, UI_Notifi_Error, UI_Acc_AlreadyExist, UI_Notifi_add_success, UI_Notifi_Confirm_delete, UI_Fix_acc
from UI_AD_Subject import UI_Add_Subject, UI_Subject_Already_exist, UI_Fix_Subject
from UI_AD_SubjectClass import UI_ADD_SubjectClass, UI_Edit_SubjectClass, UI_SubjectClass_AlreadyExist, UI_QlySinhvien, UI_QlyTKB, UI_AddTKB, UI_EditTKB
from UI_Student import UI_AddStudent, UI_EditStdent, UI_Student_AlreadyExist

def time_to_string(time=time.localtime(time.time())):
    day = str(time.tm_mday)
    month = str(time.tm_mon)
    return day + "/" + month


class MAIN:
    def __init__(self):
        self.login_win = QMainWindow()
        self.ui_login = UI_Login.Ui_MainWindow()
        self.ui_login.setupUi(self.login_win)
        self.login_win.show()

    #   Xử lý sự kiện clicked
        self.ui_login.btn_dangnhap.clicked.connect(self.check_login)

    def check_login(self):
        conn = sqlite3.connect('data.db')
        sql_acc = "SELECT quyen, maGV, hoTenGV FROM Taikhoans WHERE tenDangNhap = '"+self.ui_login.input_tendangnhap.text()+"' AND " \
                    "matKhau = '"+self.ui_login.input_matkhau.text()+"';"
        self.info_acc = conn.execute(sql_acc).fetchone()
        print(self.info_acc)
        if not self.info_acc:
            self.notification_win = QMainWindow()
            self.ui_notification_login = UI_TB_Login.Ui_MainWindow()
            self.ui_notification_login.setupUi(self.notification_win)
            self.notification_win.show()
            self.ui_notification_login.pushButton.clicked.connect(self.Hide_ui_notification)
        else:
            self.ui_login.teacher_name = self.info_acc[2]
            self.ui_login.id_teacher = self.info_acc[1]
            if self.info_acc[0] == "ad":
                self.login_win.hide()
                self.main_ad_win = QMainWindow()
                self.ui_main_ad = UI_MainAdmin.Ui_btnQuanSV()

                self.ui_main_ad.login = True
                self.ui_main_ad.teacher_name = self.ui_login.teacher_name

                self.ui_main_ad.setupUi(self.main_ad_win)
                if self.ui_main_ad.login:
                    self.main_ad_win.show()
                    self.ui_main_ad.btn_logout.clicked.connect(self.ad_clicked_btn_logout)
                    self.ui_main_ad.btnQuanLyTK.clicked.connect(self.ad_clicked_btn_quanlytk)
                    self.ui_main_ad.btnQuanLyHP.clicked.connect(self.ui_subject_ad_show)
                    self.ui_main_ad.btnQuanLyLHP.clicked.connect(self.uiQuanLyLHPShow)
                    self.ui_main_ad.btnQuanLySV.clicked.connect(self.ManageStuent)


            elif self.info_acc[0] == 'us':
                self.login_win.hide()
            #   Màn hình chính
                self.main_win = QMainWindow()

                self.ui_main = UI_Main.Ui_MainWindow(self.ui_login.id_teacher, self.ui_login.teacher_name)
                self.ui_main.setupUi(self.main_win)
                self.ui_main.teacher_name = self.ui_login.teacher_name
                self.main_win.show()
            #   Xử lý clicked giao diện chính
                self.ui_main.btn_diemdanh.clicked.connect(self.log_data)
                self.ui_main.btn_thongtindiemdanh.clicked.connect(self.ShowInFo)
                self.ui_main.btn_logout.clicked.connect(self.LogOut)



#   Quản lý sinh viên
    def ManageStuent(self):
        self.winManageStudent = QMainWindow()
        self.uiManageStudent = UI_ListStudent.Ui_MainWindow()
        self.uiManageStudent.setupUi(self.winManageStudent)
        self.uiManageStudent.InsertDataInTableWidget(self.uiManageStudent.tableWidget)
        self.winManageStudent.show()

        self.uiManageStudent.btnThem.clicked.connect(self.AddStudent)
        self.uiManageStudent.btnSua.clicked.connect(self.EditStudent)
        self.uiManageStudent.btnXoa.clicked.connect(self.DeleteStudent)
        self.uiManageStudent.btnThoat.clicked.connect(self.UIManagetStudentBackToMainAd)

    def UIManagetStudentBackToMainAd(self):
        self.main_ad_win.show()
        self.winManageStudent.hide()

#   Xóa sinh viên
    def DeleteStudent(self):
        self.winConfirmDelStudent = QMainWindow()
        self.uiConfirmDelStudent = UI_Notifi_Confirm_delete.Ui_MainWindow()
        self.uiConfirmDelStudent.setupUi(self.winConfirmDelStudent)
        self.winConfirmDelStudent.show()

        self.uiConfirmDelStudent.btn_no.clicked.connect(self.DeleteStudent_No)
        self.uiConfirmDelStudent.btn_yes.clicked.connect(self.DeleteStudent_Yes)
    def DeleteStudent_Yes(self):
        maSV = self.uiManageStudent.GetMaSV()
        sqlDelStudent = "DELETE FROM Sinhviens WHERE maSV = '"+maSV+"';"
        conn = sqlite3.connect('data.db')
        conn.execute(sqlDelStudent)
        conn.commit()
        conn.close()

        self.uiManageStudent.InsertDataInTableWidget(self.uiManageStudent.tableWidget)
        self.winManageStudent.show()
        self.winConfirmDelStudent.hide()

    def DeleteStudent_No(self):
        self.winConfirmDelStudent.hide()

#   Chỉnh sửa thông tin sinh viên
    def EditStudent(self):
        maSV = self.uiManageStudent.GetMaSV()
        self.winEditStudent = QMainWindow()
        self.uiEditStudent = UI_EditStdent.Ui_MainWindow(maSV)
        self.uiEditStudent.setupUi(self.winEditStudent)
        self.winEditStudent.show()
        self.uiEditStudent.btnSua.clicked.connect(self.CheckDataInputEditStudent)

    def CheckDataInputEditStudent(self):
        maSV, hoDem, ten, ngaySinh, gioiTinh, nganhHoc, lop = self.uiEditStudent.GetDataInput()
        if hoDem == "" or ten == "" or ngaySinh == "" or nganhHoc == "" or lop == "":
            self.ui_notifi_error = UI_Notifi_Error.Ui_MainWindow()
            self.ui_notifi_error.setupUi(self.ui_notifi_error.MainWindow)
            self.ui_notifi_error.MainWindow.show()
        else:
            conn = sqlite3.connect('data.db')
            sqlUpdateStudent = "UPDATE Sinhviens SET hoDem = '"+hoDem+"', ten = '"+ten+"'," \
                               " ngaySinh = '"+ngaySinh+"', gioiTinh = '"+gioiTinh+"', nganhHoc = '"+nganhHoc+"', lop = '"+lop+"'" \
                               " WHERE maSV = '"+maSV+"';"
            conn.execute(sqlUpdateStudent)
            conn.commit()
            conn.close()

            self.uiManageStudent.InsertDataInTableWidget(self.uiManageStudent.tableWidget)
            self.winManageStudent.show()
            self.winEditStudent.hide()


#   Thêm sinh viên
    def AddStudent(self):
        self.winAddStudent = QMainWindow()
        self.uiAddStudent = UI_AddStudent.Ui_MainWindow()
        self.uiAddStudent.setupUi(self.winAddStudent)
        self.winAddStudent.show()

        self.uiAddStudent.btnThem.clicked.connect(self.CheckDataInputAddStudent)
    def CheckDataInputAddStudent(self):
        maSV, hoDem, ten, ngaySinh, gioiTinh, nganhHoc, lop = self.uiAddStudent.GetDataInput()
        if maSV == "" or hoDem == "" or ten == "" or ngaySinh == "" or nganhHoc == "" or lop== "" :
            self.ui_notifi_error = UI_Notifi_Error.Ui_MainWindow()
            self.ui_notifi_error.setupUi(self.ui_notifi_error.MainWindow)
            self.ui_notifi_error.MainWindow.show()
        else:
            sqlCheckStudentAlreadyExist = "SELECT maSV FROM Sinhviens  WHERE maSV = '"+maSV+"';"
            conn = sqlite3.connect('data.db')
            if not len(conn.execute(sqlCheckStudentAlreadyExist).fetchall()):
                sqlAddStudent = " INSERT INTO Sinhviens(maSV, hoDem, ten, ngaySinh, gioiTinh, nganhHoc, lop, url_anh )" \
                                " VALUES('"+maSV+"','"+hoDem+"','"+ten+"','"+ngaySinh+"','"+gioiTinh+"','"+nganhHoc+"','"+lop+"','sv"+maSV+".png');"
                conn.execute(sqlAddStudent)
                conn.commit()

                self.winAddStudentSuccessful = QMainWindow()
                self.uiAddStudentSuccessful = UI_Notifi_add_success.Ui_MainWindow()
                self.uiAddStudentSuccessful.setupUi(self.winAddStudentSuccessful)
                self.winAddStudentSuccessful.show()
                self.uiAddStudentSuccessful.btn_ok.clicked.connect(self.AddStudentSuccessfulBack)

            else:
                self.uiStudentAlreadyExit = UI_Student_AlreadyExist.Ui_MainWindow()
                self.uiStudentAlreadyExit.setupUi(self.uiStudentAlreadyExit.MainWindow)
                self.uiStudentAlreadyExit.MainWindow.show()
            conn.close()


    def AddStudentSuccessfulBack(self):
        self.winAddStudentSuccessful.hide()
        self.uiManageStudent.InsertDataInTableWidget(self.uiManageStudent.tableWidget)
        self.winManageStudent.show()
        self.winAddStudent.hide()


#   Quản lý Lớp học phần

    def uiQuanLyLHPShow(self):
        self.winQuanLyLHP = QMainWindow()
        self.uiQuanLyLHP = UI_SubjectClass_ad.Ui_MainWindow()
        self.uiQuanLyLHP.setupUi(self.winQuanLyLHP)
        self.uiQuanLyLHP.insert_data_in_tablewidget(self.uiQuanLyLHP.tableWidget)
        self.winQuanLyLHP.show()
        self.main_ad_win.hide()

        self.uiQuanLyLHP.btn_them.clicked.connect(self.uiAddLHPShow)
        self.uiQuanLyLHP.btn_thoat.clicked.connect(self.BackToUIMainAd)
        self.uiQuanLyLHP.btn_xoa.clicked.connect(self.DeleteSubjectClass)
        self.uiQuanLyLHP.btn_sua.clicked.connect(self.EditSubjectClass)
        self.uiQuanLyLHP.btn_quanLySinhvienLHP.clicked.connect(self.managementStudentInClass)
        self.uiQuanLyLHP.btn_quanlyTKB.clicked.connect(self.ManageTKB)

    def ManageTKB(self):
        idSubjectClass, _, _ = self.uiQuanLyLHP.getDataFocus()
        self.winQlyTKB = QMainWindow()
        self.uiQlyTBK = UI_QlyTKB.Ui_MainWindow()
        self.uiQlyTBK.setupUi(self.winQlyTKB)
        self.uiQlyTBK.insert_data_in_tablewidget(self.uiQlyTBK.tableWidget, idSubjectClass)
        self.winQlyTKB.show()
        self.winQuanLyLHP.hide()

        self.uiQlyTBK.btn_thoat.clicked.connect(self.UIManageTKBBackToUIManageLHP)
        self.uiQlyTBK.btn_them.clicked.connect(self.UIAddTKB)
        self.uiQlyTBK.btn_sua.clicked.connect(self.UIEditTKB)
        self.uiQlyTBK.btn_xoa.clicked.connect(self.DeleteTBK)

    def DeleteTBK(self):

        self.winNotificationDelTKB = QMainWindow()
        self.uiNotificationDelTKB = UI_Notifi_Confirm_delete.Ui_MainWindow()
        self.uiNotificationDelTKB.setupUi(self.winNotificationDelTKB)
        self.winNotificationDelTKB.show()

        self.uiNotificationDelTKB.btn_no.clicked.connect(self.DelTKB_No)
        self.uiNotificationDelTKB.btn_yes.clicked.connect(self.DelTKB_Yes)

    def DelTKB_Yes(self):
        self.winNotificationDelTKB.hide()
        idSubjectClass, _, _ = self.uiQuanLyLHP.getDataFocus()
        id, _, _, _, _ = self.uiQlyTBK.GetDataInFocusRow()

        conn = sqlite3.connect('data.db')
        sqlDel = "DELETE FROM Thoikhoabieu_Lophocphans WHERE id = "+str(id)+""
        conn.execute(sqlDel)
        conn.commit()
        conn.close()
        # self.winQlyTKB.hide()
        self.uiQlyTBK.insert_data_in_tablewidget(self.uiQlyTBK.tableWidget, idSubjectClass)
        self.winQlyTKB.show()

    def DelTKB_No(self):
        self.winNotificationDelTKB.hide()

    def UIEditTKB(self):
        id, maLHP, ngayHoc, tietHoc, phongHoc = self.uiQlyTBK.GetDataInFocusRow()
        self.winEditTKB = QMainWindow()
        self.uiEditTKB = UI_EditTKB.Ui_MainWindow(id, maLHP, ngayHoc, tietHoc, phongHoc)
        self.uiEditTKB.setupUi(self.winEditTKB)
        self.winEditTKB.show()
        self.uiEditTKB.btn_sua.clicked.connect(self.PerformEditTKB)

    def PerformEditTKB(self):
        id, maLHP, ngayHoc, tietHoc, phongHoc = self.uiEditTKB.GetDataInput()
        idSubjectClass, _, _ = self.uiQuanLyLHP.getDataFocus()

        if ngayHoc == "" or tietHoc == "" or phongHoc == "":
            self.ui_notifi_error = UI_Notifi_Error.Ui_MainWindow()
            self.ui_notifi_error.setupUi(self.ui_notifi_error.MainWindow)
            self.ui_notifi_error.MainWindow.show()
        else:
            conn = sqlite3.connect('data.db')
            sqlUpdateTKB = "UPDATE Thoikhoabieu_Lophocphans SET ngayHoc = '"+ngayHoc+"', tietHoc = '"+tietHoc+"'," \
                            " phongHoc = '"+phongHoc+"' WHERE id = "+id+";"
            conn.execute(sqlUpdateTKB)
            conn.commit()
            conn.close()

            # self.winQlyTKB.hide()
            self.uiQlyTBK.insert_data_in_tablewidget(self.uiQlyTBK.tableWidget, idSubjectClass)
            self.winQlyTKB.show()
            self.winEditTKB.hide()

    def UIAddTKB(self):
        idSubjectClass, _, _ = self.uiQuanLyLHP.getDataFocus()
        self.winAddTKB = QMainWindow()
        self.uiAddTKB = UI_AddTKB.Ui_MainWindow(idSubjectClass)
        self.uiAddTKB.setupUi(self.winAddTKB)
        self.winAddTKB.show()
        self.uiAddTKB.btn_them.clicked.connect(self.CheckAddTKB)

    def CheckAddTKB(self):
        maLHP, ngayHoc, tietHoc, phongHoc = self.uiAddTKB.GetDataInput()
        if ngayHoc == "" or tietHoc == "" or phongHoc == "":
            #để trống thông tin
            self.ui_notifi_error = UI_Notifi_Error.Ui_MainWindow()
            self.ui_notifi_error.setupUi(self.ui_notifi_error.MainWindow)
            self.ui_notifi_error.MainWindow.show()
        else:
            sqlInsertTKB = "INSERT INTO Thoikhoabieu_Lophocphans(maLHP, ngayHoc, tietHoc, phongHoc)" \
                           " VALUES('"+maLHP+"','"+ngayHoc+"','"+tietHoc+"','"+phongHoc+"');"
            conn = sqlite3.connect('data.db')
            conn.execute(sqlInsertTKB)
            conn.commit()
            conn.close()

            self.winAddTKBSuccessful = QMainWindow()
            self.uiAddTKBSuccessful = UI_Notifi_add_success.Ui_MainWindow()
            self.uiAddTKBSuccessful.setupUi(self.winAddTKBSuccessful)
            self.winAddTKBSuccessful.show()
            self.uiAddTKBSuccessful.btn_ok.clicked.connect(self.AddTKBSuccessful)


    def AddTKBSuccessful(self):
        idSubjectClass, _, _ = self.uiQuanLyLHP.getDataFocus()
        self.winAddTKBSuccessful.hide()

        # self.winQlyTKB.hide()
        self.uiQlyTBK.insert_data_in_tablewidget(self.uiQlyTBK.tableWidget, idSubjectClass)
        self.winQlyTKB.show()
        self.winAddTKB.hide()


    def UIManageTKBBackToUIManageLHP(self):
        self.winQuanLyLHP.show()
        self.winQlyTKB.hide()

    def managementStudentInClass(self):
        idSubjectClass, nameSubject, _ = self.uiQuanLyLHP.getDataFocus()
        self.winManageStudentInClass = QMainWindow()
        self.uiManageStudentInClass = UI_QlySinhvien.Ui_MainWindow(idSubjectClass, nameSubject)
        self.uiManageStudentInClass.setupUi(self.winManageStudentInClass)
        self.uiManageStudentInClass.insertDataInTable(self.uiManageStudentInClass.ds_svLhp, self.uiManageStudentInClass.ds_svchuathem)
        self.winManageStudentInClass.show()
        self.winQuanLyLHP.hide()

        self.uiManageStudentInClass.btn_them.clicked.connect(self.insertStudentInClass)
        self.uiManageStudentInClass.btn_xoa.clicked.connect(self.deleteStudentInClass)
        self.uiManageStudentInClass.btn_thoat.clicked.connect(self.hideManagementStudentInClass)

    def insertStudentInClass(self, ):
        idSubjectClass, _, _ = self.uiQuanLyLHP.getDataFocus()
        studentId = self.uiManageStudentInClass.getStudentIdNotInClass()
        conn = sqlite3.connect('data.db')

        sqlCheckStudentInClass = "SELECT * FROM Lophocphan_Sinhviens WHERE maLHP = '"+idSubjectClass+"' AND maSV = '"+studentId+"';"
        if not len(conn.execute(sqlCheckStudentInClass).fetchall()):
            sqlInsertStudentInClass = "INSERT INTO Lophocphan_Sinhviens(maLHP, maSV) VALUES('"+idSubjectClass+"','"+studentId+"');"
            conn.execute(sqlInsertStudentInClass)
            conn.commit()
        conn.close()

        # self.winManageStudentInClass.hide()
        self.uiManageStudentInClass.insertDataInTable(self.uiManageStudentInClass.ds_svLhp,
                                                      self.uiManageStudentInClass.ds_svchuathem)
        self.winManageStudentInClass.show()

    def deleteStudentInClass(self):
        idSubjectClass, _, _ = self.uiQuanLyLHP.getDataFocus()
        studentId = self.uiManageStudentInClass.getStudentIdInClass()
        conn = sqlite3.connect('data.db')
        sqlDeleteStudentInClass = "DELETE FROM Lophocphan_Sinhviens WHERE maLHP = '"+idSubjectClass+"' AND maSV ='"+studentId+"';"
        conn.execute(sqlDeleteStudentInClass)
        conn.commit()
        conn.close()

        # self.winManageStudentInClass.hide()
        self.uiManageStudentInClass.insertDataInTable(self.uiManageStudentInClass.ds_svLhp,
                                                      self.uiManageStudentInClass.ds_svchuathem)
        self.winManageStudentInClass.show()

    def hideManagementStudentInClass(self):
        self.winManageStudentInClass.hide()
        self.winQuanLyLHP.show()

    def EditSubjectClass(self):
        self.winEditSubjectClass = QMainWindow()
        idSubjectClass, nameSubject, nameTeacher = self.uiQuanLyLHP.getDataFocus()
        self.uiEditSubjectClass = UI_Edit_SubjectClass.Ui_MainWindow(idSubjectClass, nameSubject, nameTeacher)
        self.uiEditSubjectClass.setupUi(self.winEditSubjectClass)
        self.winEditSubjectClass.show()

        self.uiEditSubjectClass.btn_suaLHP.clicked.connect(self.EditGetDataToForm)

    def EditGetDataToForm(self):
        idSubjectClass, idSubject, idTeacher = self.uiEditSubjectClass.getData()
        idTeacher = str(idTeacher)
        if idSubjectClass == "":
            self.ui_notifi_error = UI_Notifi_Error.Ui_MainWindow()
            self.ui_notifi_error.setupUi(self.ui_notifi_error.MainWindow)
            self.ui_notifi_error.MainWindow.show()
        else:
            sqlUpdateSubClass = "UPDATE Lophocphans SET maLHP = '"+idSubjectClass+"'," \
                                " maHP = '"+idSubject+"', maGV = '"+idTeacher+"' WHERE maLHP ='"+idSubjectClass+"';"
            conn = sqlite3.connect('data.db')
            conn.execute(sqlUpdateSubClass)
            conn.commit()
            conn.close()

            # self.winQuanLyLHP.hide()
            self.uiQuanLyLHP.insert_data_in_tablewidget(self.uiQuanLyLHP.tableWidget)
            self.winQuanLyLHP.show()
            self.winEditSubjectClass.hide()

    def DeleteSubjectClass(self):
        self.winNotificationSubjectClassDelete = QMainWindow()
        self.uiNotificationSubjectClassDelete = UI_Notifi_Confirm_delete.Ui_MainWindow()
        self.uiNotificationSubjectClassDelete.setupUi(self.winNotificationSubjectClassDelete)
        self.winNotificationSubjectClassDelete.show()

        self.uiNotificationSubjectClassDelete.btn_no.clicked.connect(self.NotiSubClassDel_No)
        self.uiNotificationSubjectClassDelete.btn_yes.clicked.connect(self.NotiSubClassDel_Yes)

    def NotiSubClassDel_Yes(self):
        self.winNotificationSubjectClassDelete.hide()
        maLHP, _, _ = self.uiQuanLyLHP.getDataFocus()
        sqlDeleteSubClass = "DELETE FROM Lophocphans WHERE maLHP = '"+maLHP+"';"
        conn = sqlite3.connect('data.db')
        conn.execute(sqlDeleteSubClass)
        conn.commit()
        conn.close()

        # self.winQuanLyLHP.hide()
        self.uiQuanLyLHP.insert_data_in_tablewidget(self.uiQuanLyLHP.tableWidget)
        self.winQuanLyLHP.show()

    def NotiSubClassDel_No(self):
        self.winNotificationSubjectClassDelete.hide()

    def BackToUIMainAd(self):
        self.winQuanLyLHP.hide()
        self.main_ad_win.show()

    def uiAddLHPShow(self):
        self.winAddLHP = QMainWindow()
        self.uiAddLHP = UI_ADD_SubjectClass.Ui_MainWindow()
        self.uiAddLHP.setupUi(self.winAddLHP)
        self.winAddLHP.show()
        self.uiAddLHP.btn_themlhp.clicked.connect(self.addLHP)

    def addLHP(self):
        maLHP, maHP, maGV = self.uiAddLHP.idSCSubjectAndTeacher()
        maGV = str(maGV)
        if maLHP == "":
            # để trống thông tin
            self.ui_notifi_error = UI_Notifi_Error.Ui_MainWindow()
            self.ui_notifi_error.setupUi(self.ui_notifi_error.MainWindow)
            self.ui_notifi_error.MainWindow.show()
        else:
            conn = sqlite3.connect('data.db')
            sql_check_LHP = "SELECT maLHP FROM Lophocphans WHERE maLHP = '" + maLHP + "' AND maHP = '" + maHP + "' AND maGV = '" + maGV + "';"
            if len(conn.execute(sql_check_LHP).fetchall()):
                self.uiSubjectClassAlreadyExist = UI_SubjectClass_AlreadyExist.Ui_MainWindow()
                self.uiSubjectClassAlreadyExist.setupUi(self.uiSubjectClassAlreadyExist.MainWindow)
                self.uiSubjectClassAlreadyExist.MainWindow.show()

            else:
                sqlAddLHP = "INSERT INTO Lophocphans(maLHP, maHP, maGV) VALUES('" + maLHP + "','" + maHP + "','"+maGV+"');"
                conn.execute(sqlAddLHP)
                conn.commit()

                self.winAddSubjectSuccessful = QMainWindow()
                self.uiAddSubjectSuccessful = UI_Notifi_add_success.Ui_MainWindow()
                self.uiAddSubjectSuccessful.setupUi(self.winAddSubjectSuccessful)
                self.winAddSubjectSuccessful.show()
                self.uiAddSubjectSuccessful.btn_ok.clicked.connect(self.NotificationAddSubjectClassSuccessful)

            conn.close()

    def NotificationAddSubjectClassSuccessful(self):
        # self.winQuanLyLHP.hide()
        self.uiQuanLyLHP.insert_data_in_tablewidget(self.uiQuanLyLHP.tableWidget)
        self.winAddSubjectSuccessful.hide()
        self.winAddLHP.hide()
        self.winQuanLyLHP.show()

    def ui_subject_ad_show(self):
        self.subject_ad_win = QMainWindow()
        self.ui_subject_ad = UI_SubjectAd.Ui_MainWindow()
        self.ui_subject_ad.setupUi(self.subject_ad_win)
        self.ui_subject_ad.insert_data_in_tablewidget(self.ui_subject_ad.tableWidget)
        self.main_ad_win.hide()
        self.subject_ad_win.show()

        self.ui_subject_ad.btn_thoat.clicked.connect(self.ui_subject_ad_hide)
        self.ui_subject_ad.btn_xoa.clicked.connect(self.ui_delete_subject)
        self.ui_subject_ad.btn_them.clicked.connect(self.ui_add_subject_show)
        self.ui_subject_ad.btn_sua.clicked.connect(self.ui_fix_subject_show)

    def ui_fix_subject_show(self):
        self.fix_sub_win = QMainWindow()
        self.ui_fix_sub = UI_Fix_Subject.Ui_MainWindow()
        self.ui_fix_sub.setupUi(self.fix_sub_win)

        index_row = self.ui_subject_ad.tableWidget.currentRow()

        self.ui_fix_sub.ip_mahocphan.setText(self.ui_subject_ad.tableWidget.item(index_row, 0).text())
        self.ui_fix_sub.ip_mahocphan.setFocusPolicy(Qt.NoFocus)
        self.ui_fix_sub.ip_tenhocphan.setText(self.ui_subject_ad.tableWidget.item(index_row, 1).text())
        self.ui_fix_sub.ip_sotinchi.setText(self.ui_subject_ad.tableWidget.item(index_row, 2).text())
        self.ui_fix_sub.ip_hockyday.setText(self.ui_subject_ad.tableWidget.item(index_row, 3).text())

        self.fix_sub_win.show()

        self.ui_fix_sub.btn_suahocpham.clicked.connect(self.update_sub)

    def update_sub(self):
        mahp = self.ui_fix_sub.ip_mahocphan.text()
        tenhp = self.ui_fix_sub.ip_tenhocphan.text()
        sotc = self.ui_fix_sub.ip_sotinchi.text()
        hockyday = self.ui_fix_sub.ip_hockyday.text()

        conn = sqlite3.connect('data.db')
        sql_update_sub = "UPDATE Hocphans SET tenHP = '"+tenhp+"', soTC = '"+sotc+"', hocKyDay = '"+hockyday+"' WHERE maHP = '"+mahp+"';"
        conn.execute(sql_update_sub)
        conn.commit()

        self.fix_sub_win.hide()
        # self.subject_ad_win.hide()
        self.ui_subject_ad.insert_data_in_tablewidget(self.ui_subject_ad.tableWidget)
        self.subject_ad_win.show()

    def ui_add_subject_show(self):
        self.add_subject_win = QMainWindow()
        self.ui_add_subject = UI_Add_Subject.Ui_MainWindow()
        self.ui_add_subject.setupUi(self.add_subject_win)
        self.add_subject_win.show()

        self.ui_add_subject.btn_themhocphan.clicked.connect(self.check_add_subject)

    def check_add_subject(self):
        mahp = self.ui_add_subject.ip_mahocphan.text()
        tenhp = self.ui_add_subject.ip_tenhocphan.text()
        sotc = self.ui_add_subject.ip_sotinchi.text()
        hockyday = self.ui_add_subject.ip_hockyday.text()
        if mahp == "" or tenhp == "" or sotc == "" or hockyday == "":
            self.ui_notifi_error = UI_Notifi_Error.Ui_MainWindow()
            self.ui_notifi_error.setupUi(self.ui_notifi_error.MainWindow)
            self.ui_notifi_error.MainWindow.show()
        else:
            conn = sqlite3.connect('data.db')
            sql_check_already_exist = "SELECT maHP FROM Hocphans WHERE maHP ='"+mahp+"';"
            if len(conn.execute(sql_check_already_exist).fetchall()):
                self.ui_subject_already_exist = UI_Subject_Already_exist.Ui_MainWindow()
                self.ui_subject_already_exist.setupUi(self.ui_subject_already_exist.MainWindow)
                self.ui_subject_already_exist.MainWindow.show()
            else:
                sql_insert_subject = "INSERT INTO Hocphans(maHP, tenHP, soTC, hocKyDay) VALUES ('"+mahp+"', '"+tenhp+"', '"+sotc+"', '"+hockyday+"');"
                conn.execute(sql_insert_subject)
                conn.commit()
                conn.close()
                self.insert_sub_success_win = QMainWindow()
                self.ui_insert_sub_success = UI_Notifi_add_success.Ui_MainWindow()
                self.ui_insert_sub_success.setupUi(self.insert_sub_success_win)
                self.insert_sub_success_win.show()
                self.ui_insert_sub_success.btn_ok.clicked.connect(self.ui_insert_sub_success_hide)

    def ui_insert_sub_success_hide(self):
        self.insert_sub_success_win.hide()
        self.add_subject_win.hide()
        self.ui_subject_ad.insert_data_in_tablewidget(self.ui_subject_ad.tableWidget)
        self.subject_ad_win.show()

    def ui_delete_subject(self):
        self.notifi_confirm_delete_win = QMainWindow()
        self.ui_notifi_confirm_delete = UI_Notifi_Confirm_delete.Ui_MainWindow()
        self.ui_notifi_confirm_delete.setupUi(self.notifi_confirm_delete_win)
        self.notifi_confirm_delete_win.show()

        self.ui_notifi_confirm_delete.btn_yes.clicked.connect(self.yes_ui_confirm_delete_subject)
        self.ui_notifi_confirm_delete.btn_no.clicked.connect(self.no_ui_confirm_delete_subject)


    def yes_ui_confirm_delete_subject(self):
        index_row = self.ui_subject_ad.tableWidget.currentRow()
        id_subject = self.ui_subject_ad.tableWidget.item(index_row, 0).text()
        self.notifi_confirm_delete_win.hide()
        sql_delete_acc = "DELETE FROM Hocphans WHERE maHP = '"+id_subject+"';"
        conn = sqlite3.connect('data.db')
        conn.execute(sql_delete_acc)
        conn.commit()

        # self.subject_ad_win.hide()
        self.ui_subject_ad.insert_data_in_tablewidget(self.ui_subject_ad.tableWidget)
        self.subject_ad_win.show()

        conn.close()

    def no_ui_confirm_delete_subject(self):
        self.notifi_confirm_delete_win.hide()

    def ui_subject_ad_hide(self):
        self.subject_ad_win.hide()
        self.main_ad_win.show()

    def ad_clicked_btn_logout(self):
        self.notification_logout_win = QMainWindow()
        self.ui_notification_logout = UI_NotificationLogout.Ui_MainWindow()
        self.ui_notification_logout.setupUi(self.notification_logout_win)
        self.notification_logout_win.show()

        self.ui_notification_logout.btn_no.clicked.connect(self.ad_clicked_logout_no)
        self.ui_notification_logout.btn_yes.clicked.connect(self.ad_clicked_logout_yes)

    def ad_clicked_logout_no(self):
        self.notification_logout_win.hide()

    def ad_clicked_logout_yes(self):
        self.notification_logout_win.hide()
        self.ui_main_ad.teacher_name = None
        self.main_ad_win.hide()
        self.ui_login.input_matkhau.setText(None)
        self.login_win.show()

    def ad_clicked_btn_quanlytk(self):
        self.main_ad_win.hide()
        self.account_win = QMainWindow()
        self.ui_account = UI_AccAD.Ui_MainWindow()
        self.ui_account.setupUi(self.account_win)
        self.ui_account.insert_data_in_tablewidget(self.ui_account.tableWidget)

        self.ui_account.btn_them.clicked.connect(self.add_tk)
        self.ui_account.btn_sua.clicked.connect(self.fix_tk)
        self.ui_account.btn_xoa.clicked.connect(self.notifi_delete_tk)

        self.account_win.show()
        self.ui_account.btn_thoat.clicked.connect(self.out_quanlytk)

    def notifi_delete_tk(self):
        self.notifi_confirm_delete_win = QMainWindow()
        self.ui_notifi_confirm_delete = UI_Notifi_Confirm_delete.Ui_MainWindow()
        self.ui_notifi_confirm_delete.setupUi(self.notifi_confirm_delete_win)
        self.notifi_confirm_delete_win.show()

        self.ui_notifi_confirm_delete.btn_yes.clicked.connect(self.yes_ui_confirm_delete_acc)
        self.ui_notifi_confirm_delete.btn_no.clicked.connect(self.no_ui_confirm_delete_acc)


    def yes_ui_confirm_delete_acc(self):
        index_row = self.ui_account.tableWidget.currentRow()
        id_gv = self.ui_account.tableWidget.item(index_row, 0).text()
        self.notifi_confirm_delete_win.hide()
        sql_delete_acc = "DELETE FROM Taikhoans WHERE maGV = " + id_gv
        conn = sqlite3.connect('data.db')
        conn.execute(sql_delete_acc)
        conn.commit()

        # self.account_win.hide()
        self.ui_account.insert_data_in_tablewidget(self.ui_account.tableWidget)
        self.account_win.show()

        conn.close()

    def no_ui_confirm_delete_acc(self):
        self.notifi_confirm_delete_win.hide()

    def fix_tk(self):
        index_row = self.ui_account.tableWidget.currentRow()
        id_gv = self.ui_account.tableWidget.item(index_row, 0).text()

        self.fix_acc_win = QMainWindow()
        self.ui_fix_acc = UI_Fix_acc.Ui_MainWindow()
        self.ui_fix_acc.setupUi(self.fix_acc_win)

        self.ui_fix_acc.ip_fullname.setText(self.ui_account.tableWidget.item(index_row, 1).text())
        self.ui_fix_acc.ip_username.setText(self.ui_account.tableWidget.item(index_row, 2).text())
        self.ui_fix_acc.ip_password.setText(self.ui_account.tableWidget.item(index_row, 3).text())

        self.ui_fix_acc.btn_fix.clicked.connect(self.fix_and_update_acc)
        self.fix_acc_win.show()

    def fix_and_update_acc(self):
        index_row = self.ui_account.tableWidget.currentRow()
        id_gv = self.ui_account.tableWidget.item(index_row, 0).text()
        if self.ui_fix_acc.ip_fullname == self.ui_account.tableWidget.item(index_row, 1).text() and self.ui_fix_acc.ip_username == self.ui_account.tableWidget.item(index_row, 2).text() and self.ui_fix_acc.ip_password == self.ui_account.tableWidget.item(index_row, 3).text():
            self.ui_acc_already_exist = UI_Acc_AlreadyExist.Ui_MainWindow()
            self.ui_acc_already_exist.setupUi(self.ui_acc_already_exist.MainWindow)
            self.ui_acc_already_exist.MainWindow.show()
        else:
            conn = sqlite3.connect('data.db')
            sql_update_acc = "UPDATE Taikhoans SET hoTenGV = '"+self.ui_fix_acc.ip_fullname.text()+"', " \
                            "tenDangNhap = '"+self.ui_fix_acc.ip_username.text()+"', matKhau = '"+self.ui_fix_acc.ip_password.text()+"' " \
                            "WHERE maGV = "+id_gv+";"
            conn.execute(sql_update_acc)
            conn.commit()
            conn.close()

            # self.account_win.hide()
            self.fix_acc_win.hide()
            self.ui_account.insert_data_in_tablewidget(self.ui_account.tableWidget)
            self.account_win.show()

    def add_tk(self):
        self.ad_add_acc_win = QMainWindow()
        self.ui_ad_add_acc = UI_add_acc.Ui_MainWindow()
        self.ui_ad_add_acc.setupUi(self.ad_add_acc_win)
        self.ad_add_acc_win.show()
        self.ui_ad_add_acc.btn_Sigin.clicked.connect(self.add_tk_in_db)

    def add_tk_in_db(self):
        fullname = self.ui_ad_add_acc.ip_fullname.text()
        username = self.ui_ad_add_acc.ip_username.text()
        password = self.ui_ad_add_acc.ip_password.text()
        conn = sqlite3.connect('data.db')
        if fullname == "" or username == "" or password == "":
            self.ui_notifi_error = UI_Notifi_Error.Ui_MainWindow()
            self.ui_notifi_error.setupUi(self.ui_notifi_error.MainWindow)
            self.ui_notifi_error.MainWindow.show()
        else:
            sql_check_acc = "SELECT maGV FROM Taikhoans WHERE hoTenGV = '" + fullname + "' AND tenDangNhap = '" + username + "' AND matKhau = '" + password + "';"
            if len(conn.execute(sql_check_acc).fetchall()) == 0:
                sql_insert_acc = "INSERT INTO Taikhoans(hoTenGV, tenDangNhap, matKhau, quyen) VALUES('"+fullname+"','"+username+"','"+password+"','us');"
                conn.execute(sql_insert_acc)
                conn.commit()
                print("Insert Successful")
                self.insert_acc_success_win = QMainWindow()
                self.ui_insert_acc_success = UI_Notifi_add_success.Ui_MainWindow()
                self.ui_insert_acc_success.setupUi(self.insert_acc_success_win)
                self.insert_acc_success_win.show()
                self.ui_insert_acc_success.btn_ok.clicked.connect(self.ui_insert_acc_success_hide)

            else:
                self.ui_acc_already_exist = UI_Acc_AlreadyExist.Ui_MainWindow()
                self.ui_acc_already_exist.setupUi(self.ui_acc_already_exist.MainWindow)
                self.ui_acc_already_exist.MainWindow.show()
        conn.close()


    def ui_insert_acc_success_hide(self):
        self.insert_acc_success_win.hide()
        # self.account_win.hide()
        self.ui_account.insert_data_in_tablewidget(self.ui_account.tableWidget)
        self.account_win.show()

    def out_quanlytk(self):
        self.account_win.hide()
        self.main_ad_win.show()




#   UI US
    def log_data(self):
        current_index = self.ui_main.listWidget.currentRow()
        if current_index != -1:
            subject_id = self.ui_main.list_class[current_index]
            conn = sqlite3.connect('data.db')
            sql_check_date = "SELECT maLHP FROM Thoikhoabieu_Lophocphans WHERE " \
                             "maLHP ='"+subject_id+"' AND ngayHoc = '"+time_to_string()+"';"
            result_check_date = conn.execute(sql_check_date)
            if result_check_date.fetchone():
                self.webcam_win = QMainWindow()
                self.ui_webcam = UI_Webcam.Ui_MainWindow(subject_id)
                self.ui_webcam.setupUi(self.webcam_win)
                self.webcam_win.show()
                self.ui_webcam.gddd_thoat.clicked.connect(self.OutCam)
            else:
                self.notification_nodate_win = QMainWindow()
                self.ui_notification_nodate = UI_Notification_Nodate.Ui_MainWindow()
                self.ui_notification_nodate.setupUi(self.notification_nodate_win)
                self.notification_nodate_win.show()
                self.ui_notification_nodate.btn_ok.clicked.connect(self.notification_nodate_win.hide)
            conn.close()
    def OutCam(self):
        self.ui_webcam.capture.release()
        self.webcam_win.hide()

    def LogOut(self):
            self.notification_logout_win = QMainWindow()
            self.ui_notification_logout = UI_NotificationLogout.Ui_MainWindow()
            self.ui_notification_logout.setupUi(self.notification_logout_win)
            self.notification_logout_win.show()

            self.ui_notification_logout.btn_no.clicked.connect(self.notification_logout_no)
            self.ui_notification_logout.btn_yes.clicked.connect(self.notification_logout_yes)

    def notification_logout_no(self):
        self.notification_logout_win.hide()

    def notification_logout_yes(self):
        # self.notification_nodate_win.hide()
        # self.info_win.hide()
        self.ui_login.teacher_name = None
        self.ui_login.id_teacher = None

        self.notification_logout_win.hide()
        self.main_win.hide()

        self.login_win.show()
        self.ui_login.input_matkhau.setText(None)
        self.ui_main.list_class_show.clear()
        self.ui_main.list_class.clear()

    def ShowInFo(self):
        currentIndex = self.ui_main.listWidget.currentRow()
        if currentIndex != -1:
            maLHP = self.ui_main.list_class[currentIndex]
            conn = sqlite3.connect("data.db")
            sql_maHp = "SELECT maHP FROM Lophocphans WHERE maLHP = '" + maLHP + "';"
            maHP = conn.execute(sql_maHp).fetchone()[0]
            sql = "SELECT tenHP FROM Hocphans WHERE Hocphans.maHP = '" + maHP + "'"
            tenHP = conn.execute(sql).fetchone()[0]

            self.info_win = QMainWindow()
            self.ui_info = UI_SHOW_INFO.Ui_MainWindow(maLHP, self.ui_login.teacher_name, tenHP)
            self.ui_info.setupUi(self.info_win)
            self.info_win.show()
            conn.close()

    def Hide_ui_notification(self):
        self.notification_win.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MAIN()
    sys.exit(app.exec_())
