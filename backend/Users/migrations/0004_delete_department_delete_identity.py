# Generated by Django 5.0.1 on 2024-02-02 01:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Users", "0003_identity"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Department",
        ),
        migrations.DeleteModel(
            name="Identity",
        ),
    ]