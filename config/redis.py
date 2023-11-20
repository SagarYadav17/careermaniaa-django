from django_redis import get_redis_connection
from django.conf import settings


r = get_redis_connection()


def set_json(index_name, data):
    r.json().set(index_name, "$", data)


def get_json(index_name):
    data = r.json().get(index_name, "$")
    return data[0] if data else {}


settings.FEATURE_FLAGS = get_json("feature_flags")
