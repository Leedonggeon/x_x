# 사업자등록증 이미지 파일을 스캔하여 다음 주요 항목을 반환하는 것
# 구글 Cloud Vision API를 활용

'''
	input :
        image_url (string)
    output : {
        "is_corporate" : boolean,  # 개인사업자 : True, 법인사업자 : False
        "company_name" : str,      # 사업자 상호
        "company_biz_number" : str,   # 사업자등록번호
        "owner_name" : str,          # 대표자 성명
        "onwer_birthdate" : str,     # 대표자 생년월일, "0000-00-00"
        "open_date" : str,         # 개업연월
        "address" : str,           # 사업장 주소
    }
'''

import config

import pandas as pd
import os
import urllib.request
from PIL import Image
from io import BytesIO

import numpy as np
import platform
from PIL import ImageFont, ImageDraw, Image
#from matplotlib import pyplot as plt
 
import uuid
import json
import time
import cv2
import requests

api_url = '<api url>'
secret_key = '<secret key'

'''
# Show the image from url
def plt_imshow(title='image', img=None, figsize=(8 ,5)):
    plt.figure(figsize=figsize)
 
    if type(img) == list:
        if type(title) == list:
            titles = title
        else:
            titles = []
 
            for i in range(len(img)):
                titles.append(title)
 
        for i in range(len(img)):
            if len(img[i].shape) <= 2:
                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_GRAY2RGB)
            else:
                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_BGR2RGB)
 
            plt.subplot(1, len(img), i + 1), plt.imshow(rgbImg)
            plt.title(titles[i])
            plt.xticks([]), plt.yticks([])
 
        plt.show()
    else:
        if len(img.shape) < 3:
            rgbImg = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        plt.imshow(rgbImg)
        plt.title(title)
        plt.xticks([]), plt.yticks([])
        plt.show()

# put the text in test Image
def put_text(image, text, x, y, color=(0, 255, 0), font_size=22):
    if type(image) == np.ndarray:
        color_coverted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(color_coverted)
    print('platform.system() : ',platform.system())
    if platform.system() == 'Darwin':
        font = 'AppleGothic.ttf'
    elif platform.system() == 'Windows':
        font = 'malgun.ttf'
    else:
        #font = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 40)
        font = "Tests/fonts/FreeMono.ttf"

    image_font = ImageFont.truetype(font, font_size)
    font = ImageFont.load_default()
    draw = ImageDraw.Draw(image)
 
    draw.text((x, y), text, font=image_font, fill=color)
    
    numpy_image = np.array(image)
    opencv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
 
    return opencv_image
    
# check the ocr result by showing image with ocr text
def check_result(result, img):
    roi_img = img.copy()
 
    for field in result['images'][0]['fields']:
        text = field['inferText']
        vertices_list = field['boundingPoly']['vertices']
        pts = [tuple(vertice.values()) for vertice in vertices_list]
        topLeft = [int(_) for _ in pts[0]]
        topRight = [int(_) for _ in pts[1]]
        bottomRight = [int(_) for _ in pts[2]]
        bottomLeft = [int(_) for _ in pts[3]]
    
        cv2.line(roi_img, topLeft, topRight, (0,255,0), 2)
        cv2.line(roi_img, topRight, bottomRight, (0,255,0), 2)
        cv2.line(roi_img, bottomRight, bottomLeft, (0,255,0), 2)
        cv2.line(roi_img, bottomLeft, topLeft, (0,255,0), 2)
        roi_img = put_text(roi_img, text, topLeft[0], topLeft[1] - 10, font_size=30)
    
        print(text)
    
    plt_imshow(["Original", "ROI"], [img, roi_img], figsize=(16, 10))

'''
# download image in url
def download_image(image_url, path):
    res = requests.get(image_url)
    img = Image.open(BytesIO(res.content))
    img.save(path)
    files = [('file', open(path,'rb'))]
    if os.path.isfile(path):
        os.remove(path)
    return cv2.imread(path), files

# request ocr info by calling Clova API
def request_ocr(files):
    request_json = {'images': [{'format': 'jpg',
                                'name': 'demo'
                               }],
                    'requestId': str(uuid.uuid4()),
                    'version': 'V2',
                    'timestamp': int(round(time.time() * 1000))
                   }
 
    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    
    headers = {
    'X-OCR-SECRET': secret_key,
    }
    
    response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
    result = response.json()
    return result

# fill output by using OCR result
def fill_output(ocr_info):
    output = {}

    output['is_corporate'] = True if ocr_info['taxType'][0]['text'] == "법인사업자" else False
    # it returns only number not hyphen
    output['company_biz_number'] = ocr_info['registerNumber'][0]['text']
    if output['is_corporate'] == True:
        output['company_name'] = ocr_info['corpName'][0]['text']
        output['corporate_regis_number'] = ocr_info['corpRegisterNum'][0]['text']
    else:
        output['owner_birthdate'] = ocr_info['birth'] [0]['text']
        output['company_name'] = ocr_info['companyName'][0]['text']
    output['owner_name'] = ocr_info['repName'][0]['text']
    output['open_date'] = ocr_info['openDate'][0]['text']
    output['address'] = ocr_info['bisAddress'][0]['text']
    return output

# Get ocr information by using image url, file_name, img_type
def get_ocr_scan(image_url, file_name = 'biz', img_type = 'jpg'):
    path = file_name + '.' + img_type
    image, files = download_image(image_url, path)
    result = request_ocr(files)
    ocr_info = result['images'][0]['bizLicense']['result']
    output = fill_output(ocr_info)
    return output

