import traceback
from django.utils import timezone
import pymongo
from contextlib import suppress

from config.envs import MONGO_ENDPOINT, MONGO_DB_NAME, DEBUG_MODE

# Assuming you have a global MongoDB connection pool for better performance and reusability.
# Initialize the connection pool somewhere in your Django app.
mongo_client = pymongo.MongoClient(MONGO_ENDPOINT)
mongo_db = mongo_client[MONGO_DB_NAME]
log_collection = mongo_db["logs"]


class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.initial_body = self.decode_request_body(request.body)
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        data = {
            "timestamp": timezone.now(),
            "method": request.method,
            "url": request.path,
            "user": request.user.username if request.user else None,
            "body": self.initial_body,
            "traceback": traceback.format_exc().strip(),
        }

        with suppress(Exception):
            if not DEBUG_MODE:
                log_collection.insert_one(data)

        return None

    @staticmethod
    def decode_request_body(body):
        try:
            return body.decode("utf-8")
        except UnicodeDecodeError:
            # Handle decoding errors gracefully. Return a fallback representation or an empty string.
            return "[Decoding Error]"
