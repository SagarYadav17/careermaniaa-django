import json
from decimal import Decimal
from django_redis import get_redis_connection
from redis.exceptions import ResponseError
from redis.commands.json.path import Path
from redis.commands.search.field import TextField, NumericField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from django.conf import settings
from rest_framework.exceptions import NotFound


r = get_redis_connection()


class RedisIndexingMixin:
    def create_redis_index(self):
        index_name = self._meta.model_name
        data = self.__dict__.copy()
        data.pop("_state", None)

        schema = []
        for key, value in data.items():
            if isinstance(value, Decimal):
                data[key] = float(value)

            if isinstance(value, (int, float)):
                schema.append(NumericField(f"$.{key}", as_name=key))
            else:
                data[key] = str(value)
                schema.append(TextField(f"$.{key}", as_name=key))

        index = r.ft(index_name)

        try:
            index.create_index(
                schema,
                definition=IndexDefinition(prefix=[f"{index_name}:"], index_type=IndexType.JSON),
            )
        except ResponseError as e:
            if "Index already exists" not in e.args:
                raise e

        r.json().set(f"{index_name}:{self.id}", Path.root_path(), data)

    def delete_redis_index(self):
        index_name = self._meta.model_name
        r.delete(f"{index_name}:{self.id}")


def set_json(index_name, data):
    r.json().set(index_name, "$", data)


def get_json(index_name):
    data = r.json().get(index_name, "$")
    return data[0] if data else {}


def query_redis_index(index_name, query="*"):
    index = r.ft(index_name)

    try:
        result = index.search(Query(query))
    except ResponseError as e:
        raise NotFound(e.args)

    data = {
        "count": result.total,
        "results": [],
    }

    for doc in result.docs:
        data["results"].append(json.loads(doc.json))

    return data


settings.FEATURE_FLAGS = get_json("feature_flags")
