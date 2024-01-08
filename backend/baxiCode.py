import firebase_admin
from firebase_admin import credentials, storage, db
# import face_recognition
from utils import final_processed, OCR_results, download_image_from_storage
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
        if (class_id == 0):
            detection_crop = frame[int(y1):int(y2), int(x1):int(x2), :]
            fin_processed = final_processed(detection_crop)
            filename = f'x1_{x1}.jpg'
            output_path = os.path.join('output_images', filename)
            cv2.imwrite(output_path, fin_processed)
            ocr_texts = OCR_results(fin_processed)
            print(ocr_texts)
            ocr_text_string = ' '.join(map(str, ocr_texts))
            print("The license plate number is:", ocr_text_string)


            if ocr_texts:
                fileName = f'{ocr_text_string}.jpg'
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
                            return key, value.get('name'), value.get('licence')

                    # If no match is found, return None, None
                    return None, None, None



            # Example usage
                    result_id, result_name = find_match(ocr_text_string)

                    if result_id is not None:
                        # download_image_from_storage('Registration/' + result_id, 'validating.png')
                        #
                        # validation_image = face_recognition.load_image_file("validating.png")
                        # original_image = face_recognition.load_image_file(picture)
                        # try:
                        #     validation_image_encoding = face_recognition.face_encodings(validation_image)[0]
                        #     original_image_encoding = face_recognition.face_encodings(original_image)[0]
                        #     results = face_recognition.compare_faces([validation_image_encoding], original_image_encoding)
                        #     print(results)
                        # except IndexError:
                        #     print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
                        #     quit()
                        # os.remove('test.png')
                        # os.remove('validating.png')
                        # if(results[0]==True):
                        #     print(f"Match found! ID: {result_id}, Name: {result_name} and Faces matches also found")
                        #     return (result_name,results[0])
                        return (result_name)
                    else:
                        return ("No match found.")


def Validation(UpfileName):
    download_image_from_storage(UpfileName, 'test.mp4')
    cap = cv2.VideoCapture('./test.mp4')
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_index = 0
    while True:
        # Read the frame
        ret, frame = cap.read()

        # Check if the frame was read successfully
        if not ret:
            break

        if frame_index % int(fps) == 0:
            # output_filename = f"processed_frame_{frame_index // int(fps)}.png"
            # cv2.imwrite(output_path + '/' + output_filename, frame)
            # return frame
            string_licence_num = license_Plate(frame)




        frame_index += 1

    return string_licence_num




