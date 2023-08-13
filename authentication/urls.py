from django.urls import path

from authentication import views

urlpatterns = [
    path("register/", views.UserRegistraionAPI.as_view(), name="auth-register"),
    path("otp-login/<str:phonenumber>/", views.LoginUsingOTPAPI.as_view(), name="auth-otp-login"),
    path("user/me/", views.UserProfileUpdateAPI.as_view(), name="auth-user-profile-update"),
]
