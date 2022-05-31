# Generated by Django 3.2.7 on 2022-05-31 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bussiness', '0003_share_share_type'),
        ('media', '0003_auto_20220521_1115'),
        ('square', '0002_auto_20220529_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issues',
            name='categories',
            field=models.ManyToManyField(blank=True, to='bussiness.Category', verbose_name='分类'),
        ),
        migrations.AlterField(
            model_name='issues',
            name='medias',
            field=models.ManyToManyField(blank=True, to='media.File', verbose_name='图片和视频'),
        ),
        migrations.AlterField(
            model_name='issues',
            name='tags',
            field=models.ManyToManyField(blank=True, to='bussiness.Tag', verbose_name='标签'),
        ),
    ]
