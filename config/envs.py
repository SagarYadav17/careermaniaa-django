from config import infisical

environ = infisical.get_secrets()

DJANGO_SECRET_KEY = environ.get("DJANGO_SECRET_KEY", "e!%qy(nxwz-fs7lfuvv70uvx@@^8qizcn!cr-d^wh-h2shq2j6")

DEBUG_MODE = environ.get("DEBUG_MODE", False)
STACK = environ.get("STACK", "development")

# Postgres Main DB Credentials
DB_HOST = environ.get("DB_HOST", "127.0.0.1")
DB_NAME = environ.get("DB_NAME", "postgres")
DB_USER = environ.get("DB_USER", "postgres")
DB_PASSWORD = environ.get("DB_PASSWORD", "postgres")
DB_PORT = environ.get("DB_PORT", 5432)

# Redis Credentials
REDIS_USERNAME = environ.get("REDIS_USERNAME", "default")
REDIS_PASSWORD = environ.get("REDIS_PASSWORD", "default")
REDIS_URL = environ.get("REDIS_URL", "127.0.0.1:6379")
REDIS_ENDPOINT = environ.get("REDIS_ENDPOINT", f"redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_URL}")

# Mongo DB Credentials
MONGO_USERNAME = environ.get("MONGO_USERNAME", "admin")
MONGO_PASSWORD = environ.get("MONGO_PASSWORD", "password")
MONGO_HOST = environ.get("MONGO_HOST", "127.0.0.1:27017")
MONGO_ENDPOINT = environ.get("MONGO_ENDPOINT", f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}/")
MONGO_DB_NAME = environ.get("MONGO_DB_NAME", STACK)

# Twilio Credentials
TWILIO_ACCOUNT_SID = environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = environ.get("TWILIO_AUTH_TOKEN")
TWILIO_CALLBACK_URL = environ.get("TWILIO_CALLBACK_URL")
TWILIO_FROM_NUMBER = environ.get("TWILIO_FROM_NUMBER")
