# _*_ coding:utf-8 _*_

__author__ = 'kevin'
__date__ = '2018/5/11 10:16'
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers

from .models import UserFav, UserLeavingMessage


class UserFavSerializer(serializers.ModelSerializer):
    # 隐藏user，设为当前登录的user
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav

        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"
            )
        ]

        # 要删除功能，必须加id字段
        fields = ("user", "goods", "id")


class UserMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    message_type = serializers.IntegerField(help_text=u"留言类型: 1(留言),2(投诉),3(询问),4(售后),5(求购)")
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")
    """
    用户留言
    """

    class Meta:
        model = UserLeavingMessage
        fields = ("id", "message_type", "subject", "message", "file", "user", "add_time")
