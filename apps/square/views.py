from rest_framework.decorators import action
from rest_framework import status
from apps.consts import PublishStatus
from apps.square.models import Collection, Issues, Reply, Share, ThumbsUp
from apps.square.serializers import CollectionSerializer, IssuesSerializer, ReplySerializer, ShareSerializer, ThumbsUpSerializer
from apps.base_view import CustomViewBase, JsonResponse
import http

from exceptions.custom_excptions.issues_error import IssuesError


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
        isuess = Issues.logic_objects.filter(publisher__id=user.id).order_by('-updated_at')
        page = self.paginate_queryset(isuess)
        if page:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)

        ser = self.get_serializer(isuess, many=True)
        headers = self.get_success_headers(ser.data)
        return JsonResponse(status=http.HTTPStatus.OK,
                            data=ser.data, headers=headers, msg="OK", code=0)

    @action(methods=['post'], detail=False)
    def publishing(self, request, *args, **kwargs):
        user = request.user
        id = request.data.get('id', None)  # 存在这个就需要发布，否则就是创建(创建的时候就是发布)
        if id:
            issues = Issues.logic_objects.filter(
                publisher__id=user.id, id=id).first()  # 如果搜索不到，就报错
            if issues:
                # 更新 - 发布
                if issues.status == PublishStatus.PUBLISHED:
                    raise IssuesError.ErrHasPublished
                data_ = request.data.copy()
                partial = kwargs.pop('partial', False)
                data_["status"] = PublishStatus.PUBLISHED
                serializer = self.get_serializer(
                    issues, data=data_, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return JsonResponse(data=serializer.data, msg="OK", code=0, status=http.HTTPStatus.OK)
            else:
                # 没有动态数据
                raise IssuesError.ErrNotExist
        else:
            # 创建 - 发布
            return self._create_publish(request, *args, **kwargs)

    def _create_publish(self, request, *args, **kwargs):
        """并不重写create方法，直接创建发布
        """
        data_ = request.data.copy()
        data_["publisher"] = request.user.id
        data_["status"] = PublishStatus.PUBLISHED
        serializer = self.get_serializer(data=data_)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(data=serializer.data, msg="OK", code=0, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """更新必然要形成新的副本
        """
        instance = self.get_object()
        if instance is None:
            raise IssuesError.ErrNotExist
        if instance.status == PublishStatus.ABANDONED:
            raise IssuesError.ErrAbandonInstance
        # 首先需要将原本的issues变为废弃状态，然后再创建新的副本
        instance.status = PublishStatus.ABANDONED
        instance.save()  # 推荐使用save，这样可以记录保存时间
        data_ = request.data.copy()
        data_["publisher"] = request.user.id
        # 如果原本的数据有origin，则使用origin，否则就使用issues的id
        data_["origin"] = instance.origin.id if instance.origin else instance.id
        data_["version"] = instance.version + 1
        serializer = self.get_serializer(data=data_)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse(data=serializer.data, msg="OK", code=0, status=http.HTTPStatus.OK)


class CollectionViewSet(SquareBaseViewSet):
    queryset = Collection.objects.all().order_by('-id')
    serializer_class = CollectionSerializer


class ThumbsUpViewSet(SquareBaseViewSet):
    queryset = ThumbsUp.objects.all().order_by('-id')
    serializer_class = ThumbsUpSerializer


class ShareViewSet(SquareBaseViewSet):
    queryset = Share.objects.all().order_by('-id')
    serializer_class = ShareSerializer


class ReplyViewSet(SquareBaseViewSet):
    queryset = Reply.logic_objects.all().order_by('-created_at')
    serializer_class = ReplySerializer
