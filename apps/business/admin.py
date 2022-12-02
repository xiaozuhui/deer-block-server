from django.contrib import admin

from apps.business.models import Category, Tag, Message, TaskLog


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "label", "user")
    list_filter = ('user',)
    list_per_page = 40


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "label", 'level')
    list_per_page = 40


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "source_type", "from_user", "to_user", "has_consumed")
    list_per_page = 20
    list_filter = ('from_user', "to_user", "has_consumed", "source_type")


@admin.register(TaskLog)
class TaskLogAdmin(admin.ModelAdmin):
    list_display = ("uuid", "celery_task_id",
                    "from_model", "celery_function",
                    "retry_count", "final_status", "is_success", "login")
    list_per_page = 50
    list_filter = ('celery_task_id', "from_model", "celery_function", "login")
