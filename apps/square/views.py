import http

from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from apps.base_view import CustomViewBase, JsonResponse
from apps.business.serializers import ShareSerializer, ThumbUpSerializer, CollectionSerializer, CommentSerializer
from apps.celerytask.comment_task import send_comment_message
from apps.celerytask.issues_task import send_issues_message
from apps.celerytask.thumbsup_task import send_thumbsub_message
from apps.consts import PublishStatus, UpgradeUserLevelMethod
from apps.square.models import Issues
from apps.square.serializers import IssuesSerializer, IssuesSimpleSerializer
from apps.users.level_manager import LevelManager
from apps.users.model2 import UserProfile
from exceptions.custom_excptions.business_error import BusinessError
from exceptions.custom_excptions.issues_error import IssuesError
from exceptions.custom_excptions.user_error import UserError


class IssuesViewSet(CustomViewBase):
    queryset = Issues.logic_objects.all().order_by('-created_at')
    serializer_class = IssuesSerializer
    filter_fields = ('id', 'title', 'status', 'publisher')
    permission_classes = [IsAuthenticated]
    permission_classes_by_action = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'default': [IsAuthenticated],
        "video_list": [AllowAny],
        "follow_issues_list": [IsAuthenticated],
    }
    level_manager = LevelManager()

    def create(self, request, *args, **kwargs):
        """
        创建草稿，并不会发布
        """
        data_ = request.data.copy()
        data_["publisher"] = request.user.id
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META.get("HTTP_X_FORWARDED_FOR")
        else:
            ip = request.data.get('ip', None)
        if ip:
            data_["ip"] = ip
        serializer = self.get_serializer(data=data_, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(data=serializer.data, msg="OK", code=0, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['get'], detail=False)
    def user_list(self, request, *args, **kwargs):
        """用户查看自己的动态列表时的接口
           其实可以使用/issues?publisher=1来控制 
        """
        user = request.user
        issues = Issues.logic_objects.filter(
            publisher__id=user.id, status=PublishStatus.PUBLISHED).order_by('-updated_at')
        page = self.paginate_queryset(issues)
        if page:
            ser = self.get_serializer(page, many=True, context={'user_id': request.user.id})
            return self.get_paginated_response(ser.data)

        ser = self.get_serializer(issues, many=True, context={'user_id': request.user.id})
        headers = self.get_success_headers(ser.data)
        return JsonResponse(status=http.HTTPStatus.OK,
                            data=ser.data, headers=headers, msg="OK", code=0)

    @action(methods=['post'], detail=False)
    @transaction.atomic
    def publishing(self, request, *args, **kwargs):
        user = request.user
        id_ = request.data.get('id', None)  # 存在这个就需要发布，否则就是创建(创建的时候就是发布)
        if id_:
            issues = Issues.logic_objects.filter(
                publisher__id=user.id, id=id_).first()  # 如果搜索不到，就报错
            if issues:
                # 更新 - 发布
                if issues.status == PublishStatus.PUBLISHED:
                    raise IssuesError.ErrHasPublished
                if issues.status == PublishStatus.ABANDONED:
                    raise IssuesError.ErrAbandonInstance
                data_ = request.data.copy()
                partial = kwargs.pop('partial', False)
                data_["status"] = PublishStatus.PUBLISHED
                if request.META.get('HTTP_X_FORWARDED_FOR'):
                    ip = request.META.get("HTTP_X_FORWARDED_FOR")
                else:
                    ip = request.data.get('ip', "")
                if ip:
                    data_["ip"] = ip
                serializer = self.get_serializer(
                    issues, data=data_, partial=partial, context={'user_id': request.user.id})
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                # self.level_manager.inc_exp(user.id, UpgradeUserLevelMethod.ISSUES)
                send_issues_message.delay(user_id=user.id, issues_id=issues.id)
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
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META.get("HTTP_X_FORWARDED_FOR")
        else:
            ip = request.data.get('ip', "")
        if ip:
            data_["ip"] = ip
        data_["status"] = PublishStatus.PUBLISHED
        serializer = self.get_serializer(data=data_, context={'user_id': request.user.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        issues_id = serializer.data.get("id")
        # self.level_manager.inc_exp(request.user.id, UpgradeUserLevelMethod.ISSUES)
        send_issues_message.delay(user_id=request.user.id, issues_id=issues_id)

        headers = self.get_success_headers(serializer.data)
        return JsonResponse(data=serializer.data, msg="OK", code=0, status=status.HTTP_201_CREATED, headers=headers)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """更新必然要形成新的副本
        """
        instance = self.get_object()
        if instance is None:
            raise IssuesError.ErrNotExist
        if instance.status == PublishStatus.ABANDONED:
            raise IssuesError.ErrAbandonInstance
        if instance.status == PublishStatus.PUBLISHED:
            raise IssuesError.ErrHasPublished
        resp = super(IssuesViewSet, self).update(request, *args, **kwargs)
        return resp

    @action(methods=['post', 'get', 'delete'], detail=True)
    @transaction.atomic
    def thumbs_up(self, request, *args, **kwargs):
        """点赞
        post:  创建点赞
        get    获取点赞的详情
        delete 取消点赞
        """
        # 1、先获取对应的点赞
        # 2、如果存在点赞，则不能创建
        # 3、如果不存在点赞，则不能删除
        issues = self.get_object()  # 获取到对应的issues
        user = request.user  # 获取登录的用户
        tp = issues.get_thumb_up(user)  # 如果不存在，则为[]
        data = []
        if request.method == 'POST':
            if not tp:
                tp = issues.create_thumbs_up(user)
                # self.level_manager.inc_exp(user.id, UpgradeUserLevelMethod.THUMBS_UP)
                # self.level_manager.inc_exp(issues.publisher.id, UpgradeUserLevelMethod.BE_THUMBS_UP)
                send_thumbsub_message.delay(user.id, issues.id)
            data = ThumbUpSerializer(tp).data
        elif request.method == 'DELETE':
            if not tp:
                raise BusinessError.ErrNoThumbUp
            issues.delete_thumbs_up(user)
        elif request.method == 'GET':
            data = ThumbUpSerializer(tp).data
        return JsonResponse(data=data, msg="OK", code=0, status=200)

    @action(methods=['post', 'get', 'delete'], detail=True)
    @transaction.atomic
    def collection(self, request, *args, **kwargs):
        """收藏
        post:  创建收藏
        get    获取收藏的详情
        delete 取消收藏
        """
        issues = self.get_object()  # 获取到对应的issues
        user = request.user  # 获取登录的用户
        coll = issues.get_collect(user)
        data = []
        if request.method == 'POST':
            if not coll:
                coll = issues.create_collect(user)
            data = CollectionSerializer(coll).data
        elif request.method == 'DELETE':
            if not coll:
                raise BusinessError.ErrNoThumbUp
            issues.delete_thumbsup(user)
        elif request.method == 'GET':
            data = CollectionSerializer(coll).data
        return JsonResponse(data=data, msg="OK", code=0, status=200)

    @action(methods=['post', 'get'], detail=True)
    def share(self, request, *args, **kwargs):
        """创建分享链接
        每一次获取分享链接，就是创建一条新的分享数据
        获取分享链接时，应该将该动态所有的分享链接全部拿出来
        """
        issues = self.get_object()  # 获取到对应的issues
        user = request.user  # 获取登录的用户
        data = []
        if request.method == 'POST':
            share_url = request.data.get('share_url', "")  # 分享的链接
            # 分享的类型，或者是分享的路径，比如微信分享、QQ分享
            share_type = request.data.get('share_type', "")
            share = issues.create_share(
                user, share_url=share_url, share_type=share_type)
            data = ShareSerializer(share).data
        elif request.method == 'GET':
            shares = issues.get_all_share()
            data = ShareSerializer(shares, many=True).data
        return JsonResponse(data=data, msg="OK", code=0, status=200)

    @action(methods=['post', 'delete'], detail=True)
    @transaction.atomic
    def comment(self, request, *args, **kwargs):
        """
        写评论或是删除评论
        删除评论需要评论的id

        获取评论，只获取第一级评论
        """
        issues = self.get_object()  # 获取到对应的issues
        user = request.user  # 获取登录的用户
        data = []
        if request.method == 'POST':
            content = request.data.get("content", "")
            medias = request.data.get("medias", None)
            if request.META.get('HTTP_X_FORWARDED_FOR'):
                ip = request.META.get("HTTP_X_FORWARDED_FOR")
            else:
                ip = request.data.get('ip', None)
            # issues的评论不需要parent_comment
            comment = issues.create_comment(user, content=content, medias=medias, ip=ip)
            # 需要给评论者和被评论者增加经验
            # self.level_manager.inc_exp(user.id, UpgradeUserLevelMethod.COMMENT)
            # self.level_manager.inc_exp(issues.publisher.id, UpgradeUserLevelMethod.BE_COMMENTED)
            send_comment_message.delay(user_id=user.id, issues_id=issues.id, comment_id=comment.id)
            data = CommentSerializer(comment, context={'user_id': request.user.id}).data
        elif request.method == 'DELETE':
            # 从query中获取comment_id
            comment_id = request.query_params.get("comment_id", None)
            if not comment_id:
                raise BusinessError.ErrNoCommentId
            issues.delete_comment(comment_id, user)
        return JsonResponse(data=data, msg="OK", code=0, status=200)

    @action(methods=['get'], detail=False)
    def video_list(self, request, *args, **kwargs):
        """获取视频动态
        TODO 应该根据热度来控制，下一个视频动态是什么
        因为目前的问题，所以不适合使用热度来控制，于是我们可以将视频动态全部获取，然后随机给用户
        在这里，因为每一次请求的视频动态应该是不同的，所以我们需要使用缓存来控制
        每一次请求的视频动态都丢进缓存，除非溢出，则重新随机，否则就不再从缓存中获取
        Args:
            request (_type_): _description_
        """
        pass

    @action(methods=['get'], detail=False)
    def follow_list(self, request, *args, **kwargs):
        """User follow someones, and can get there issues

        Args:
            request (_type_): _description_
        """
        user = request.user  # 获取登录的用户
        user_profile = UserProfile.logic_objects.filter(user__id=user.id).first()
        if not user_profile:
            raise UserError.ErrProfileNoExist
        follows = user_profile.follow.all()  # 我关注的人
        follow_ids = [f.id for f in follows]
        # 获取到所有的issues
        issues = Issues.objects.filter(publisher__id__in=follow_ids, status=PublishStatus.PUBLISHED).order_by(
            '-created_at')
        page = self.paginate_queryset(issues)
        if page:
            ser = IssuesSimpleSerializer(page, many=True)
            return self.get_paginated_response(ser.data)
        ser = IssuesSimpleSerializer(issues, many=True)
        headers = self.get_success_headers(ser.data)
        return JsonResponse(status=http.HTTPStatus.OK,
                            data=ser.data, headers=headers, msg="OK", code=0)
