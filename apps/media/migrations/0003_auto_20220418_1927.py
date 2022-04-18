# Generated by Django 3.2.7 on 2022-04-18 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('media', '0002_file_remarks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='uploader_id',
        ),
        migrations.RemoveField(
            model_name='file',
            name='uploader_name',
        ),
        migrations.AddField(
            model_name='file',
            name='uploader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uploader', to=settings.AUTH_USER_MODEL, verbose_name='上传者'),
        ),
    ]
