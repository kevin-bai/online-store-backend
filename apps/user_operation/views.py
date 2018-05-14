from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .serializers import UserFavSerializer,UserMessageSerializer
from .models import UserFav,UserLeavingMessage
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """
    list:
        收藏列表
    create:
        创建用户收藏
    destroy:
        取消用户收藏
    retrieve:
        获取某个收藏信息
    """
    # queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # 获取详情，查找的字段id改成goods_id
    lookup_field = "goods_id"

    # 重载queryset，只获取当前用户的收藏
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)


class UserMessageViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    """
    list:
        获取用户留言信息
    create:
        添加留言
    destroy:
        删除用户留言
    """
    serializer_class = UserMessageSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)