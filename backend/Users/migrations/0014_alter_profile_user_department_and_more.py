# Generated by Django 5.0.1 on 2024-03-10 22:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Users", "0013_alter_profile_user_department_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="user_department",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="Users.department",
                verbose_name="Department",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="user_identity",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="Users.identity",
                verbose_name="Role",
            ),
        ),
    ]