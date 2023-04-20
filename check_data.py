import sqlite3


import time
def TimeToString(time = time.localtime(time.time())):
    day = str(time.tm_mday)
    month = str(time.tm_mon)
    return day+"/"+month

conn = sqlite3.connect("data_demo.db")
sql_select_url_in_lophocphan = """
    SELECT Sinhviens.maSV, url_anh,hoDem, ten FROM Lophocphans INNER JOIN Sinhviens 
    ON Lophocphans.maSV = Sinhviens.maSV 
    WHERE Lophocphans.maLop ='202110503190002';
"""
sinhviens = conn.execute(sql_select_url_in_lophocphan)
#
# for item in sinhviens:
#     print(item)


#------------------------Lấy buổi học
maLop = "202110503190006"
sql_select_date = """
    SELECT ngayHoc FROM Thoikhoabieulophocphans
    WHERE maLop = """+maLop+""";
"""
date = conn.execute(sql_select_date)
list_date = []
for item in date:
    list_date.append(item[0])
# print(list_date.index(TimeToString()))



sql_selectAll_lophocphan = """
    SELECT * FROM Lophocphans WHERE maSV = 2019605363;
"""
lophocphans = conn.execute(sql_selectAll_lophocphan)
# for item in lophocphans:
#     print(item)




masv = "2019605363"
index = 1
sql_update = "UPDATE Lophocphans SET b"+str(index)+" = x WHERE maSV = "+masv
"""
UPDATE Lophocphans SET b2 = 'x' WHERE maSV = 2019605363 AND maLop = 202110503190002 AND b2 = ''             - đúng
    UPDATE Lophocphans SET b2 = 'x' WHERE maSV = 2019605363 AND maLop = 202110503190002 AND b1 IS NOT NULL  - sẽ cập nhật
    UPDATE Lophocphans SET b2 = 'x' WHERE maSV = 2019605363 AND maLop = 202110503190002 AND b2 IS NULL      - không cập nhật
"""
# print(sql_update)
maGV = "gv003"

sql_select_lophocphan = "SELECT DISTINCT maLop,maGV, tenHocPhan FROM Lophocphans INNER JOIN Hocphans ON Lophocphans.maHocPhan = Hocphans.maHocPhan WHERE Lophocphans.maGV = '"+maGV+"'"


lophocphan = conn.execute(sql_select_lophocphan)
# for item in lophocphan:
#     print(item)
conn.close()





# print(TimeToString())


# import UI_thongtindiemdanh
# UI_thongtindiemdanh.Thongtindiemdanh()

conn = sqlite3.connect("data.db")
maLHP = "201920503127001"
sql_selecl_subject_name = "SELECT tenHocPhan FROM Hocphans JNNER JOIN Lophocphans ON Hocphans.maHocPhan = Lophocphans.maHP " \
                                  "WHERE Lophocphans.maLHP = '"+maLHP+"';"
sql_maHp = "SELECT maHP FROM Lophocphans WHERE maLHP = '"+maLHP+"';"
maHP = conn.execute(sql_maHp).fetchone()[0]
sql = "SELECT tenHP FROM Hocphans WHERE Hocphans.maHP = '"+maHP+"'"
tenHP = conn.execute(sql)
print(tenHP.fetchone()[0])


import cv2

cv2.imread()