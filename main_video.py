import cv2
from simple_facerec import SimpleFacerec

# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("images")

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# Load Camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    location_face = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
    # Detect Faces
    student_id ,face_names = sfr.detect_known_faces(frame)
    print(student_id, face_names)
    for (x, y, w, h) in location_face:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()