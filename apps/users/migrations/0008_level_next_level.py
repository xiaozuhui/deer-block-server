# Generated by Django 3.2.7 on 2022-09-04 01:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0007_auto_20220822_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='level',
            name='next_level',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='the_next_level', to='users.level'),
        ),
    ]
