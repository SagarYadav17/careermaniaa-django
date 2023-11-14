from contextlib import suppress

from django.core.cache import cache
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from phonenumber_field.phonenumber import PhoneNumber

from authentication.models import User
from authentication.serializers import UserSerializer, UserProfileUpdateSerializer
from authentication.utils import create_auth_otp
from core.utils import get_object_or_error
from core.tasks import send_sms


class UserRegistraionAPI(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


class LoginUsingOTPAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, phonenumber):
        with suppress(User.DoesNotExist):
            get_object_or_error(User, phonenumber=PhoneNumber.from_string(phonenumber))
            otp, expired_sec = create_auth_otp(key=f"login-otp-{phonenumber}", otp_length=4)
            send_sms(f"Your Careermaniaa OTP is {otp}. Valid for {int(expired_sec / 60)} Minutes", phonenumber)

        return Response({"message": "New OTP is generated"})

    def post(self, request, phonenumber):
        otp = request.data.get("otp")

        if not otp:
            raise ValidationError("OTP is required")

        with suppress(User.DoesNotExist):
            user_obj = User.objects.get(phonenumber=PhoneNumber.from_string(phonenumber))

        queryset = cache.get(f"login-otp-{phonenumber}")
        if queryset and queryset == otp:
            cache.delete(f"login-otp-{phonenumber}")
            refresh = RefreshToken.for_user(user_obj)
            return Response({"refresh": str(refresh), "access": str(refresh.access_token)})

        return Response({"detail": "Invalid OTP"}, status=HTTP_400_BAD_REQUEST)


class UserProfileUpdateAPI(RetrieveUpdateAPIView):
    serializer_class = UserProfileUpdateSerializer

    def get_object(self):
        return self.request.user
