# _*_ coding:utf-8 _*_

__author__ = 'kevin'
__date__ = '2018/5/2 17:26'

from rest_framework import serializers
from .models import Goods, GoodsImage, GoodsCategoryBrand, GoodsCategory


class GoodsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)
    click_num = serializers.IntegerField(default=0, )
    goods_front_image = serializers.ImageField()

    # validated_data就是传进来的所有信息是个dict
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Goods.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


class CategorySerializerAll3(serializers.ModelSerializer):
    """
    商品类别序列化3
    """

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializerAll2(serializers.ModelSerializer):
    """
    商品类别序列化2
    """
    sub_cat = CategorySerializerAll3(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializerAll(serializers.ModelSerializer):
    """
    商品类别序列化1
    """
    sub_cat = CategorySerializerAll2(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


# 用ModelSerializer
class GoodsSerializerAll(serializers.ModelSerializer):
    # 重写category外键，用上面的 CategorySerializer实例替代
    category = CategorySerializerAll()

    class Meta:
        model = Goods
        # fields = ('name', 'click_num', 'goods_front_image', 'add_time')
        fields = '__all__'


class GoodsImageSerializerAll(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = '__all__'


class GoodsCategoryBandSerializerALL(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'
