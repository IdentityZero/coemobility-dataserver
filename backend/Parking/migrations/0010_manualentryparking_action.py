# Generated by Django 5.0.1 on 2024-03-01 20:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Parking", "0009_alter_manualentryparking_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="manualentryparking",
            name="action",
            field=models.CharField(
                choices=[("in", "In"), ("out", "Out")], default="in", max_length=3
            ),
        ),
    ]