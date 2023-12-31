# Generated by Django 4.2.4 on 2023-08-18 19:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_user_invite_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Почта')),
                ('last_activated_code', models.CharField(blank=True, max_length=6, null=True, verbose_name='Последний активированный код')),
                ('activate_code', models.BooleanField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
