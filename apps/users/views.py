import http
import logging
import random

from django.core.cache import cache
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from exceptions.cache_err import CacheRequestError as crerr
from exceptions.custom_errors import SUCCESS
from exceptions.send_message import SendMessageError as smerr
from utils import consts
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from utils.send_message import dispatch

from utils.user_tools import get_user_name, get_user_password

from .models import User
from .model2 import UserProfile
from .serializers import MobileSendMessageSerializer, RegisterSerializer, UserSerializer, ProfileSerializer, BlackTokenSerializer

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

    def _register(self, phone_number, vcode, username="") -> dict:
        if not phone_number:
            raise smerr.PhoneNumberEmpty
        register_key = "smg_{}".format(phone_number)
        token = cache.get(register_key, None)
        if token:
            # 2、如果存在值，则验证token
            if not vcode:
                raise smerr.ValidCodeEmpty
            if token != vcode:
                raise smerr.ValidCodeWrong
            return {
                "phone_number": phone_number,
                "username": username if username else get_user_name(phone_number),
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
            }
        # 如果token为空，则可以直接判断为失效
        raise smerr.ValidCodeExpire

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.data["phone_number"]
        vcode = serializer.data["validate_code"]
        username = serializer.data.get("username", "")
        data = self._register(phone_number, vcode, username)
        user = User()
        user.username = data["username"]
        user.set_password(get_user_password())
        user.phone_number = data["phone_number"]
        user.save()

        # 注册用户后默认生成profile数据
        profile = UserProfile.objects.get(user__id=user.id)
        # 注册用户后，默认登录
        refresh = RefreshToken.for_user(user)
        res_data = {
            "username": user.username,
            "phone_number": user.phone_number,
            "user_id": user.id,
            "user_profile_id": profile.id,  # 用户对应的profile的id，已经初始化创建
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
        return Response(status=http.HTTPStatus.OK, data=res_data)


class SendMessageView(GenericAPIView):
    """发送短信的API

    post: 
        请求短信的发送

        参数:
            - phone_number: 手机号码
    """
    serializer_class = MobileSendMessageSerializer
    permission_classes = [AllowAny]

    def _send_message(self, phone_number: str, vcode: str):
        client = dispatch()
        res = client.send_message(phone_number, vcode)
        if res["Code"] != "OK":
            # logger.error("错误的结果：{}".format(res["Message"]))
            err = smerr.SendFailure
            err.set_message = res["Message"]
            err.set_params = res
            raise err
        return

    def post(self, request, *args, **kwargs):
        """请求短信的发送

        1、如果cache中没有对应的手机号，那么就生成验证码，然后发送信息
        2、如果有验证码，那么就返回不能重复请求

        这里的请求有一个问题，那就是失效时间
        预计会在cache中保留两份数据
        一份是请求的cache，限时60秒，60秒内无法重新请求
        一份是发送验证码的cache，限时5分钟，如果60秒后重新请求，则删除该记录后，再重新生成记录
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.data["phone_number"]
        if not phone_number:
            raise smerr.PhoneNumberEmpty

        # 从cache中查询
        token = cache.get("req_{}".format(phone_number), default=None)
        if token is not None:
            # req_num的value本身就是""空字符串，所以not none就是存在
            # 如果token存在，说明已经请求过并且还没有失效，因此直接返回即可
            warn = crerr.ExistToken
            warn.set_message = "手机验证码请求已经存在，并且还未经过60秒失效"
            return Response(status=http.HTTPStatus.OK, data=warn.to_serializer())

        # token 为None意味着，可以重新请求验证码
        cache.set("req_{}".format(phone_number), "", timeout=60)  # 设置60秒的失效时间
        vcode = "".join(random.choices(consts.NUM, k=6))  # 形似 654789

        # 搜索smg_phonenumber对应的token，如果存在，则删除重新写入，如果不存在，直接写入
        if cache.get("smg_{}".format(phone_number), default=None):
            cache.delete("smg_{}".format(phone_number))

        # 发送信息，如果没有报错，说明信息正确发出
        self._send_message(phone_number, vcode)
        cache.set("smg_{}".format(phone_number), vcode, timeout=5*60)  # 5分钟的失效
        return Response(status=http.HTTPStatus.OK, data={"code": 0, "message": "OK"})
