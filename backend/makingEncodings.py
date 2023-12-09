import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import  storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://celebrecognize-default-rtdb.firebaseio.com/",
    'storageBucket': "celebrecognize.appspot.com"
})


# Importing student images
folderPath = 'celebPics'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

    # fileName = f'{folderPath}/{path}'
    # bucket = storage.bucket()
    # blob = bucket.blob(fileName)
    # blob.upload_from_filename(fileName)


    # print(path)
    # print(os.path.splitext(path)[0])
print(studentIds)


def findEncodings(imagesList, filenames):
    encodeList = []
    files_with_no_faces = []
    for img, filename in zip(imagesList, filenames):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(img)
        
        if len(face_encodings) > 0:
            # If faces were found in the image, append the first encoding to the list.
            encodeList.append(face_encodings[0])
        else:
            # Handle the case where no faces were found in the image and store the filename.
            print(f"No face found in the image: {filename}")
            files_with_no_faces.append(filename)
    
    return encodeList, files_with_no_faces


print("Encoding Started ...")
encodeListKnown, no_faces_files = findEncodings(imgList, studentIds)
print(no_faces_files)

# print(encodeListKnown)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print(studentIds)
print("Encoding Complete")

file = open("EncodeFileas.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")