import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from config.upload_to_paths import BANK_DETAIL_KYC_FILES
from core.models import City, Language, TimestampedModel


class Usergroup(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class BankName(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class Profile(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=False)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, null=True)
    language = models.ManyToManyField(Language, blank=True)
    whatsapp_number = PhoneNumberField(blank=True)
    pan_number = models.CharField(max_length=10, unique=True, blank=True, null=True)
    gstin = models.CharField(max_length=15, unique=True, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    year_of_establishment = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class BankDetail(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    bank = models.ForeignKey(BankName, on_delete=models.PROTECT)
    account_holder_name = models.CharField(max_length=255)
    account_number = models.PositiveBigIntegerField()
    branch_name = models.CharField(max_length=255)
    ifsc_code = models.CharField(max_length=11)
    attachment = models.FileField(upload_to=BANK_DETAIL_KYC_FILES)

    class Meta:
        unique_together = ["profile", "bank", "account_number", "branch_name", "ifsc_code"]

    def __str__(self) -> str:
        return self.account_holder_name


class Address(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    address = models.TextField(default="")
    postal_code = models.CharField(max_length=20, default="")
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        unique_together = ["profile", "address", "postal_code", "city"]

    def __str__(self) -> str:
        return self.address


class UserManager(BaseUserManager):
    def create_user(self, username: str, password: str, phonenumber: str, usergroup: Usergroup, name: str = ""):
        profile_obj = Profile.objects.create(name=name)
        user = self.model(username=username, phonenumber=phonenumber, usergroup=usergroup, profile=profile_obj)
        user.set_password(password)
        user.is_superuser = False
        user.is_staff = False
        user.save()

        return user

    def create_superuser(self, username: str, phonenumber: str, password: str):
        usergroup_obj = Usergroup.objects.get_or_create(name="superuser")[0]
        user = self.create_user(username=username, password=password, phonenumber=phonenumber, usergroup=usergroup_obj)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(db_index=True, max_length=128, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile = models.OneToOneField(Profile, on_delete=models.PROTECT)
    usergroup = models.ForeignKey(Usergroup, on_delete=models.PROTECT)
    phonenumber = PhoneNumberField(unique=True)
    email = models.EmailField(max_length=50, unique=True, blank=True, null=True)

    USERNAME_FIELD = "phonenumber"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self) -> str:
        return self.username
