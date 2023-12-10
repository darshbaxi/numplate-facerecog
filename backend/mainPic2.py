import firebase_admin
from firebase_admin import credentials, storage, db
# import face_recognition
from utils import final_processed, OCR_results, download_image_from_storage
from roboflow import Roboflow
import os
import cv2

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {'storageBucket': 'numplate-face.appspot.com',
                                     'databaseURL': 'https://numplate-face-default-rtdb.firebaseio.com/'})

rf = Roboflow(api_key="ULr8zI3pE4MU4eijDqFm")
project = rf.workspace().project("license-plate-detection-l8xs4")
model = project.version(1).model

ref = db.reference('num-face')

def Validation(UpfileName):

    download_image_from_storage(UpfileName, 'test.png')

    picture = "test.png"
    image = cv2.imread(picture)
    # infer on a local image

    detections = model.predict(picture, confidence=40, overlap=30).json()


    # model.predict(picture, confidence=20, overlap=30).save("backend/prediction.jpg")

    # print(detections)


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

        output_path = os.path.join('output_images', filename)
        cv2.imwrite(output_path, fin_processed)
        ocr_texts = OCR_results(output_path)
        ocr_text_string = ' '.join(map(str, ocr_texts))
        
        print("The license plate number is:", ocr_text_string)

        # Create a unique filename based on OCR text or x1 coordinate
        if ocr_texts:
            fileName = f'{ocr_text_string}.jpg'

        # Save the fin_processed image
        output_Path = os.path.join('output_images', fileName)
        cv2.imwrite(output_Path, detection_crop)

        os.remove(output_path)

        # Function to find a match and return the ID and name
        def find_match(input_licence):
            data = ref.get()
            for key, value in data.items():
                if input_licence == value.get('licence'):
                    return key, value.get('name')
            return None, None

        # Example usage
        result_id, result_name = find_match(ocr_text_string)

        if result_id is not None:
            print(f"Match found! ID: {result_id}, Name: {result_name}")
            return(result_name)
        else:
            return("No match found.")

        





    # download_image_from_storage('Registration/GJ01234', 'backend/validating.png')


    # # Load the jpg files into numpy arrays
    # Harry_image = face_recognition.load_image_file("backend/validating.png")
    # unknown_image = face_recognition.load_image_file(picture)


    # # Get the face encodings for each face in each image file
    # # Since there could be more than one face in each image, it returns a list of encodings.
    # # But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
    # try:
    #     Harry_face_encoding = face_recognition.face_encodings(Harry_image)[0]
    #     unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
    # except IndexError:
    #     print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
    #     quit()

    # known_faces = [
    #     Harry_face_encoding
    # ]

    # # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
    # results = face_recognition.compare_faces(known_faces, unknown_face_encoding)

    # print("Is the unknown face a picture of Sarah Baxi? {}".format(results[0]))
    # print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))


    # os.remove("backend/validating.png")
    # os.remove("backend/test.png")