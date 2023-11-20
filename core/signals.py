from rest_framework import serializers
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings

from core.models import City


mongo_client = settings.MONGO_CLIENT


class CitySerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    name = serializers.ReadOnlyField()
    state = serializers.ReadOnlyField(source="state.id")
    district = serializers.ReadOnlyField()
    division = serializers.ReadOnlyField()
    region = serializers.ReadOnlyField()
    pincode = serializers.ReadOnlyField()
    state_name = serializers.ReadOnlyField(source="state.name")

    class Meta:
        model = City
        fields = "__all__"


@receiver(post_save, sender=City)
def upload_data_in_mongo(sender, instance, created, *args, **kwargs):
    mongo_client.update_one(
        "city",
        {"id": instance.id},
        {"$set": CitySerializer(instance).data},
        upsert=True,
    )
