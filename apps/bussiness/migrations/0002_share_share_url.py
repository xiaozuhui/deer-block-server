# Generated by Django 3.2.7 on 2022-05-29 14:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('bussiness', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='share',
            name='share_url',
            field=models.URLField(default='', verbose_name='分享链接'),
        ),
    ]
