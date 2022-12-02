# Generated by Django 3.2.7 on 2022-05-21 03:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('media', '0002_file_uploader'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='filestorage',
            options={'verbose_name': '文件', 'verbose_name_plural': '文件'},
        ),
        migrations.AlterField(
            model_name='filestorage',
            name='filename',
            field=models.CharField(default='', max_length=225, verbose_name='文件名'),
        ),
    ]
