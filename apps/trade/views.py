from django.shortcuts import render

from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShoppingCartSerializer
from .models import ShoppingCart


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    购物车功能
    create:
        创建购物车记录
    list:
        购物车记录列表
    update:
        购物车更新
    delete:
        删除购物车记录
    """
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)