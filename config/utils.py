from rest_framework.pagination import PageNumberPagination


def check_pagination(request: dict):
    if request.get("pagination") == "all":
        return None

    return PageNumberPagination
