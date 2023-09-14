from rest_framework.serializers import CharField, ModelSerializer

from core.models import City, Country, Expertise, Language, Locality, State


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class StateSerializer(ModelSerializer):
    country_name = CharField(source="country.name", read_only=True)

    class Meta:
        model = State
        fields = "__all__"


class CitySerializer(ModelSerializer):
    state_name = CharField(source="state.name", read_only=True)
    country_name = CharField(source="state.country.name", read_only=True)

    class Meta:
        model = City
        fields = "__all__"


class LanguageSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"


class ExpertiseSerializer(ModelSerializer):
    class Meta:
        model = Expertise
        fields = "__all__"


class LocalitySerializer(ModelSerializer):
    class Meta:
        model = Locality
        fields = "__all__"
