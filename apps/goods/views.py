from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# Create your views here.
from .models import Goods, GoodsCategory, GoodsCategoryBand, GoodsImage
from .serializers import GoodsSerializer, GoodsSerializerAll
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics


class GoodsListView(APIView):
    """
    商品列表
    """

    def get(self, request, format=None):
        goods = Goods.objects.all()[:10]
        # many参数表示goods是复数，单个的话不用配置
        serializer = GoodsSerializerAll(goods, many=True)
        return Response(serializer.data)

    def post(self, request):
        # 这个request不再是django的request，DRF对request进行了一次封装
        data = JSONParser().parse(request)
        serializer = GoodsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# generics.GenericAPIView 对APIView进行了一层封装，加了filter，分页等等
class GoodsListView2(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    """
    用mixin和GenericAPIView
    """
    queryset = Goods.objects.all()[:10]
    serializer_class = GoodsSerializerAll

    # mixins.ListModelMixin 对应get。封装了一些功能
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # mixins.CreateModelMixin 对应post，创建。
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class GoodsListView3(generics.ListAPIView,
                     generics.CreateAPIView):
    """
    继承generics.ListAPIView
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializerAll
