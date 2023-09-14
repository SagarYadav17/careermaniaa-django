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

from config.utils import check_pagination
from core.models import City, Country, Expertise, Language, State, Locality
from core.serializers import (
    CitySerializer,
    CountrySerializer,
    ExpertiseSerializer,
    LanguageSerializer,
    LocalitySerializer,
    StateSerializer,
)

from config.redis import query_redis_index
from core.tasks import create_sms_logs


class CountryListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Country.objects.filter()
    serializer_class = CountrySerializer
    filter_backends = (SearchFilter,)
    search_fields = ("name",)

    def get_queryset(self):
        self.pagination_class = check_pagination(self.request.query_params)
        return super().get_queryset()

    def get(self, request):
        search = request.query_params.get("search")
        if settings.FEATURE_FLAGS.get("use_redis_search"):
            data = query_redis_index("country", search or "*")
            return Response(data)

        return super().get(request)


class StateListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = State.objects.filter()
    serializer_class = StateSerializer
    filter_backends = (SearchFilter,)
    search_fields = ("name",)

    def get_queryset(self):
        self.pagination_class = check_pagination(self.request.query_params)
        return super().get_queryset()

    def get(self, request):
        search = request.query_params.get("search")
        if settings.FEATURE_FLAGS.get("use_redis_search"):
            data = query_redis_index("state", search or "*")
            return Response(data)

        return super().get(request)


class CityListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = City.objects.filter()
    serializer_class = CitySerializer
    filter_backends = (SearchFilter,)
    search_fields = ("name",)

    def get_queryset(self):
        self.pagination_class = check_pagination(self.request.query_params)
        return super().get_queryset()

    def get(self, request):
        search = request.query_params.get("search")
        if settings.FEATURE_FLAGS.get("use_redis_search"):
            data = query_redis_index("city", search or "*")
            return Response(data)

        return super().get(request)


class LanguageListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Language.objects.filter()
    serializer_class = LanguageSerializer
    filter_backends = (SearchFilter,)
    search_fields = ("name_en",)

    def get_queryset(self):
        self.pagination_class = check_pagination(self.request.query_params)
        return super().get_queryset()

    @method_decorator(cache_page(settings.DEFAULT_CACHE_TIMEOUT))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ExpertiseListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Expertise.objects.filter(is_active=True)
    serializer_class = ExpertiseSerializer
    filter_backends = (SearchFilter,)
    search_fields = ("name",)

    def get_queryset(self):
        self.pagination_class = check_pagination(self.request.query_params)
        return super().get_queryset()

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
            create_sms_logs.delay(json.dumps(request.query_params), provider)
        return Response()

    def post(self, request, provider):
        with suppress(Exception):
            create_sms_logs.delay(json.dumps(request.data), provider)
        return Response()
