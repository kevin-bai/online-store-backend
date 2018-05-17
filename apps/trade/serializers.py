# _*_ coding:utf-8 _*_

__author__ = 'kevin'
__date__ = '2018/5/15 16:05'

from rest_framework import serializers

from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.models import Goods
from goods.serializers import GoodsSerializerAll


class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializerAll(many=False)

    class Meta:
        model = ShoppingCart
        fields = "__all__"


class ShoppingCartSerializer(serializers.Serializer):
    """
    购物车
    """
    # 这里不用ModelSerializer,因为当点击加入购物车，此时购物车列表已经存在，这个记录。我们model里面写了unique_together = ("user", "goods")
    # 那么会直接抛异常，而我们希望这个记录数量加1
    # 所以要自己控制
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M")
    nums = serializers.IntegerField(required=True, min_value=1, help_text="商品数量", error_messages={"required": "请填写数量",
                                                                                                  "min_value": "数量至少为1"
                                                                                                  })
    # 这里不是ModelSerializer 在Meta中写好对应的model,需要在参数中指定queryset。
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all(), required=True, help_text="商品id")

    def create(self, validated_data):
        # 在serializer中，requset不直接放在self里，views.py里面 倒是可以直接 self.request.user
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]

        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            # 这里不用加user？
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        instance.nums = validated_data["nums"]
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_status = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)

    def generator_order_sn(self):
        # 时间+userid+随机字符串
        import time
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{user_id}{random_str}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                            user_id=self.context["request"].user.id,
                                                            random_str=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generator_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializerAll(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    # 根据relate_name 取得
    # 本身OrderInfo 没有goods这个字段，但是OrderGoods有goods这个外键和order这个外键，通过relate_name 连接到
    OrderGoods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = "__all__"


