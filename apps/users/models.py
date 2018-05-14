from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户
    """
    nick_name = models.CharField(max_length=20, null=True, blank=True, verbose_name='用户昵称')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name='手机')
    gender = models.CharField(max_length=6, choices=(('male', '男'), ('female', '女')), default='male', verbose_name='性别')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='邮箱')
    image = models.ImageField(upload_to='users/', max_length=150, verbose_name='头像')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    短信验证码，正式项目也可以放在redis里，不放数据库
    """
    code = models.CharField(max_length=10, verbose_name='验证码')
    mobile = models.CharField(max_length=11, verbose_name='手机')

    # 一般项目都会有这3个字段，
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    update_time = models.DateTimeField(default=datetime.now, verbose_name='更改时间')
    # 有的数据库做删除，是只做删除标记，没有真的删除
    is_deleted = models.DateTimeField(default=datetime.now, verbose_name='是否删除')

    class Meta:
        verbose_name = '短信验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
