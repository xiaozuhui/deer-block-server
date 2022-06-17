class CanComment:
    """
    可评论接口
    """

    def create_comment(self, user, content, medias=None, ip=None): ...

    def delete_comments(self, user): ...

    def delete_comment(self, comment_id, user): ...

    def get_comments(self): ...

    def get_user_comments(self, user): ...
