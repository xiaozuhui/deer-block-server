# Generated by Django 3.2.7 on 2022-08-15 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artwork', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='art',
            options={'verbose_name': '艺术品', 'verbose_name_plural': '艺术品'},
        ),
        migrations.AlterModelTable(
            name='art',
            table='art',
        ),
    ]