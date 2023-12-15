import firebase_admin
from firebase_admin import credentials, storage, db
import face_recognition
from utils import final_processed, OCR_results, download_image_from_storage
from roboflow import Roboflow
import os
import cv2
from fuzzywuzzy import fuzz

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


        def find_match(input_licence):
            data = ref.get()
            
            for key, value in data.items():
                licence_to_compare = value.get('licence')
                
                # Use ratio() from fuzzywuzzy to get a similarity score
                similarity_score = fuzz.ratio(input_licence, licence_to_compare)
                
                # You can adjust the threshold as needed (e.g., 80 for 80% similarity)
                if similarity_score >= 30:
                    return key, value.get('name'),value.get('licence')

            # If no match is found, return None, None
            return None, None, None




        result_id, result_name, licenseNum = find_match(ocr_text_string)
            # Your existing code that uses result_id, result_name, and licenseNum goes here



        if result_id is not None:
            download_image_from_storage('Registration/' + result_id, 'validating.png')

            validation_image = face_recognition.load_image_file("validating.png")
            original_image = face_recognition.load_image_file(picture)
            try:
                validation_image_encoding = face_recognition.face_encodings(validation_image)[0]
                original_image_encoding = face_recognition.face_encodings(original_image)[0]
                results = face_recognition.compare_faces([validation_image_encoding], original_image_encoding)
                print(results)
            except IndexError:
                print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
                quit()
            os.remove('test.png')
            os.remove('validating.png')
            if(results[0]==True):
                print(f"Match found! ID: {result_id}, Name: {result_name} and Faces matches also found")
                return ([result_name, licenseNum])
            else:
                return([0,licenseNum])
        else:
            return([0,0])



