import firebase_admin
from firebase_admin import credentials, storage, db
import face_recognition
from utils import final_processed, OCR_results, download_image_from_storage, PaddleOCRLocal
import os
import cv2
from ultralytics import YOLO
# from frameIdea import process_video
from fuzzywuzzy import fuzz

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {'storageBucket': 'numplate-face.appspot.com',
                                     'databaseURL': 'https://numplate-face-default-rtdb.firebaseio.com/'})

coco_model = YOLO('yolov8n.pt')
license_plate_detector = YOLO('weights/best.pt')
ref = db.reference('num-face')


def license_Plate(frame):
    # print("in actual func")
    # print(frame)

    vehicles = [2, 3, 5, 7]
    detections = coco_model(frame)[0]
    detections_ = []
    for detection in detections.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = detection
        if int(class_id) in vehicles:
            detections_.append([int(x1), int(y1), int(x2), int(y2), score])

    license_plates = license_plate_detector(frame)[0]
    for license_plate in license_plates.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = license_plate
        print(license_plate)
        if (class_id == 0):
            print('hi')
            detection_crop = frame[int(y1):int(y2), int(x1):int(x2), :]
            fin_processed = final_processed(detection_crop)
            filename = f'x1_{x1}.png'
            output_path = os.path.join('output_images', filename)
            cv2.imwrite(output_path, fin_processed)
            # ocr_texts = OCR_results(output_path)
            # print(ocr_texts)
            # ocr_text_string = ' '.join(map(str, ocr_texts))

            ocr_texts = PaddleOCRLocal(output_path)
            ocr_text_string = ocr_texts

            print("The license plate number is:", ocr_text_string)


            os.remove(output_path)
            if ocr_texts:
                fileName = f'{ocr_text_string}.jpg'
                # output_Path = os.path.join('output_images', fileName)
                detection_crop = cv2.rotate(detection_crop, cv2.ROTATE_180)
                # cv2.imwrite(output_Path, detection_crop)

                # def find_match(input_licence):
                #     data = ref.get()
            
                #     for key, value in data.items():
                #         licence_to_compare = value.get('licence')
                        
                #         # Use ratio() from fuzzywuzzy to get a similarity score
                #         similarity_score = fuzz.ratio(input_licence, licence_to_compare)
                        
                #         # You can adjust the threshold as needed (e.g., 80 for 80% similarity)
                #         if similarity_score >= 80:
                #             flag = 1
                #             return key, value.get('name'),value.get('licence'),flag
                        
                #     # If no match is found, return None, None
                #     return None, None, None, 0


                data = ref.get()
    
                for key, value in data.items():
                    licence_to_compare = value.get('licence')
                    
                    # Use ratio() from fuzzywuzzy to get a similarity score
                    similarity_score = fuzz.ratio(ocr_text_string, licence_to_compare)
                    
                    # You can adjust the threshold as needed (e.g., 80 for 80% similarity)
                    if similarity_score >= 80:
                        flag = 1
                        result_id = key
                        result_name = value.get('name')
                        licenseNum = value.get('licence')
                        print(result_name, licenseNum)
                        return result_name, licenseNum, result_id, flag
                
                # os.remove(output_Path)
    return 0,0,0,0
                        
             
def faceRec(result_id, result_name,frame, licenseNum):
    output_path_checkFace = result_name + ".png"
    print(output_path_checkFace)

    # Rotate the frame by 180 degrees
    rotated_frame = cv2.rotate(frame, cv2.ROTATE_180)

    cv2.imwrite(output_path_checkFace, rotated_frame)
    print("saved")
    results = [0,0]
    download_image_from_storage('Registration/' + result_id, 'validating.png')

    validation_image = face_recognition.load_image_file("validating.png")
    original_image = face_recognition.load_image_file(output_path_checkFace)
    try:
        validation_image_encoding = face_recognition.face_encodings(validation_image)[0]
        original_image_encoding = face_recognition.face_encodings(original_image)[0]
        results = face_recognition.compare_faces([validation_image_encoding], original_image_encoding)
        print(results)
    except IndexError:
        print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
    os.remove('validating.png')
    os.remove(output_path_checkFace)
    if(results[0]==0):
        pass
    elif(results[0]==True):
        print(f"Match found! ID: {result_id}, Name: {result_name} and Faces matches also found")
        return ([result_name, licenseNum], 2)
    else:
        return([0,licenseNum],1)

    return([0,0], 1)


def Validation(UpfileName):
    download_image_from_storage(UpfileName, 'test.mp4')
    cap = cv2.VideoCapture('./test.mp4')
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_index = 0
    flag = 0
    while True:
        # Read the frame
        ret, frame = cap.read()

        # Check if the frame was read successfully
        if not ret:
            break

        if frame_index % int(fps * 0.5) == 0:
        #     # output_filename = f"processed_frame_{frame_index // int(fps)}.png"
        #     # cv2.imwrite(output_path + '/' + output_filename, frame)
        #     # return frame
            if flag == 0:
                result_name, licenseNum, result_id, flag = license_Plate(frame)
            if flag == 1:
                arrayAns, flag = faceRec(result_id, result_name, frame, licenseNum)
                print(arrayAns)
            if flag == 2:
                print("Verified and Confirmed")
                break
        frame_index += 1
    os.remove('./test.mp4')
    return arrayAns




