# Generated by Django 3.2.7 on 2022-08-15 10:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('business', '0007_auto_20220815_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent',
                                    to='business.category', verbose_name='父级分类'),
        ),
    ]
