# Generated by Django 5.0.1 on 2024-02-01 15:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Users", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Departments",
            new_name="Department",
        ),
    ]
