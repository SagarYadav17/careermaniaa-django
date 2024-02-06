from core.models import SMSLog
from contextlib import suppress

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from config.envs import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_CALLBACK_URL, TWILIO_FROM_NUMBER


def create_sms_logs(log, provider):
    SMSLog.objects.create(log=log, provider=provider)


def send_sms(message: str, to: str) -> None:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    with suppress(TwilioRestException):
        client.messages.create(from_=TWILIO_FROM_NUMBER, body=message, to=to, status_callback=TWILIO_CALLBACK_URL)
