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
from core.models import Expertise
from core.serializers import (
    CityMongoSerializer,
)

from core.tasks import create_sms_logs


class ExpertiseListAPI(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Expertise.objects.filter(is_active=True)
    # serializer_class = ExpertiseSerializer
    filter_backends = (SearchFilter,)
    search_fields = ("name",)

    def get_queryset(self):
        self.pagination_class = check_pagination(self.request.query_params)
        return super().get_queryset()

    @method_decorator(cache_page(settings.DEFAULT_CACHE_TIMEOUT))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CitySearchAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CityMongoSerializer

    def get(self, request):
        query = request.query_params.get("query")

        if not query:
            return Response({"error": "query is required"})

        queryset = settings.MONGO_CLIENT.perform_search("city", query, "city")

        data = self.serializer_class(queryset, many=True).data

        return Response(data)


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
