# Generated by Django 3.2.7 on 2022-08-22 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import utils.gen_code


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_user_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=1, verbose_name='阶段等级')),
                ('level_name', models.CharField(max_length=255, verbose_name='等级名称')),
                ('base_upgrade_exp', models.FloatField(default=0.0, verbose_name='基础升级所需经验')),
                ('is_default', models.BooleanField(default=False, verbose_name='是否默认等级')),
            ],
            options={
                'verbose_name': '等级',
                'verbose_name_plural': '等级',
                'db_table': 'level',
            },
        ),
        migrations.CreateModel(
            name='UpgradeMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=utils.gen_code.get_level_code, max_length=8, unique=True, verbose_name='编码')),
                ('upgrade_name', models.IntegerField(choices=[(1, '发布动态'), (2, '评论'), (3, '点赞'), (4, '发表作品'), (5, '被评论'), (6, '被点赞')], verbose_name='升级方式')),
                ('base_exp_value', models.FloatField(default=0.0, help_text='对应的每次达成条件的基础经验值', verbose_name='基础经验值')),
                ('is_default', models.BooleanField(default=False, verbose_name='是否默认升级方式')),
            ],
            options={
                'verbose_name': '升级方式',
                'verbose_name_plural': '升级方式',
                'db_table': 'upgrade_method',
            },
        ),
        migrations.AddField(
            model_name='userpayment',
            name='constant_way',
            field=models.CharField(choices=[('weixin', '微信支付'), ('alipay', '支付宝'), ('union_pay', '银联支付')], default='weixin', max_length=20, verbose_name='常用支付方式'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='has_exp',
            field=models.FloatField(default=0.0, verbose_name='以获取经验'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_level',
            field=models.IntegerField(default=1, verbose_name='用户等级'),
        ),
        migrations.CreateModel(
            name='RealNameAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('created_at', models.DateTimeField(auto_now=True, null=True, verbose_name='数据创建时间')),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='数据更新时间')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='数据失效时间')),
                ('real_name', models.CharField(max_length=10, verbose_name='真实姓名')),
                ('id_number', models.CharField(max_length=20, unique=True, verbose_name='身份证号')),
                ('is_active', models.BooleanField(default=False, verbose_name='是否已经验证')),
                ('user', models.OneToOneField(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='real_user', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('logic_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='LevelGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_level', models.IntegerField(default=1, verbose_name='最低等级')),
                ('max_level', models.IntegerField(default=99, verbose_name='最高等级')),
                ('is_default', models.BooleanField(default=False, verbose_name='是否默认等级组')),
                ('levels', models.ManyToManyField(null=True, to='users.Level', verbose_name='等级')),
                ('upgrade_method', models.ManyToManyField(to='users.UpgradeMethod', verbose_name='升级方式')),
            ],
            options={
                'verbose_name': '等级组',
                'verbose_name_plural': '等级组',
                'db_table': 'level_group',
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='level_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.levelgroup', verbose_name='等级组'),
        ),
    ]
