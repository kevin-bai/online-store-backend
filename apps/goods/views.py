from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, mixins, generics, viewsets
from rest_framework.decorators import action
from rest_framework import filters as rest_filter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

# Create your views here.
from .models import Goods, GoodsCategory, GoodsCategoryBrand, GoodsImage
from .serializers import GoodsSerializer, GoodsSerializerAll, CategorySerializerAll
from utils.DRF_PaginationSet import SmallResultsSetPagination, StandardResultsSetPagination,GoodsResultsSetPagination


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


class GoodsListView3(generics.ListCreateAPIView):
    """
    继承generics.ListAPIView
    """
    queryset = Goods.objects.all()[:13]
    # 序列化配置
    serializer_class = GoodsSerializerAll
    # 分页配置
    pagination_class = StandardResultsSetPagination


##########################################################################


class GoodsFilter(filters.FilterSet):
    # lookup_expr= 'gte' 相当于 order_by(xx__gte)   __后面跟着的操作
    pricemin = filters.NumberFilter(name='shop_price', lookup_expr='gte')
    pricemax = filters.NumberFilter(name='shop_price', lookup_expr='lte')
    name = filters.CharFilter(name='name', lookup_expr='icontains')
    top_category = filters.NumberFilter(method='top_category_filter', label='根据类别id筛选商品')

    # 查找某类别下的所有商品
    # 自定义filter函数，参数是固定的
    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['name', 'pricemin', 'pricemin']


class GoodsViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin):
    """
    list:
        商品列表页，分页，搜索，过滤，排序
    """
    queryset = Goods.objects.all().order_by('id')
    serializer_class = GoodsSerializerAll
    pagination_class = GoodsResultsSetPagination
    filter_backends = (DjangoFilterBackend, rest_filter.SearchFilter, rest_filter.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('=name', '^goods_brief')
    ordering_fields = ('id', 'shop_price', 'fav_num')


class GoodsCategoryViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    """
    list:
        商品目录列表
    retrieve:
        获取商品分类详情
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializerAll
    filter_backends = (DjangoFilterBackend,)
