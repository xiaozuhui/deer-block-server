# Generated by Django 3.2.7 on 2022-06-28 09:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0003_userprofile_ip'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='followed',
        ),
    ]
