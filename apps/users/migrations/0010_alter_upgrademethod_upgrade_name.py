# Generated by Django 3.2.7 on 2022-09-04 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_levelgroup_levels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upgrademethod',
            name='upgrade_name',
            field=models.CharField(choices=[('发布动态', '发布动态'), ('评论', '评论'), ('点赞', '点赞'), ('发表作品', '发表作品'), ('被评论', '被评论'), ('被点赞', '被点赞')], max_length=10, verbose_name='升级方式'),
        ),
    ]
