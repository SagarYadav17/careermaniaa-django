from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import CharField, ModelSerializer

from authentication.models import Profile, User, Usergroup
from authentication.utils import create_auth_otp


class UserSerializer(ModelSerializer):
    username = CharField(required=False)
    password = CharField(validators=[validate_password], write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "created_at", "phonenumber", "password")

    def create(self, validated_data):
        usergroup_obj = Usergroup.objects.get_or_create(name="default")[0]
        obj = User.objects.create_user(
            username=validated_data["phonenumber"],
            phonenumber=validated_data["phonenumber"],
            usergroup=usergroup_obj,
            password=validated_data["password"],
        )

        create_auth_otp(key=f"login-otp-{obj.phonenumber}", otp_length=4)
        return obj


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        exclude = ("is_active",)


class UserProfileUpdateSerializer(ModelSerializer):
    password = CharField(write_only=True, validators=[validate_password])
    profile = ProfileSerializer()

    class Meta:
        model = User
        exclude = (
            "created_at",
            "updated_at",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "last_login",
            "user_permissions",
        )
        read_only_fields = ("phonenumber", "usergroup")

    def update(self, instance, validated_data):
        profile_data = validated_data.get("profile", {})
        profile = Profile.objects.get(id=instance.profile_id)

        # User Model
        instance.username = validated_data.get("username", instance.username)

        # Profile Model
        profile.name = profile_data.get("name", profile.name)
        profile.city = profile_data.get("city", profile.city)
        profile.whatsapp_number = profile_data.get("whatsapp_number", profile.whatsapp_number)
        profile.pan_number = profile_data.get("pan_number", profile.pan_number)
        profile.gstin = profile_data.get("gstin", profile.gstin)
        profile.email = profile_data.get("email", profile.email)
        profile.year_of_establishment = profile_data.get("year_of_establishment", profile.year_of_establishment)

        profile.name = profile_data.get("name", profile.name)
        profile.language.set(profile_data.get("language", profile.language.all()))

        profile.save()
        instance.save()
        return instance
