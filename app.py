from biz_license_scan import biz_license_scan
from ocr_scan import get_ocr_scan
from biz_status import get_biz_status



# Test for get_ocr_scan

# 개인사업자
#image_url = 'http://m.orderplus.co.kr/media/survey/20230322/25290fa62474db9d5cffcb059d7cca16dd40e4fd/033233/006C4B3D-29D6-4CB8-A003-A890D3A45891.jpeg'
# 법인사업자
image_url = 'http://m.orderplus.co.kr/media/survey/20230326/2b61d2d9b8dc451540b7f8feed265a8a8c94a53c/070700/A55AB285-8AF0-41BA-BC40-24796037DF11.jpeg'

ocr_info = get_ocr_scan(image_url)
print(ocr_info)

# Test for get_biz_status
biz_status = get_biz_status(ocr_info["company_biz_number"])
print(biz_status)

# Test for biz_license_scan

biz_license = biz_license_scan(image_url)
print(biz_license)