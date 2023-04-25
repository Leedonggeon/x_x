# 사업자등록번호를 바탕으로 사업자 상태 조회를 한 후 결과를 반환하는 것
# 사업자 상태조회 API 가이드는 아래 참고

import requests
import json

'''
input : 
    company_biz_number (string)      # 000-00-00000 형태
output : 
    {
				"is_active" : boolean,     # b_stt == 01 (01: 계속사업자) 인 경우만 true
        "status" : string,         # 계속사업자 / 휴업자 / 폐업자 중 한글로 반환
        "tax_type" : string,       # 과세사업자 일반과세자 등 API 결과를 한글로 그대로 반환
        "end_date" : string,       # 0000-00-00 형태로 폐업일자 반환
		}

'''

serviceKey = "<service key>"

# 국세청 제공 사업자등록번호 상태조회 API 호출해서 결과를 가져오는 함수
def request_biz_status(biz_number):
    headers = {
        'accept': 'application/json',
        'Authorization': serviceKey,
        'Content-Type': 'application/json',
            }
    param = {'serviceKey': serviceKey}
    data = '{"b_no":["'+biz_number+'"]}'
    
    res = requests.post('https://api.odcloud.kr/api/nts-businessman/v1/status', headers = headers, params=param, data=data)
    return res.json()["data"]

# business status 01, 02, 03에 따른 "계속사업자", "휴업자", "폐업자"를 반환하는 함수
def get_status(b_stt):
    if b_stt == "01":
        return '계속사업자'
    elif b_stt == "02":
        return '휴업자'
    else:
        return '폐업자'

# 사업자등록 번호를 받아 최상단 결과를 반환하는 함수
def get_biz_status(biz_number):
    processed_biz_number = biz_number.replace('-', '')
    res = request_biz_status(processed_biz_number)
    output = {}
    output['is_active'] = True if res[0]['b_stt_cd'] == "01" else False
    output['status'] = res[0]['b_stt']
    output['tax_type'] = res[0]["tax_type"]
    output['end_date'] = res[0]['end_dt']
    return output