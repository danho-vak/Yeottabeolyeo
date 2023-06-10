import json

from django.conf import settings
from django.db.models import QuerySet, TextChoices
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from map.models import Box


class MainView(TemplateView):
    template_name = "map/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["SGIS_CONSUMER_KEY"] = settings.SGIS_CONSUMER_KEY
        context["SGIS_CONSUMER_SECRET"] = settings.SGIS_CONSUMER_SECRET
        context["VWORLD_KEY"] = settings.VWORLD_KEY
        return context


class AjaxGetPinView(View):
    def getPinsInSquare(self, data: dict) -> list:
        """
        사각형 안에 있는 수거함 데이터 반환
        """

        kwargs = {
            "x__gte": data["xStart"],
            "x__lte": data["xEnd"],
            "y__gte": data["yStart"],
            "y__lte": data["yEnd"],
        }

        # 특정 type의 데이터 요청 파라미터 있다면 검색 kwargs에 추가
        if data.get('type'):
            kwargs['type'] = data['type']

        result_values_qs = Box.objects.filter(**kwargs).values().distinct()
        # 데이터가 없으면 빈 리스트 반환
        if not result_values_qs:
            return []

        # 200개 이상이면 반환하지 않음
        if result_values_qs.count() >= 200:
            return []

        # QS -> list
        return list(result_values_qs)

    def get(self, request, *args, **kwargs):
        """
        xStart, xEnd, yStart, yEnd 파라미터를 받아서 사각형 안에 있는 수거함 데이터 반환 API
        """

        # 필수 파라미터가 없으면 에러 반환
        check_list = ["xStart", "xEnd", "yStart", "yEnd"]
        for key in check_list:
            if key not in request.GET:
                return JsonResponse({"result": "fail", "msg": "잘못된 요청"}, status=400)

        # 필수 파라미터가 있으면 데이터 반환
        data = {}
        if result_list := self.getPinsInSquare(request.GET):
            data = result_list
        return JsonResponse({"result": "success", "data": data}, status=200)

