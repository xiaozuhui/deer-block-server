import http
import logging
from django.core.cache import cache
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from utils.message_tools import send_message
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from utils.user_tools import get_register_key, get_register_token, get_user_name, validate_code

from .models import User
from .model2 import UserProfile
from .serializers import RegisterSerializer, UserSerializer, ProfileSerializer, BlackTokenSerializer
from apps.users import serializers

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    """
    User TODO 需要对每个操作都进行验权
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().order_by('id')
    serializer_class = ProfileSerializer


class LogoutView(GenericAPIView):
    """
    注销用黑名单做
    加入黑名单不能再刷新生成新的token, 但是当前token依然有效
    前端逻辑：注销时去掉请求头，请求接口没有权限会自动刷新token->因为加入了黑名单所以无法刷新，此时处于注销状态
    重新登录可以正常使用
    TODO： 需要 flushexpiredtokens命令定期清理？ https://django-rest-framework-simplejwt.readthedocs.io/en/latest/blacklist_app.html
    另一种做法时用redis记录用户的状态, 注销时状态为logout 无法访问，重新登录时状态为login
    """
    serializer_class = BlackTokenSerializer

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterView(GenericAPIView):

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def _register(self, phone_number, vcode, username=""):
        """
        1、如果cache中没有token，则发出短信验证码，并且五分钟后失效
        2、如果cache中有该对应的token，则验证token是否正确，如果正确，则直接创建用户
        """
        if not phone_number:
            raise ValueError("phone number is required")

        register_key = get_register_key(phone_number)
        if cache.get(register_key, None):
            # 2、如果存在值，则验证token
            if not vcode:
                raise ValueError("验证码 is required")
            if not validate_code(phone_number, vcode):
                raise ValueError("验证码过期，请重新请求")
            return {
                "phone_number": phone_number,
                "username": username if username else get_user_name(phone_number),
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
            }
        else:
            # 1、如果没有，则写入token
            _, register_code = get_register_token()  # 存入cache的token，以及发送给用户的code
            cache.set(register_key, register_code, timeout=5*60)  # 只保存五分钟
            res = send_message(phone_number, register_code,
                               'LTAI5tKqWQhoEfRhyJKc15yW', 'FGhlSPqkSE7qmZksPUYya762j2AdaR')
            if res["Code"] != "OK":
                logger.error("错误的结果：{}".format(res["Message"]))
                raise ValueError("发送信息失败")
            return None

    def post(self, request):
        phone_number = request.data.get("phone_number", None)
        validate_code = request.data.get("validate_code", None)
        password = request.data.get("password", "123456")
        username = request.data.get("username", "")
        data = self._register(phone_number, validate_code, username)
        if data:
            # 如果有用户，那么就应该创建User
            user = User()
            user.username = data["username"]
            user.set_password(password)
            user.phone_number = data["phone_number"]
            user.save()
            refresh = RefreshToken.for_user(user)
            res_data = {
                "username": user.username,
                "phone_number": user.phone_number,
                "user_id": user.id,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
            return Response(status=http.HTTPStatus.OK, data=res_data)
        return Response(status=http.HTTPStatus.OK, data={"send_status": "OK"})
