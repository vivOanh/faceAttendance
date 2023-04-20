import face_recognition
import cv2
import os
import numpy as np
import sqlite3

class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.list_student_id = []
        # Resize frame for a faster speed
        self.frame_resizing = 0.4

    def load_encoding_images(self, images_path, maLHP):
        print(maLHP)
        list_img_path = []
        conn = sqlite3.connect("data.db")
        sql_select_url_in_lophocphan = """
            SELECT url_anh,hoDem, ten, Sinhviens.maSV FROM Lophocphan_Sinhviens INNER JOIN Sinhviens 
            ON Lophocphan_Sinhviens.maSV = Sinhviens.maSV 
            WHERE Lophocphan_Sinhviens.maLHP ='"""+maLHP+"""';
        """
        sinhviens = conn.execute(sql_select_url_in_lophocphan)
        for item in sinhviens:
            list_img_path.append(os.path.join(images_path, item[0]))
            self.known_face_names.append(item[1]+" "+item[2])
            self.list_student_id.append(item[3])
        conn.close()
        # Store image encoding and names
        for img_path in list_img_path:
            print(img_path)
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # Get encoding
            img_encoding = face_recognition.face_encodings(rgb_img)[0]
            # Store file name and file encoding
            self.known_face_encodings.append(img_encoding)
        print("Mã hóa hình ảnh thành công")

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        # Find all the faces and face encodings in the current frame of video
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        # face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame)

        name = ""
        id = ""
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            # matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if face_distances[best_match_index] < 0.45:
                name = self.known_face_names[best_match_index]
                id = self.list_student_id[best_match_index]
        return id, name

