# _*_ coding:utf-8 _*_

__author__ = 'kevin'
__date__ = '2018/5/7 21:42'

from django.contrib.auth import get_user_model
import re
from datetime import datetime, timedelta

from rest_framework import serializers

from .models import VerifyCode
from utils.regex import REGEX_MOBILE

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        手机号码验证
        :param mobile:
        :return:
        """

        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('该手机号已存在')

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码不合法")

        # 验证发送频率
        one_min_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(mobile=mobile, add_time__gt=one_min_ago).count():
            raise serializers.ValidationError('请求验证过快,每分钟最多1次')

        return mobile
