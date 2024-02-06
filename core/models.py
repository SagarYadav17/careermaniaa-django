import uuid
from django.db import models


class TimestampedModel(models.Model):
    # A universally unique identifier for this object.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

        # By default, any model that inherits from `TimestampedModel` should
        # be ordered in reverse-chronological order. We can override this on a
        # per-model basis as needed, but reverse-chronological is a good
        # default ordering for most models.
        ordering = ["-created_at"]


class Country(TimestampedModel):
    name = models.CharField(max_length=255)
    iso3 = models.CharField(max_length=3, unique=True)
    iso2 = models.CharField(max_length=2, unique=True)
    numeric_code = models.IntegerField(unique=True)
    phone_code = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    subregion = models.CharField(max_length=100)
    currency_name = models.CharField(max_length=100)
    currency_symbol = models.CharField(max_length=10)
    emoji = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class State(TimestampedModel):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state_code = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return "%s: %s" % (self.name, self.country.name)


class City(TimestampedModel):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return "%s: %s: %s" % (self.name, self.state.name, self.state.country.name)


class Locality(TimestampedModel):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    district = models.CharField(max_length=255, blank=True, null=True)
    division = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return "%s: %s: %s" % (self.name, self.state.name, self.pincode)


class Expertise(TimestampedModel):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class Language(TimestampedModel):
    iso_639_1 = models.CharField(max_length=2, unique=True, blank=True)
    iso_639_2T = models.CharField(max_length=3, unique=True, blank=True)
    iso_639_2B = models.CharField(max_length=3, unique=True, blank=True)
    iso_639_3 = models.CharField(max_length=3, blank=True)
    name_en = models.CharField(max_length=100)
    name_native = models.CharField(max_length=100)
    family = models.CharField(max_length=50)

    class Meta:
        ordering = ["name_en"]

    def __str__(self):
        return self.name_en


class SMSLog(TimestampedModel):
    provider = models.TextField(max_length=20)
    log = models.TextField(default="")

    def __str__(self):
        return self.created_at
