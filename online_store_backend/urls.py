"""online_store_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.static import serve

import xadmin
from online_store_backend.settings import MEDIA_ROOT
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from goods.views import GoodsListView3, GoodsViewSet

router = DefaultRouter()
# router 自动生成的url配置，get，post等是根据 GoodsViewSet里的mixin来生成的，比如：
# ListModelMixin 就会生成get的配置，CreateModelMixin就是post
router.register(r'goods', GoodsViewSet)

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    # media文件路径
    url(r'^media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),
    # DRF文档功能
    url(r'^docs/', include_docs_urls(title="生鲜超市")),
    # DRF登录配置
    url(r'^api-auth/', include('rest_framework.urls')),
    # 路由注册
    url(r'^', include(router.urls)),
    # url(r'^goods/$', GoodsListView3.as_view()),
]
