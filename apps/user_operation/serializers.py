# _*_ coding:utf-8 _*_

__author__ = 'kevin'
__date__ = '2018/5/11 10:16'

from rest_framework import serializers
from .models import UserFav


class UserFavSerializer(serializers.ModelSerializer):
    # 隐藏user，设为当前登录的user
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        # 要删除功能，必须加id字段
        fields = ("user", "goods", "id")
