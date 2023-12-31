# Generated by Django 4.2.4 on 2023-09-02 18:27

import config.redis
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Country",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("iso3", models.CharField(max_length=3, unique=True)),
                ("iso2", models.CharField(max_length=2, unique=True)),
                ("numeric_code", models.IntegerField(unique=True)),
                ("phone_code", models.CharField(max_length=100)),
                ("region", models.CharField(max_length=100)),
                ("subregion", models.CharField(max_length=100)),
                ("currency_name", models.CharField(max_length=100)),
                ("currency_symbol", models.CharField(max_length=10)),
                ("emoji", models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                "ordering": ["name"],
            },
            bases=(config.redis.RedisIndexingMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Expertise",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, unique=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Language",
            fields=[
                ("iso_639_1", models.CharField(max_length=2, primary_key=True, serialize=False)),
                ("iso_639_2T", models.CharField(blank=True, max_length=3, unique=True)),
                ("iso_639_2B", models.CharField(blank=True, max_length=3, unique=True)),
                ("iso_639_3", models.CharField(blank=True, max_length=3)),
                ("name_en", models.CharField(max_length=100)),
                ("name_native", models.CharField(max_length=100)),
                ("family", models.CharField(max_length=50)),
            ],
            options={
                "ordering": ["name_en"],
            },
            bases=(config.redis.RedisIndexingMixin, models.Model),
        ),
        migrations.CreateModel(
            name="SMSLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("provider", models.TextField(max_length=20)),
                ("log", models.TextField(default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="State",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("state_code", models.CharField(max_length=255)),
                ("latitude", models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ("longitude", models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ("country", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.country")),
            ],
            options={
                "ordering": ["name"],
            },
            bases=(config.redis.RedisIndexingMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Locality",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("district", models.CharField(blank=True, max_length=255, null=True)),
                ("division", models.CharField(blank=True, max_length=255, null=True)),
                ("pincode", models.CharField(max_length=6)),
                ("state", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.state")),
            ],
            options={
                "ordering": ["name"],
            },
            bases=(config.redis.RedisIndexingMixin, models.Model),
        ),
        migrations.CreateModel(
            name="City",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("latitude", models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ("longitude", models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ("state", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="core.state")),
            ],
            options={
                "ordering": ["name"],
            },
            bases=(config.redis.RedisIndexingMixin, models.Model),
        ),
    ]
