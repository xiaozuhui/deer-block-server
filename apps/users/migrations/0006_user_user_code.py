# Generated by Django 3.2.7 on 2022-08-17 14:02

from django.db import migrations, models

import apps.users.models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0005_rename_signature_userprofile_autograph'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_code',
            field=models.CharField(default=apps.users.models.default_user_code, max_length=20, unique=True,
                                   verbose_name='用户编码'),
        ),
    ]
