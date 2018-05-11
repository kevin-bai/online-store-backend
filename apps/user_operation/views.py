from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import UserFavSerializer
from .models import UserFav


class UserFavViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    list:
        收藏列表
    create:
        创建用户收藏
    destroy:
        取消用户收藏
    """
    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer

