import face_recognition
from utils import final_processed, OCR_results
from roboflow import Roboflow
import os
import cv2


rf = Roboflow(api_key="ULr8zI3pE4MU4eijDqFm")
project = rf.workspace().project("license-plate-detection-l8xs4")
model = project.version(1).model

picture = "backend/SarahBaxi.jpg"
image = cv2.imread(picture)
# infer on a local image
detections = model.predict(picture, confidence=40, overlap=30).json()


# model.predict(picture, confidence=20, overlap=30).save("backend/prediction.jpg")


for prediction in detections['predictions']:
    x1 = float(prediction['x']) - float(prediction['width']) / 2
    x2 = float(prediction['x']) + float(prediction['width']) / 2
    y1 = float(prediction['y']) - float(prediction['height']) / 2
    y2 = float(prediction['y']) + float(prediction['height']) / 2
    class_id = prediction['class_id']
    score = prediction['confidence']
    # box = (x1, y1, x2, y2)
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    detection_crop = image[y1:y2, x1:x2, :]
    fin_processed = final_processed(detection_crop)

    filename = f'x1_{x1}.jpg'

    output_path = os.path.join('backend/output_images', filename)
    cv2.imwrite(output_path, fin_processed)
    ocr_texts = OCR_results(output_path)
    ocr_text_string = ' '.join(map(str, ocr_texts))
    
    print("The license plate number is:", ocr_text_string)

    # Create a unique filename based on OCR text or x1 coordinate
    if ocr_texts:
        fileName = f'{ocr_text_string}.jpg'

    # Save the fin_processed image
    output_Path = os.path.join('backend/output_images', fileName)
    cv2.imwrite(output_Path, detection_crop)

    os.remove(output_path)


# Load the jpg files into numpy arrays
Sarah_image = face_recognition.load_image_file("backend/SarahBaxi.jpg")
James_image = face_recognition.load_image_file("backend/JamesSahu.jpg")
Christopher_image = face_recognition.load_image_file("backend/ChristopherBaxi.jpg")
Harry_image = face_recognition.load_image_file("backend/HarrySahu.jpeg")
unknown_image = face_recognition.load_image_file(picture)


# Get the face encodings for each face in each image file
# Since there could be more than one face in each image, it returns a list of encodings.
# But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
try:
    Sarah_face_encoding = face_recognition.face_encodings(Sarah_image)[0]
    James_face_encoding = face_recognition.face_encodings(James_image)[0]
    Christopher_face_encoding = face_recognition.face_encodings(Christopher_image)[0]
    Harry_face_encoding = face_recognition.face_encodings(Harry_image)[0]
    unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
except IndexError:
    print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
    quit()

known_faces = [
    Sarah_face_encoding,
    James_face_encoding,
    Christopher_face_encoding,
    Harry_face_encoding
]

# results is an array of True/False telling if the unknown face matched anyone in the known_faces array
results = face_recognition.compare_faces(known_faces, unknown_face_encoding)

print("Is the unknown face a picture of Sarah Baxi? {}".format(results[0]))
print("Is the unknown face a picture of James Sahu? {}".format(results[1]))
print("Is the unknown face a picture of Christopher Baxi? {}".format(results[2]))
print("Is the unknown face a picture of Harry Sahu? {}".format(results[3]))
print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))
