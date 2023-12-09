import cv2
import requests
import json


#### Preproccessing for OCR ####

def grayscale(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh, im_bw = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)
    return im_bw

def noise_removal(image):
    grayscale(image)
    import numpy as np
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return (image)

def thick_font(image):
    import numpy as np
    # image = cv2.bitwise_not(image)
    # kernel = np.ones((5,5),np.uint8)
    # image = cv2.dilate(image, kernel, iterations=1)
    # image = cv2.bitwise_not(image)
    return (image)

def final_processed(img):
    img_bw = grayscale(img)

    rotated_image = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    no_noise = noise_removal(rotated_image)
    dilated_image = thick_font(no_noise)

    return dilated_image



def ocr_space_file(filename, overlay=True, api_key='K84842733188957', language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               "OCREngine": 2,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()

def OCR_results(fileName):
    test_file_response = ocr_space_file(filename=fileName)

    test_file_json = json.loads(test_file_response)
    print(test_file_json)
    
    # Check if there are ParsedResults and TextOverlay in the response
    if "ParsedResults" in test_file_json and test_file_json["ParsedResults"]:
        word_texts = []

        for line in test_file_json["ParsedResults"][0].get("TextOverlay", {}).get("Lines", []):
            for word in line.get("Words", []):
                word_texts.append(word.get("WordText", ""))

        # Printing the extracted WordText values
        print(word_texts)
        return word_texts
    else:
        print("Error in OCR processing. Check the response for details.")
        return None
