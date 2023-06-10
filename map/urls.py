from django.urls import path

from map import views

app_name = "map"
urlpatterns = [
    path("", views.MainView.as_view(), name="main"),
    path("api/pin/", views.AjaxGetPinView.as_view(), name="get_pin"),
]
