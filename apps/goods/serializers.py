# _*_ coding:utf-8 _*_

__author__ = 'kevin'
__date__ = '2018/5/2 17:26'

from rest_framework import serializers
from .models import Goods, GoodsImage, GoodsCategoryBand, GoodsCategory


class GoodsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    click_num = serializers.IntegerField(default=0, )
    goods_front_image = serializers.ImageField()
