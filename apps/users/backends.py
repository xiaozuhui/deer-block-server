from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.cache import cache
from django.db.models import Q

UserModel = get_user_model()


class CustomBackend(ModelBackend):
    """
    用户名、手机号 + 密码
    """

    def user_can_authenticate(self, user):
        is_active = getattr(user, 'is_active', None)
        is_delete = getattr(user, 'is_delete', False)
        return (is_active and not is_delete) or (is_active is None)

    def authenticate(self, request, username=None, password=None, **kwargs):
        """使用用户名或是手机号+密码的方式验证

        Args:
            request (_type_): _description_
            username (_type_, optional): 可能是手机号也可能是用户名. Defaults to None.
            password (_type_, optional): 密码. Defaults to None.

        Returns:
            _type_: _description_
        """
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = UserModel.logic_objects.get(
                Q(username=username) | Q(phone_number=username))
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


class MobileTokenModelBackend(ModelBackend):

    def user_can_authenticate(self, user):
        is_active = getattr(user, 'is_active', None)
        is_delete = getattr(user, 'is_delete', False)
        return (is_active and not is_delete) or (is_active is None)

    def authenticate(self, request, username=None, password=None, **kwargs):
        """手机号+验证码的方式验证
        如果手机号码不正确，那么就直接报错

        Args:
            request (_type_): _description_
            username (_type_, optional): 手机号码. Defaults to None.
            password (_type_, optional): 验证码. Defaults to None.

        Returns:
            _type_: _description_
        """
        if username is None:
            if UserModel.USERNAME_FIELD not in kwargs:
                return None
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel.logic_objects.get(phone_number=username)  # 手机号存在
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
        else:
            register_key = "smg_{}".format(username)
            token = cache.get(register_key, None)
            if token:
                # 2、如果存在值，则验证token
                if not password:
                    return None
                if token != password:
                    return None
                if self.user_can_authenticate(user):
                    return user
            return None
