import django_filters

from apps.business.models import Tag


class TagFilter(django_filters.FilterSet):
    class Meta:
        model = Tag
        fields = {
            "id": ['exact'],
            "label": ['exact', 'icontains'],
            "user": ['exact'],
        }
