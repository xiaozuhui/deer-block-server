# Generated by Django 3.2.7 on 2022-06-04 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220531_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='ip',
            field=models.GenericIPAddressField(blank=True, null=True, verbose_name='注册时ip地址'),
        ),
    ]