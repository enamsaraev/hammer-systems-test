# Generated by Django 4.2.4 on 2023-08-18 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_userprofile_active_user_activeuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='last_activated_code',
        ),
    ]
