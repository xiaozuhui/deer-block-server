# Generated by Django 3.2.7 on 2022-06-10 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('square', '0006_reply_ip'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issues',
            old_name='is_vedio_issues',
            new_name='is_video_issues',
        ),
    ]
