# Generated by Django 3.2.7 on 2022-05-15 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('square', '0004_rename_dy_info_thumbsup_issues'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collection',
            old_name='who',
            new_name='publisher',
        ),
        migrations.RenameField(
            model_name='reply',
            old_name='replier',
            new_name='publisher',
        ),
        migrations.RenameField(
            model_name='thumbsup',
            old_name='who',
            new_name='publisher',
        ),
        migrations.AlterField(
            model_name='issues',
            name='status',
            field=models.CharField(choices=[('draft', '草稿'), ('published', '发布'), ('abandoned', '废弃')], default='draft', max_length=20, verbose_name='状态'),
        ),
    ]