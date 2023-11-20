from django.urls import path

from core import views

urlpatterns = [
    # path("language/", views.LanguageListAPI.as_view(), name="core-language"),
    path("expertise/", views.ExpertiseListAPI.as_view(), name="core-expertise"),
    path("city/", views.CitySearchAPI.as_view(), name="core-city"),
    path("sms-webhook/<str:provider>/", views.SMSWebhook.as_view(), name="core-sms-webhook"),
]
