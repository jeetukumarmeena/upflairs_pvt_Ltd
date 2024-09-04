import cv2
import pandas as pd
import numpy as np

def load_face_database(filename):
    try:
        face_db = pd.read_csv(filename, index_col=0)
        data = {"NAME": face_db["name"].values.tolist(),
                "ENCODING": face_db["enc"].values.tolist()}
    except Exception as e:
        print(e)
        data = {"NAME": [], "ENCODING": []}
    return data

def recognize_faces(img, face_db):
    faces = fd.detectMultiScale(img, 1.1, 5)
    for x, y, w, h in faces:
        cropped_face = img[y:y+h, x:x+w].copy()

        if len(faces) == 1:
            fresh_face_enc = fr.face_encodings(cropped_face)
            for ind, fe in enumerate(face_db["ENCODING"]):
                try:
                    matched = fr.compare_faces(fresh_face_enc, np.array(eval(fe)))[0]

                    if matched:
                        print("Matched:", face_db["NAME"][ind])
                        cv2.putText(img, face_db["NAME"][ind], (x, y), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 255), 4)
                        cv2.rectangle(img, pt1=(x, y), pt2=(x+w, y+h), color=(0, 255, 255), thickness=2)
                    else:
                        print("Not Matched")

                except IndexError:
                    print("No face is detected!!")

    return img

# Video read using webcam
vid = cv2.VideoCapture(1)

# Load face database
filename = "database.csv"
data = load_face_database(filename)

while True:
    flag, img = vid.read()

    if flag:
        img = recognize_faces(img, data)
        cv2.imshow("webcam_image", img)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break
    else:
        break

cv2.destroyAllWindows()
vid.release()
