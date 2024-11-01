# Generated by Django 5.1.2 on 2024-11-01 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="users",
            managers=[],
        ),
        migrations.RemoveField(
            model_name="users",
            name="active",
        ),
        migrations.RemoveField(
            model_name="users",
            name="admin",
        ),
        migrations.RemoveField(
            model_name="users",
            name="staff",
        ),
        migrations.AddField(
            model_name="users",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="users",
            name="is_admin",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="users",
            name="is_staff",
            field=models.BooleanField(default=False),
        ),
    ]