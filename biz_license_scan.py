from ocr_scan import get_ocr_scan
from biz_status import get_biz_status

# orc_scan.py를 통해 사업자등록증 이미지를 스캔한 다음
# biz_status.py로 사업자 상태를 조회하고 
# 두 결과를 조합하여 반환

'''
	input : 
			image_url (string)
	output : {
		"is_corporate" : boolean,  # 개인사업자 : False, 법인사업자 : True
        "company_name" : str,      # 사업자 상호
        "company_biz_number" : str,   # 사업자등록번호
        "corporate_regis_number" : str,    # 법인등록번호(법인사업자만)
        "owner_name" : str,          # 대표자 성명
        "onwer_birthdate" : str,     # 대표자 생년월일(개인사업자만), "0000-00-00"
		"open_date" : str,         # 개업연월일
		"address" : str,           # (개인)사업장 주소, (법인)사업장 소재지
		"is_active" : boolean,     # 사업장 영업중 여부
	}

'''

def biz_license_scan(url):
    ocr_info = get_ocr_scan(url)
    biz_number = ocr_info['company_biz_number']
    biz_status = get_biz_status(biz_number)
    ocr_info["is_active"] = biz_status["is_active"]
    #ocr_info.update(biz_status)
    return ocr_info


