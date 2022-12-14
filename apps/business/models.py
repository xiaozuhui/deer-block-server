from uuid import uuid4

from django.db import models
from django.db.models import JSONField

from apps.base_model import BaseModel, GenericModel
from apps.consts import SourceType
from apps.interfaces.can_base import CanCommentBase, CanThumbUpBase
from apps.media.models import File
from apps.users.models import User
from exceptions.custom_excptions.business_error import BusinessError

"""点赞和收藏，虽然使用了BaseModel，但是不应该使用逻辑删除
而且在使用的时候，也不应该释放出相关的api，而应该从issues等模型处创建或删除
"""


class Share(GenericModel):
    """用于分享的模型，该模型是不是能用于别的app
    """
    user = models.ForeignKey(User, verbose_name="分享者", on_delete=models.CASCADE, related_name="sharer")
    share_url = models.URLField(verbose_name="分享链接", default="")
    content = models.JSONField(verbose_name="分享信息", default=dict, null=True, blank=True)
    backup = models.TextField(verbose_name="备注", default="", null=True, blank=True)
    # TODO 暂定
    share_type = models.CharField(max_length=20, verbose_name="分享类型", default="")

    class Meta:
        verbose_name = "分享"
        verbose_name_plural = verbose_name
        db_table = "share"


class Collection(GenericModel):
    """
    收藏，收藏不需要使用逻辑删除
    收藏只能对应动态来收藏，而不能收藏回复
    """
    user = models.ForeignKey(User, verbose_name="收藏者", on_delete=models.CASCADE, related_name="collector")

    class Meta:
        verbose_name = "收藏"
        verbose_name_plural = verbose_name
        db_table = "collection"


class ThumbUp(GenericModel):
    """
    点赞，点赞不需要逻辑删除
    但是点赞可以对回复进行点赞
    """
    user = models.ForeignKey(User, verbose_name="点赞者", on_delete=models.CASCADE, related_name="tper")

    class Meta:
        verbose_name = "点赞"
        verbose_name_plural = verbose_name
        db_table = "thumbs_up"


"""
1、评论的保存，需要保存唯一的父级评论，也就是issues下的第一级评论
2、评论的返回，不仅仅是评论本身，我们需要：
    1、评论的用户数据
    2、评论的内容
    3、当前登陆的用户是否关注评论者的，评论者是否和当前用户互相关注
    4、当前登陆用户是否给这条评论点了赞
    5、改评论是“谁”评论了“谁”，并且指向被评论的评论
    6、所有的非一级评论，都需要被平铺为一个列表，而非一个树形结构
"""


class Comment(GenericModel, CanThumbUpBase, CanCommentBase):
    """
    评论
    1、评论内容
    2、评论者
    3、评论图片，最多三张
    P.S. 评论还可以进行评论，这个怎么写？

    评论模块也可以点赞和评论

    因为CanThumbUp和CanComment的引入导致了循环应用，所以这里使用重写让这种引用消失

    TODO 都应该提示该回复的“父回复”的“回复者”，以及回复中被@的用户
    """
    user = models.ForeignKey(User, verbose_name="评论者", on_delete=models.CASCADE, related_name="commenter")
    content = models.TextField(verbose_name="评论内容", blank=True)
    medias = models.ManyToManyField(File, verbose_name="图片和视频", blank=True)
    ip = models.GenericIPAddressField(verbose_name="评论ip地址", blank=True, null=True)
    # 第一级评论，所有的评论都应该有第一级评论
    first_class_comment = models.ForeignKey('Comment', verbose_name="第一级评论",
                                            on_delete=models.CASCADE, related_name="first_comment", null=True)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        db_table = "comment"

    def create_comment(self, user, content, medias=None, ip=None, *args, **kwargs):
        """
        创建评论

        content: string 评论内容 不可为空
        medias: list of File id 保存的文件id
        parent_comments: 父评论id
        ip: ip地址

        对于评论的评论，还需要一个父级评论
        """
        if not user:
            # 没有对应的用户，就不能创建
            raise BusinessError.ErrNoUser
        if not content and not medias:
            # 如果既没有内容又没有图片，则报错
            raise BusinessError.ErrContentEmpty
        # 这个评论id是指所有子评论的最高级评论，即issues下的第一层评论
        parent_comment_id = kwargs["parent_comment_id"]
        if not parent_comment_id:
            raise BusinessError.ErrParentCommentIDEmpty
        parent_comment = Comment.logic_objects.filter(id=parent_comment_id).first()
        if not parent_comment:
            raise BusinessError.ErrParentCommentEmpty
        # 创建
        if not medias:
            comment = Comment.create_instance(self, user=user,
                                              content=content,
                                              ip=ip,
                                              first_class_comment=parent_comment)
        else:
            comment = Comment.create_instance(self, user=user,
                                              content=content,
                                              medias=medias,
                                              ip=ip,
                                              first_class_comment=parent_comment)
        return comment

    def delete_comments(self, user):
        """
        删除所有该对象下的所有该用户的评论
        """
        c = Comment.get_instances(self).filter(user__id=user.id)
        if not c:
            raise BusinessError.ErrNoComment
        c.delete()

    def delete_comment(self, comment_id, user):
        """
        删除这个用户的某个精确到id的评论
        """
        c = Comment.get_instances(self).filter(id=comment_id).filter(user__id=user.id)
        if not c:
            raise BusinessError.ErrNoUserComment
        c.delete()

    def get_comments(self):
        """
        获取某个对象下的comment
        """
        c = Comment.get_instances(self)
        return c

    def get_all_level_comments(self):
        """
        获取某个comment下的所有级comments
        """
        comments = Comment.logic_objects.filter(first_class_comment__id=self.id)
        return comments

    def get_user_comments(self, user):
        c = Comment.get_instances(self).filter(user__id=user.id)
        return c

    def create_thumbs_up(self, user):
        """点赞，其实就是创建点赞模型的对象

        Args:
            user (_type_): 用户对象

        Raises:
            BusinessError.ErrNoUser: _description_

        Returns:
            ThumbUp: 点赞模型对象
        """
        if not user:
            # 没有对应的用户，就不能创建
            raise BusinessError.ErrNoUser
        tp = ThumbUp.create_instance(self, user=user)
        return tp

    def delete_thumbs_up(self, user):
        """取消点赞

        Args:
            user (_type_): _description_

        Raises:
            BusinessError.ErrNoThumbUp: _description_
        """
        tp = ThumbUp.get_instances(self).filter(
            user__id=user.id).first()  # 如果不存在，则为[]
        if not tp:
            raise BusinessError.ErrNoThumbUp
        tp.delete()

    def get_thumb_up(self, user):
        """获取该对象下的该用户的点赞

        Args:
            user (_type_): _description_

        Returns:
            _type_: _description_
        """
        tp = ThumbUp.get_instances(self).filter(
            user__id=user.id).first()
        return tp

    def get_thumb_ups(self):
        """获取该对象下的所有点赞

        Returns:
            _type_: _description_
        """
        tps = ThumbUp.get_instances(self)
        return tps

    def get_target_comment(self):
        """
        获取该评论所评论的评论

        只针对Comment类
        """
        content_type = self.content_type
        if content_type.model != "comment":
            # 如果不是评论，不需要
            return None
        co = self.content_object
        if not isinstance(co, Comment):
            return None
        if not co.first_class_comment:
            # 如果没有上级评论，不需要
            return None
        return co


class Tag(BaseModel):
    label = models.CharField(max_length=10, verbose_name="标签")
    user = models.ForeignKey(User, verbose_name="创建者",
                             on_delete=models.CASCADE)  # 这个只是记录一下是谁创建的这个tag
    backup = models.TextField(verbose_name="备注", default="", null=True, blank=True)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name
        db_table = "tag"


class Category(BaseModel):
    """
    关于父级分类：
    在创建分类关联的时候，如果选择了二级分类，则需要将一级分类也关联，之后以此类推
    在ser中获取的时候，将实现一颗树
    """
    label = models.CharField(max_length=100, verbose_name="分类", unique=True)
    parent_category = models.ForeignKey(
        'Category', verbose_name="父级分类",
        related_name="parent", on_delete=models.CASCADE, null=True)
    level = models.IntegerField(default=0, verbose_name="分级")  # 用于记录

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name
        db_table = "category"


class Message(BaseModel):
    """
    通知
    所有的通知将使用这个模型
    """

    # 消息源
    source_type = models.CharField(choices=SourceType.choices, verbose_name="消息源", max_length=10,
                                   default=SourceType.ISSUES)
    message_content = JSONField(verbose_name="消息内容", blank=True, null=True)
    # 消息是从哪个用户来的，默认系统用户将固定为system
    from_user = models.ForeignKey(User, related_name="from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="to_user", on_delete=models.SET_NULL, null=True)  # 消息接受者
    has_consumed = models.BooleanField(verbose_name="是否已被消费", default=False)

    class Meta:
        verbose_name = "消息"
        verbose_name_plural = verbose_name
        db_table = "message"
        managed = False


class TaskLog(BaseModel):
    """记录任务的日志
        什么日志，由什么模块发出，用于什么，时间，重试次数，是否成功
    """
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    celery_task_id = models.UUIDField(unique=True)  # celery任务的id

    from_model = models.CharField(max_length=50, verbose_name="对应模型")
    celery_function = models.CharField(max_length=255, verbose_name="方法名称")

    retry_count = models.IntegerField(default=0, verbose_name="重试次数")
    final_status = models.CharField(verbose_name="最终状态", default="", null=True, blank=True, max_length=10)
    is_success = models.BooleanField(default=False, verbose_name="是否成功")

    args = JSONField(verbose_name="传递参数", null=True, blank=True)
    result = JSONField(verbose_name="返回值", null=True, blank=True)

    login = models.ForeignKey(User, verbose_name="启动任务时的用户", null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "任务日志"
        verbose_name_plural = verbose_name
        db_table = "task_log"

    @classmethod
    def init_entity(cls, task_id, func_name, kwargs):
        entity = cls()
        entity.celery_task_id = task_id
        entity.celery_function = func_name
        entity.retry_count = 0
        entity.args = kwargs
        return entity
