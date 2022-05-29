# Generated by Django 3.2.7 on 2022-05-29 06:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ThumbUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('created_at', models.DateTimeField(auto_now=True, null=True, verbose_name='数据创建时间')),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='数据更新时间')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='数据失效时间')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('tper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='点赞者')),
            ],
            options={
                'verbose_name': '点赞',
                'verbose_name_plural': '点赞',
                'db_table': 'thumbs_up',
            },
            managers=[
                ('logic_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('created_at', models.DateTimeField(auto_now=True, null=True, verbose_name='数据创建时间')),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='数据更新时间')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='数据失效时间')),
                ('label', models.CharField(max_length=10, verbose_name='标签')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
                'db_table': 'tag',
            },
            managers=[
                ('logic_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('created_at', models.DateTimeField(auto_now=True, null=True, verbose_name='数据创建时间')),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='数据更新时间')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='数据失效时间')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('sharer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='分享者')),
            ],
            options={
                'verbose_name': '分享',
                'verbose_name_plural': '分享',
                'db_table': 'share',
            },
            managers=[
                ('logic_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('created_at', models.DateTimeField(auto_now=True, null=True, verbose_name='数据创建时间')),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='数据更新时间')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='数据失效时间')),
                ('object_id', models.PositiveIntegerField()),
                ('collecter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='收藏者')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': '收藏',
                'verbose_name_plural': '收藏',
                'db_table': 'collection',
            },
            managers=[
                ('logic_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('created_at', models.DateTimeField(auto_now=True, null=True, verbose_name='数据创建时间')),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='数据更新时间')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='数据失效时间')),
                ('label', models.CharField(max_length=100, verbose_name='分类')),
                ('level', models.IntegerField(default=0, verbose_name='分级')),
                ('parent_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='bussiness.category', verbose_name='父级分类')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
                'db_table': 'category',
            },
            managers=[
                ('logic_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
