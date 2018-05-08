from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from random import choice

from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from .serializers import SmsSerializer
from utils.yunpian import YunPian
from online_store_backend.settings import yunpian_apikey
from .models import VerifyCode

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证，重写authenticate
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 通过Q 实现查找的or操作， 用户可以用username 或者mobile登录
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            # 通过user继承的AbstractUser中的方法
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    """
    create:
        发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成4位数字验证码
        :return:
        """
        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)  # 把数组转成字符串

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # 这里异常，会抛http 400，能返回给前端
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']
        yunpian = YunPian(yunpian_apikey)

        code = self.generate_code()

        sms_status = yunpian.send_sms(mobile=mobile, code=code)

        if sms_status['code'] != 0:
            return Response({
                'mobile': sms_status['msg']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code,mobile=mobile)
            code_record.save()
            return Response({
                'mobile': mobile
            }, status=status.HTTP_201_CREATED)

        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
