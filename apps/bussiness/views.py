from apps.base_view import CustomViewBase
from apps.bussiness.filter import TagFilter
from apps.bussiness.models import Tag
from apps.bussiness.serializers import TagSerializer


class TagViewSet(CustomViewBase):
    queryset = Tag.logic_objects.all()
    serializer_class = TagSerializer
    filter_class = TagFilter
