# Generated by Django 3.2.7 on 2022-08-06 18:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0004_remove_userprofile_followed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='signature',
            new_name='autograph',
        ),
    ]
