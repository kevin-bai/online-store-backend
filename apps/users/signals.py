# _*_ coding:utf-8 _*_

__author__ = 'kevin'
__date__ = '2018/5/8 16:08'

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


# 装饰器，sender是接收对象
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    # 如果是新建的
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()
        # 用jwt就不用加token了
        # Token.objects.create(user=instance)
