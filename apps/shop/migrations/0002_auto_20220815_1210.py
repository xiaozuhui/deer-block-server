# Generated by Django 3.2.7 on 2022-08-15 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artwork', '0003_auto_20220815_1210'),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='count',
            field=models.IntegerField(default=1, verbose_name='数量'),
        ),
        migrations.AddField(
            model_name='product',
            name='is_grounding',
            field=models.BooleanField(default=False, verbose_name='是否上架'),
        ),
        migrations.AlterField(
            model_name='product',
            name='art',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='artwork.art', verbose_name='艺术品'),
        ),
    ]
