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

import pandas as pd
import os
import cv2
import urllib.request
from PIL import Image
from io import BytesIO

import requests

# Load image from image url
# Input : url 'string'
# Output : PIL.Image

def get_image(image_url):
    res = requests.get(image_url)
    img = Image.open(BytesIO(res.content))
    return img

# get ocr data from PIL.Image
# Input : PIL.Image
# Output : 

def get_ocr_info(image):

    return ocr_info



'''
def fill_output(ocr_info):
    output = {}

    output['is_corporate'] = 
    output['company_name'] = 
    output['company_biz_number'] = 
    output['owner_birthdate'] = 
    output['open_date'] = 
    output['address'= = 

    return output
'''

def get_ocr_scan(image_url):
    image = get_image(image_url)
    ocr_info = get_ocr_info(image)
    output = fill_output(ocr_info)
    return output


image_url = 'http://m.orderplus.co.kr/media/survey/20230322/04fcfbb6f5c9330155b76ce97c92fc5260b917fc/040242/ohpl_20230322_160236.jpg'
image_url = 'http://m.orderplus.co.kr/media/survey/20230322/25290fa62474db9d5cffcb059d7cca16dd40e4fd/033233/006C4B3D-29D6-4CB8-A003-A890D3A45891.jpeg'
get_ocr_scan(image_url)


'''
dir = '.상세_배송_정보_사업자등록증이미지_정보'
biz_df = pd.read_excel(dir)
print(biz_df)
'''
