# Generated by Django 5.0.1 on 2024-02-02 01:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Users", "0007_alter_profile_user_department_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="department",
            name="dept_abbr",
            field=models.CharField(
                max_length=10, unique=True, verbose_name="Department Abbreviation"
            ),
        ),
        migrations.AlterField(
            model_name="department",
            name="dept_name",
            field=models.CharField(max_length=30, verbose_name="Department Name"),
        ),
        migrations.AlterField(
            model_name="identity",
            name="identity_name",
            field=models.CharField(
                max_length=30, unique=True, verbose_name="Identity Name"
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="user_department",
            field=models.ForeignKey(
                default="OTHERS",
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="Users.department",
                verbose_name="Department",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="user_identity",
            field=models.ForeignKey(
                default="Student",
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="Users.identity",
                verbose_name="Role",
            ),
        ),
    ]
