from django.utils.text import gettext_lazy as _
from rest_framework import serializers
from . import models
from . import model2
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'username', 'phone_number')


class ProfileSerializer(serializers.ModelSerializer):

    phone_number = serializers.CharField(max_length=14, read_only=True)
    current_user_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=50, read_only=True)

    class Meta:
        model = model2.UserProfile
        fields = '__all__'
        extra_kwargs = {
            "ip": {"required": False, "allow_null": True},
            "user": {"required": False, "allow_null": True},
        }


class BlackTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class RegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        min_length=11, max_length=11, trim_whitespace=True)
    validate_code = serializers.CharField(max_length=6, trim_whitespace=True)
    username = serializers.CharField(
        max_length=50, allow_blank=True, trim_whitespace=True)

    def to_internal_value(self, data):
        if 'username' not in data:
            data['username'] = ""
        return super(RegisterSerializer, self).to_internal_value(data)


class MobileSendMessageSerializer(serializers.Serializer):
    """手机号码请求验证码
    """
    phone_number = serializers.CharField(
        min_length=11, max_length=11, trim_whitespace=True)
