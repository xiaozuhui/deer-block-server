# Generated by Django 3.2.7 on 2022-06-10 09:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('media', '0005_filestorage_file_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='file',
            options={'ordering': ['upload_time'], 'verbose_name': '基础文件管理', 'verbose_name_plural': '基础文件管理'},
        ),
    ]