from rest_framework.decorators import action
from rest_framework import status
from apps.square.models import Collection, Issues, Reply, ThumbsUp
from apps.square.serializers import CollectionSerializer, IssuesSerializer, ReplySerializer, ThumbsUpSerializer
from apps.base_view import CustomViewBase, JsonResponse
import http


class SquareBaseViewSet(CustomViewBase):
    def create(self, request, *args, **kwargs):
        data_ = request.data.copy()
        data_["publisher"] = request.user.id
        serializer = self.get_serializer(data=data_)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(data=serializer.data, msg="OK", code=0, status=status.HTTP_201_CREATED, headers=headers)


class IssuesViewSet(SquareBaseViewSet):
    queryset = Issues.logic_objects.all().order_by('-created_at')
    serializer_class = IssuesSerializer
    filter_fields = ('id', 'title', 'status', 'publisher')

    @action(methods=['get'], detail=False)
    def user_list(self, request, *args, **kwargs):
        """用户查看自己的动态列表时的接口
           其实可以使用/issues?publisher=1来控制 
        """
        user = request.user
        isues = Issues.logic_objects.filter(publisher__id=user.id)
        ser = self.get_serializer(isues, many=True)
        headers = self.get_success_headers(ser.data)
        return JsonResponse(status=http.HTTPStatus.OK,
                            data=ser.data, headers=headers, msg="OK", code=0)


class CollectionViewSet(SquareBaseViewSet):
    queryset = Collection.objects.all().order_by('-id')
    serializer_class = CollectionSerializer


class ThumbsUpViewSet(SquareBaseViewSet):
    queryset = ThumbsUp.objects.all().order_by('-id')
    serializer_class = ThumbsUpSerializer


class ReplyViewSet(SquareBaseViewSet):
    queryset = Reply.logic_objects.all().order_by('-created_at')
    serializer_class = ReplySerializer
