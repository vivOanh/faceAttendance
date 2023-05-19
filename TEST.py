import cv2
import os
import sqlite3


def ResizeImages():
    path = os.getcwd()
    path = os.path.join(path, 'images')
    os.chdir(path)
    for label in os.listdir():
        print(label)
        image = cv2.imread(os.path.join(path, label))
        new_image = cv2.resize(image, (150, 150))
        cv2.imwrite(label, new_image)
    print(f"Done!")

ResizeImages()

def InsertTableDiemDanh(maLHP):
    conn = sqlite3.connect('data.db')
    querySelect = f"SELECT maSV, ngayHoc FROM Lophocphan_Sinhviens INNER JOIN Thoikhoabieu_Lophocphans ON " \
                  f"Lophocphan_Sinhviens.maLHP = Thoikhoabieu_Lophocphans.maLHP WHERE Lophocphan_Sinhviens.maLHP = '{maLHP}';"
    result = conn.execute(querySelect).fetchall()
    for data in result:
        maSV = data[0]
        ngayHoc = data[1]
        queryInsertDiemdanh = f"INSERT INTO Diemdanhs(maLHP, maSV, ngayHoc, diemdanh) VALUES('{maLHP}','{maSV}','{ngayHoc}','x');"
        conn.execute(queryInsertDiemdanh)
        conn.commit()

    conn.close()
    print("Done!")
# InsertTableDiemDanh("202110503190006")

"""
Vi Văn Oanh
201920503127005

202010503130010
202010503130011
20221IT6021007
----------------
201920503127001
201920503127002
20221IT6021005
201920503127008
-----------------
201920503127004
201920503127003
20221IT6021006
-----------------
202010503130012
202110503190005
202110503190006
-----------------
201920503127008


"""