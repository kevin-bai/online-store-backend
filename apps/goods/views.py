from django.shortcuts import render

# Create your views here.
from .models import Goods,GoodsCategory,GoodsCategoryBand,GoodsImage
from .serializers import GoodsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class GoodsListView(APIView):
    """
    商品列表
    """
    def get(self, request, format=None):
        goods = Goods.objects.all()[:10]
        # many参数表示goods是复数，单个的话不用配置
        serializer = GoodsSerializer(goods, many=True)
        return Response(serializer.data)

