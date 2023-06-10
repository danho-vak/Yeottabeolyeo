import csv
import time

import requests


ACCESS_TOKEN = ''

def get_access_token():
    url = "https://sgisapi.kostat.go.kr/OpenAPI3/auth/authentication.json"
    response = requests.get(url, params={
        "consumer_key": "8a274d0e9319443980ac",
        "consumer_secret": "0c5a83fe3bb34d97abf4",
    })
    return response.json()['result']['accessToken']

def get_geo_data(address) -> (bool, dict):
    url = "https://sgisapi.kostat.go.kr/OpenAPI3/addr/geocode.json"
    response = requests.get(url, params={
        "accessToken": ACCESS_TOKEN,
        "address": address,
    })

    # 결과 반환 값 dict
    result = {"x": "", "y": ""}
    # 응답 코드가 200이 아니면 반환
    if response.status_code != 200:
        return False, result

     # 응답 json을 dict로 변환
    result_json = response.json()

    # 응답 json의 errCd가 0보다 작으면 반환
    if result_json["errCd"] < 0:
        return False, result

    # 응답 json의 resultData를 반환
    result_data = result_json["result"]["resultdata"]
    data = result_data[0]
    result["x"] = data["x"]
    result["y"] = data["y"]
    return True, result

def replace_nbsp(value):
    return value.replace('\xa0', ' ')

def __main__():
    csv_file = open('c_box_total.csv', 'r')
    reader = csv.reader(csv_file)

    for i, row in enumerate(reader):
        district = row[0]
        lot_address = replace_nbsp(row[1])
        load_address = replace_nbsp(row[2])

        # 지번 주소가 없으면 도로명 주소로 대체
        search_address = lot_address or load_address
        time.sleep(1)
        is_success, result_code = get_geo_data(search_address)

        # 지번 주소가 없고, 도로명 주소로 검색했는데도 실패하면
        if not is_success and lot_address:
            address_number = search_address.split("동 ")[-1]
            alternative_address = f"{district} {address_number}"

            # 행정구 + 지번 주소번호로 재검색 시도
            time.sleep(1)
            is_success, result_code = get_geo_data(alternative_address)

        # Test Code START
        # 작성자 : 박상준
        # 작성일 : 2023-05-29
        print('*'*40)
        print("address : ", lot_address or load_address)
        print("result_code : ", result_code)
        print('*'*40)
        # Test code END

        if i == 10:
            break

if __name__ == '__main__':
    ACCESS_TOKEN = get_access_token()
    try:
        __main__()
    except Exception as e:
        print(e)
