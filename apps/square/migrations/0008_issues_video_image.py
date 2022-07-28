# Generated by Django 3.2.7 on 2022-06-12 04:40

import django.db.models.deletion
from django.db import migrations

import apps.custom_models


class Migration(migrations.Migration):
    dependencies = [
        ('media', '0006_alter_file_options'),
        ('square', '0007_rename_is_vedio_issues_issues_is_video_issues'),
    ]

    operations = [
        migrations.AddField(
            model_name='issues',
            name='video_image',
            field=apps.custom_models.ImageField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                                related_name='video_image', to='media.file'),
        ),
    ]
