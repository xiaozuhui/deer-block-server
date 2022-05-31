from apps.base_view import CustomViewBase, JsonResponse
from apps.bussiness.filter import TagFilter
from apps.bussiness.models import Tag
from apps.bussiness.serializers import TagSerializer
from rest_framework import status


class TagViewSet(CustomViewBase):
    queryset = Tag.logic_objects.all()
    serializer_class = TagSerializer
    filter_class = TagFilter

    def create(self, request, *args, **kwargs):
        data_ = request.data.copy()
        data_["user"] = request.user.id
        serializer = self.get_serializer(data=data_)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(data=serializer.data, msg="OK", code=0, status=status.HTTP_201_CREATED, headers=headers)
