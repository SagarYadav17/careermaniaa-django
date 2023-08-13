from django.urls import path

from core import views

urlpatterns = [
    path("country/", views.CountryListAPI.as_view(), name="core-country"),
    path("state/", views.StateListAPI.as_view(), name="core-state"),
    path("city/", views.CityListAPI.as_view(), name="core-city"),
    path("language/", views.LanguageListAPI.as_view(), name="core-language"),
    path("expertise/", views.ExpertiseListAPI.as_view(), name="core-expertise"),
    path("sms-webhook/<str:provider>/", views.SMSWebhook.as_view(), name="core-sms-webhook"),
]
