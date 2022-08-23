import http

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from apps.base_view import CustomViewBase, JsonResponse
from apps.business.filter import TagFilter
from apps.business.models import Tag, Comment, Message
from apps.business.serializers import TagSerializer, CommentSerializer, ThumbUpSerializer, MessageSerializer
from apps.celerytask.comment_task import send_comment_message
from apps.celerytask.thumbsup_task import send_thumbsub_message
from apps.consts import UpgradeUserLevelMethod
from apps.custom_permission import NoPermission
from apps.users.level_manager import LevelManager
from exceptions.custom_excptions.business_error import BusinessError
from exceptions.custom_excptions.params_error import ParamsError


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


class CommentViewSet(CustomViewBase):
    """
    评论应该可以被单独搜索，而不应该全部拿出
    评论多的需要分页
    """
    queryset = Comment.logic_objects.all()
    serializer_class = CommentSerializer
    level_manager = LevelManager()

    # list和retrieve操作是可以任何人都请求的，但是其他操作，只能本人从评论处操作，包括创建、和删除
    permission_classes_by_action = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'destroy': [IsAuthenticated],
        'default': [NoPermission],
        'by_content_type': [AllowAny],
        'comment': [IsAuthenticated],
        'thumbs_up': [IsAuthenticated],
    }

    @action(methods=['get'], detail=False)
    def by_content_type(self, request, *args, **kwargs):
        """
        通过模型名称和id获取对应的评论

        类似：
        content_type = issues
        content_id = 2
        """
        content_type = request.query_params.get("content_type", None)
        if not content_type:
            err = ParamsError.ErrPostParams
            err.params = {"content_type": content_type}
            err.message = "参数{}为空".format("content_type")
            raise err
        content_id = request.query_params.get("content_id", None)
        if not content_id:
            err = ParamsError.ErrPostParams
            err.params = {"content_id": content_id}
            err.message = "参数{}为空".format("content_id")
            raise err
        # 获取到对应的模型下的所有的评论
        comments = Comment.logic_objects.filter(content_type__model=content_type, object_id=content_id)
        # 分页
        page = self.paginate_queryset(comments)
        if page:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)
        ser = self.get_serializer(comments, many=True)
        headers = self.get_success_headers(ser.data)
        return JsonResponse(status=http.HTTPStatus.OK,
                            data=ser.data, headers=headers, msg="OK", code=0)

    @action(methods=['get', 'post', 'delete'], detail=True)
    def comment(self, request, *args, **kwargs):
        """
        对于“评论”模型

        创建、删除、获取“子评论”

        post data 参数需要issues_id
        """
        comment = self.get_object()  # 获取到对应的comment
        user = request.user  # 获取登录的用
        data = []
        if request.method == 'POST':
            issues_id = request.data.get("issues_id")
            if not issues_id:
                raise BusinessError.ErrParamsNotIssuesId
            content = request.data.get("content", "")
            medias = request.data.get("medias", None)
            if request.META.get('HTTP_X_FORWARDED_FOR'):
                ip = request.META.get("HTTP_X_FORWARDED_FOR")
            else:
                ip = request.data.get('ip', None)
            parent_comment_id = request.data.get("parent_comment_id", None)
            if not parent_comment_id:
                raise BusinessError.ErrParentCommentIDEmpty
            comment_ = comment.create_comment(user, content=content, medias=medias, ip=ip,
                                              parent_comment_id=parent_comment_id)
            self.level_manager.inc_exp(user.id, UpgradeUserLevelMethod.COMMENT)
            self.level_manager.inc_exp(comment.user.id, UpgradeUserLevelMethod.BE_COMMENTED)
            send_comment_message.delay(user_id=user.id, issues_id=issues_id, comment_id=comment_.id,
                                       target_comment_id=comment.id)
            data = CommentSerializer(comment_, context={'user_id': request.user.id}).data
        elif request.method == 'DELETE':
            comment_id = request.data.get("comment_id", None)
            if not comment_id:
                raise BusinessError.ErrNoCommentId
            comment.delete_comment(comment_id, user)
        else:
            # 这里的获取是指comment下的所有子评论
            # 要不要分页？
            sub_comments = comment.get_all_level_comments()
            page = self.paginate_queryset(sub_comments)
            if page:
                ser = self.get_serializer(page, many=True)
                return self.get_paginated_response(ser.data)
            ser = self.get_serializer(sub_comments, many=True)
            data = ser.data
        return JsonResponse(status=http.HTTPStatus.OK, data=data, msg="OK", code=0)

    @action(methods=['post', 'delete'], detail=True)
    def thumbs_up(self, request, *args, **kwargs):
        """对评论点赞
        post data 参数需要issues_id
        """
        comment = self.get_object()  # 获取到对应的issues
        user = request.user  # 获取登录的用户
        issues_id = request.data.get("issues_id")
        if not issues_id:
            raise BusinessError.ErrParamsNotIssuesId
        tp = comment.get_thumb_up(user)  # 如果不存在，则为[]
        data = []
        if request.method == 'POST':
            if not tp:
                tp = comment.create_thumbs_up(user)
                self.level_manager.inc_exp(user.id, UpgradeUserLevelMethod.THUMBS_UP)
                self.level_manager.inc_exp(comment.user.id, UpgradeUserLevelMethod.BE_THUMBS_UP)
                send_thumbsub_message(user.id, issues_id, comment.id)
            data = ThumbUpSerializer(tp).data
        elif request.method == 'DELETE':
            if not tp:
                raise BusinessError.ErrNoThumbUp
            comment.delete_thumbs_up(user)
        return JsonResponse(data=data, msg="OK", code=0, status=200)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.logic_objects.all()
    serializer_class = MessageSerializer

    @action(methods=['get'], detail=False)
    def get_user_messages(self, request, *args, **kwargs):
        """
        获取用户的所有消息

        需要分组排序
        1、按照已读未读分组，未读在前
        2、按照接收发送时间排序，新的在前
        """
        if not request.method == 'GET':
            raise BusinessError.ErrErrorMethod
        user_id = request.query_params['user_id']
        msgs = Message.logic_objects.filter(to_user_id=user_id).order_by('has_consumed', '-created_at', )
        page = self.paginate_queryset(msgs)
        if page:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)
        ser = self.get_serializer(msgs, many=True)
        data = ser.data
        return JsonResponse(status=http.HTTPStatus.OK, data=data, msg="OK", code=0)
