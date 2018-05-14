# _*_ coding:utf-8 _*_

__author__ = 'kevin'
__date__ = '2018/5/7 21:42'

from django.contrib.auth import get_user_model
import re
from datetime import datetime, timedelta

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

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


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, max_length=4, min_length=4,
                                 error_messages={
                                     'blank': '请输入验证码',
                                     'required': "请输入验证码",
                                     'max_length': '验证码最大4位',
                                     'min_length': '验证码最小4位'
                                 },
                                 write_only=True,
                                 help_text="请输入4位验证码", label="验证码")
    username = serializers.CharField(required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")],
                                     error_messages={
                                         'blank': '请输入验证码',
                                     })
    password = serializers.CharField(required=True, style={'input_type': 'password'}, label="密码", write_only=True)

    def validate_code(self, code):
        """
        验证码验证
        :param code:
        :return:
        """

        # 为什么不用get
        # 1: 可能有2条记录的，完全有可能验证码相同的2条数据。 2.找不到匹配的
        # 这2种情况 get都会给我抛异常。我们要去捕获异常，还要去处理。用filter容易多了
        # try:
        #     verify_records = VerifyCode.objects.get(mobile=self.initial_data["username"], code=code)
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass

        # self.initial_data 里面放的是前端传送过来的值
        # 一定要倒叙排序，我们只要验证最新的一条就行了
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by('-add_time')
        if not verify_records:
            raise serializers.ValidationError('验证码错误')

        last_record = verify_records[0]
        five_min_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
        if five_min_ago > last_record.add_time:
            raise serializers.ValidationError('验证码过期，超过5分钟')
        if str(last_record) != code:
            raise serializers.ValidationError('验证码错误')

        return code

    # 加密逻辑转移到signals
    # def create(self, validated_data):
    #     user = super().create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validate(self, attrs):
        # 不需要用户传递mobile，直接可以username赋值给mobile
        attrs['mobile'] = attrs['username']
        # 某个字段不属于指定model，它是write_only，需要用户传进来，但我们不能对它进行save( )，
        # 如在用户注册时，我们需要填写验证码，这个验证码只需要验证，不需要保存到用户这个Model中：
        del attrs['code']
        return attrs

    class Meta:
        model = User
        # username:这里用的userprofile继承了AbstractUser，username是必填项
        # code: 这个字段不在model里，我们在上面定义了，才能这么写
        fields = ("username", "code", "mobile", "password")


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详细信息
    """
    class Meta:
        model = User
        fields = (  "nick_name","birthday", "gender", "email", "mobile",)
