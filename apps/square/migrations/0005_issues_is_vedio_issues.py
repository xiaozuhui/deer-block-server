# Generated by Django 3.2.7 on 2022-06-06 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('square', '0004_issues_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='issues',
            name='is_vedio_issues',
            field=models.BooleanField(default=False, verbose_name='是否是视频动态'),
        ),
    ]