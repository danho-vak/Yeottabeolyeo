import csv
import time

import requests

from django.contrib.postgres.fields import ArrayField
from django.db import models


class BoxType(models.TextChoices):
    """
    수거함 타입 정의
    """

    clothes = "C", "의류수거함"
    battery = "B", "폐전지수거함"


class Box(models.Model):
    """
    수거함 모델 정의
    """

    class Meta:
        verbose_name = "수거함"

    district = models.CharField(max_length=50, verbose_name="행정구역")
    lot_address = models.CharField(max_length=200, verbose_name="지번주소", null=True)
    load_address = models.CharField(max_length=200, verbose_name="도로명주소", null=True)
    address_detail = models.CharField(max_length=200, verbose_name="상세주소", null=True, blank=True)
    x = models.FloatField(verbose_name="X 좌표")
    y = models.FloatField(verbose_name="Y 좌표")
    type = models.CharField(max_length=50, choices=BoxType.choices, verbose_name="수거함타입")

    def __str__(self):
        return self.lot_address or self.load_address

def save_box_data(file_path: str):
    """
    수거함 데이터 저장
    이 함수는 직접 실행함
    """

    ACCESS_TOKEN = ""

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
        time.sleep(0.8)

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

    def process(_file_path):
        csv_file = open(_file_path, 'r')
        reader = csv.reader(csv_file)

        for i, row in enumerate(reader):
            district = row[0]
            lot_address = replace_nbsp(row[1])
            load_address = replace_nbsp(row[2])

            # 지번 주소가 없으면 도로명 주소로 대체
            search_address = lot_address or load_address

            is_success, result_code = get_geo_data(search_address)

            # 지번 주소가 없고, 도로명 주소로 검색했는데도 실패하면
            if not is_success and lot_address:
                address_number = search_address.split("동 ")[-1]
                alternative_address = f"{district} {address_number}"

                # 행정구 + 지번 주소번호로 재검색 시도
                time.sleep(1)
                is_success, result_code = get_geo_data(alternative_address)

            if is_success:
                Box(
                    district=district,
                    lot_address=lot_address,
                    load_address=load_address,
                    x=result_code["x"],
                    y=result_code["y"],
                    type=BoxType.battery).save()

    # 실행부
    try:
        ACCESS_TOKEN = get_access_token()
        process(file_path)

    except Exception as e:
        print('*'*40)
        print(e)
        print('*'*40)
        import logging
        logger = logging.getLogger("default")
        logger.error(e)
