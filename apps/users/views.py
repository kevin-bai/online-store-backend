from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
# Create your views here.

from django.contrib.auth import get_user_model

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证，重写authenticate
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 通过Q 实现查找的or操作， 用户可以用username 或者mobile登录
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            print('pass')
            # 通过user继承的AbstractUser中的方法
            if user.check_password(password):
                return user
        except Exception as e:
            return None