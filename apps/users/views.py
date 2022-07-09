import http
import logging
import random

from django.core.cache import cache
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.base_view import CustomViewBase, JsonResponse
from exceptions.custom_excptions.cache_err import CacheRequestError as crerr
from exceptions.custom_excptions.send_message import SendMessageError as smerr
from exceptions.custom_excptions.user_error import UserError
from utils import consts
from utils.send_message import dispatch
from utils.user_tools import get_user_name, get_user_password
from .model2 import UserProfile
from .models import User
from .serializers import MobileSendMessageSerializer, RegisterSerializer, UserSerializer, ProfileSerializer, \
    BlackTokenSerializer

logger = logging.getLogger('django')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.logic_objects.all()
    serializer_class = UserSerializer

    @action(methods=['post', 'delete'], detail=True)
    def follow(self, request, *args, **kwargs):
        """
        关注功能

        post 当前用户关注对应的用户，需要被关注用户的id
        delete 取消关注
        """
        current_user = request.user  # 当前登录用户
        current_profile = UserProfile.logic_objects.filter(user__id=current_user.id).first()
        target_user = self.get_object()  # 目标用户
        current_follows = current_profile.follow.all()  # 当前登录用户的关注列表
        if request.method == "POST":
            if target_user in current_follows:
                # 已经关注
                raise UserError.ErrHasFollow
            current_profile.follow.add(target_user)
            current_profile.save()
        elif request.method == "DELETE":
            if target_user not in current_follows:
                # 没有关注
                raise UserError.ErrNotFollow
            current_profile.follow.remove(target_user)
        return JsonResponse(data=[], msg="OK", code=0, status=200)

    @action(methods=['get'], detail=False)
    def follows(self, request, *args, **kwargs):
        """
        获取当前用户的所有关注的用户
        """
        user = request.user
        profile = UserProfile.logic_objects.filter(user__id=user.id).first()
        follows = profile.follow.all()
        page = self.paginate_queryset(follows)
        if page:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)
        ser = self.get_serializer(follows, many=True)
        headers = self.get_success_headers(ser.data)
        return JsonResponse(status=http.HTTPStatus.OK,
                            data=ser.data, headers=headers, msg="OK", code=0)

    @action(methods=['get'], detail=False)
    def followed(self, request, *args, **kwargs):
        """
        获取关注当前用户的所有用户
        """
        user = request.user
        users = User.logic_objects.filter(profile_user__follow__id__contains=user.id)
        page = self.paginate_queryset(users)
        if page:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)
        ser = self.get_serializer(users, many=True)
        headers = self.get_success_headers(ser.data)
        return JsonResponse(status=http.HTTPStatus.OK,
                            data=ser.data, headers=headers, msg="OK", code=0)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.logic_objects.all()
    serializer_class = ProfileSerializer

    @action(methods=['get'], detail=False)
    def current_profile(self, request, *args, **kwargs):
        """
        获取当前用户的profile
        """
        user = request.user
        profile = UserProfile.logic_objects.filter(user=user.id).first()
        if not profile:
            raise UserError.ErrProfileNoExist
        serializer = self.get_serializer(profile)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(status=http.HTTPStatus.OK,
                            data=serializer.data, headers=headers, msg="OK", code=0)

    def create(self, request, *args, **kwargs):
        """
        重写create，增加user
        """
        user = request.user
        profile = UserProfile.logic_objects.filter(user=user.id).first()
        if profile:
            raise UserError.ErrProfileHasExist
        data_ = request.data.copy()
        data_['user'] = user
        serializer = self.get_serializer(data=data_)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(status=http.HTTPStatus.OK,
                            data=serializer.data, headers=headers, msg="OK", code=0)

    def update(self, request, *args, **kwargs):
        """
        重写update，增加user
        """
        user = request.user
        data_ = request.data.copy()
        data_['user'] = user.id
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META.get("HTTP_X_FORWARDED_FOR")
        else:
            ip = request.data.get('ip', None)
        if ip:
            data_["ip"] = ip
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=data_, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(status=http.HTTPStatus.OK,
                            data=serializer.data, headers=headers, msg="OK", code=0)


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
        sz = self.get_serializer(data=request.data.copy())
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

    def _login(self, phone_number: str, vcode: str, user: User) -> User:
        """登录流程，且对user的合法性进行检测

        Args:
            phone_number (str): _description_
            vcode (str): _description_
            user (User): _description_

        Raises:
            smerr.ValidCodeExpire: _description_

        Returns:
            User: _description_
        """
        register_key = "smg_{}".format(phone_number)
        token = cache.get(register_key, None)
        if token:
            if token != vcode:
                raise smerr.ValidCodeWrong
            if not user.is_active:
                raise smerr.UserNotActive
            if user.is_delete:
                raise smerr.UserHasDeleted
            return user
        raise smerr.ValidCodeExpire

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.data["phone_number"]
        vcode = serializer.data["validate_code"]
        username = serializer.data.get("username", "")
        # 先判断，是否存在该user，如果存在，则不再创建
        user = User.logic_objects.filter(
            phone_number=phone_number)  # 为queryset，需要取第一个值
        if not user:
            data = self._register(phone_number, vcode, username)
            user = User()
            user.username = data["username"]
            user.set_password(get_user_password())
            user.phone_number = data["phone_number"]
            user.save()
        else:
            user = self._login(phone_number, vcode, user[0])
        # 注册用户后默认生成profile数据
        profile = UserProfile.logic_objects.filter(user__id=user.id)
        # 注册用户后，默认登录
        refresh = RefreshToken.for_user(user)
        res_data = {
            "username": user.username,
            "phone_number": user.phone_number,
            "user_id": user.id,
            "user_profile_id": profile[0].id if profile else "",
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
        return Response(status=http.HTTPStatus.OK, data={"code": 0, "message": "OK", "data": res_data})


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
            err.set_message(res["Message"])
            err.set_params(res)
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
        serializer = self.get_serializer(data=request.data.copy())
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
            warn.set_message("手机验证码请求已经存在，并且还未经过60秒失效")
            raise warn

        # token 为None意味着，可以重新请求验证码
        cache.set("req_{}".format(phone_number), "", timeout=60)  # 设置60秒的失效时间
        vcode = "".join(random.choices(consts.NUM, k=6))  # 形似 654789

        # 搜索smg_phonenumber对应的token，如果存在，则删除重新写入，如果不存在，直接写入
        if cache.get("smg_{}".format(phone_number), default=None):
            cache.delete("smg_{}".format(phone_number))

        # 发送信息，如果没有报错，说明信息正确发出
        self._send_message(phone_number, vcode)
        cache.set("smg_{}".format(phone_number), vcode, timeout=5 * 60)  # 5分钟的失效
        return Response(status=http.HTTPStatus.OK, data={"code": 0, "message": "OK", "data": {}})
