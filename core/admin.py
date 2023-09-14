from django.contrib import admin
from core.models import Country, State, City, Locality


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country")


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "state")


@admin.register(Locality)
class LocalityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "state")
