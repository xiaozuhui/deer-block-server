# Generated by Django 3.2.7 on 2022-05-11 15:43

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220510_1930'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='userpayment',
            managers=[
                ('logic_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='userprofile',
            managers=[
                ('logic_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='数据创建时间'),
        ),
        migrations.AddField(
            model_name='user',
            name='delete_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='数据失效时间'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='数据更新时间'),
        ),
        migrations.AddField(
            model_name='userpayment',
            name='created_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='数据创建时间'),
        ),
        migrations.AddField(
            model_name='userpayment',
            name='delete_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='数据失效时间'),
        ),
        migrations.AddField(
            model_name='userpayment',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='userpayment',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='数据更新时间'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='created_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='数据创建时间'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='delete_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='数据失效时间'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='数据更新时间'),
        ),
    ]
