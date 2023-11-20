from django.contrib import admin
from core.models import State, City


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "state")
