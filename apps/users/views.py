from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import Profile
from .serializers import UserSerializer, ProfileSerializer, BlackTokenSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all().order_by('id')
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
