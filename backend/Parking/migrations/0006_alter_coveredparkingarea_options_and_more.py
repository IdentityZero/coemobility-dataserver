# Generated by Django 5.0.1 on 2024-02-10 13:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Parking", "0005_alter_coveredparkingarea_area"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="coveredparkingarea",
            options={
                "verbose_name": "Covered Parking Area",
                "verbose_name_plural": "Covered Parking Areas",
            },
        ),
        migrations.AlterModelOptions(
            name="parking",
            options={"verbose_name": "Parking", "verbose_name_plural": "Parkings"},
        ),
        migrations.AlterModelOptions(
            name="unregisteredparking",
            options={
                "verbose_name": "Unregistered RFID Parking",
                "verbose_name_plural": "Unregistered RFID Parkings",
            },
        ),
        migrations.RenameField(
            model_name="coveredparkingarea",
            old_name="area",
            new_name="area_name",
        ),
    ]
