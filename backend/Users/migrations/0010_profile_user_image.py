# Generated by Django 5.0.1 on 2024-02-02 14:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Users", "0009_alter_profile_user_department_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="user_image",
            field=models.ImageField(default="profile.png", upload_to="profile_pics"),
        ),
    ]
