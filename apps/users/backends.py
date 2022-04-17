from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.cache import cache
from django.db.models import Q

UserModel = get_user_model()


class CustomBackend(ModelBackend):
    """
    用户名、手机号、邮箱登录
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = UserModel.objects.get(Q(username=username) | Q(profile__phone=username) | Q(email=username))
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


class MobileTokenModelBackend(ModelBackend):
    """
    手机号+验证码
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            if UserModel.USERNAME_FIELD not in kwargs:
                return None
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel.objects.get(profile__phone=username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
        else:
            token_key = 'deer_block_phone_token' + username
            if cache.get(token_key) == password and self.user_can_authenticate(user):
                return user
