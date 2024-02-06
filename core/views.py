from contextlib import suppress
import json

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.models import City, Country, Expertise, Language, State, Locality
from core.serializers import (
    CitySerializer,
    CountrySerializer,
    ExpertiseSerializer,
    LanguageSerializer,
    LocalitySerializer,
    StateSerializer,
)

from core.tasks import create_sms_logs


class CountryListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Country.objects.filter()
    serializer_class = CountrySerializer
    filter_backends = (SearchFilter,)
    search_fields = ("name",)


class StateListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = State.objects.filter()
    serializer_class = StateSerializer
    filter_backends = (SearchFilter,)
    search_fields = ("name",)


class CityListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = City.objects.filter()
    serializer_class = CitySerializer
    filter_backends = (SearchFilter,)
    search_fields = ("name",)


class LanguageListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Language.objects.filter()
    serializer_class = LanguageSerializer
    filter_backends = (SearchFilter,)
    search_fields = ("name_en",)

    @method_decorator(cache_page(settings.DEFAULT_CACHE_TIMEOUT))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ExpertiseListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Expertise.objects.filter(is_active=True)
    serializer_class = ExpertiseSerializer
    filter_backends = (SearchFilter,)
    search_fields = ("name",)

    @method_decorator(cache_page(settings.DEFAULT_CACHE_TIMEOUT))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class LocalityListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Locality.objects.filter()
    serializer_class = LocalitySerializer
    filter_backends = (SearchFilter,)
    search_fields = ("pincode",)


class SMSWebhook(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, provider):
        with suppress(Exception):
            create_sms_logs(json.dumps(request.query_params), provider)
        return Response()

    def post(self, request, provider):
        with suppress(Exception):
            create_sms_logs(json.dumps(request.data), provider)
        return Response()
