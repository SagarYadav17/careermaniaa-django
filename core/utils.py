import re

from rest_framework.exceptions import NotFound


def get_object_or_error(model, *args, **kwargs):
    try:
        obj = model.objects.get(*args, **kwargs)
        return obj
    except model.DoesNotExist:
        model_name = " ".join(re.findall("[A-Z][^A-Z]*", model.__name__))
        raise NotFound(detail="{} not found".format(model_name))


def is_valid_pan(pan):
    pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$"
    return bool(re.match(pattern, pan))
