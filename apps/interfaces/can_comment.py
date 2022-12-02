from apps.business.models import Comment
from apps.interfaces.can_base import CanCommentBase
from exceptions.custom_excptions.business_error import BusinessError


class CanComment(CanCommentBase):
    """
    可评论接口
    """

    def create_comment(self, user, content, medias=None, ip=None, *args, **kwargs):
        """
        创建评论

        content: string 评论内容 不可为空
        medias: list of File id 保存的文件id
        parent_comments: 父评论id
        ip: ip地址
        """
        if not user:
            # 没有对应的用户，就不能创建
            raise BusinessError.ErrNoUser
        if not content and not medias:
            # 如果既没有内容又没有图片，则报错
            raise BusinessError.ErrContentEmpty
        if not medias:
            comment = Comment.create_instance(self, user=user, content=content, ip=ip)
        else:
            comment = Comment.create_instance(self, user=user, content=content, medias=medias, ip=ip)
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
        获取某个comment对象下的comment
        """
        c = Comment.get_instances(self)
        return c

    def get_user_comments(self, user):
        c = Comment.get_instances(self).filter(user__id=user.id)
        return c
