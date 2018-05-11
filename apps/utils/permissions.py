# _*_ coding:utf-8 _*_
"""
    自定义权限
"""
__author__ = 'kevin'
__date__ = '2018/5/11 13:31'

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
            # GET, HEAD or OPTIONS 这些安全的请求，不进行permission验证
        if request.method in permissions.SAFE_METHODS:
            return True

        # 请求删除的user，和我们当前的user做对比
        return obj.user == request.user
