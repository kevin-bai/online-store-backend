# _*_ coding:utf-8 _*_

__author__ = 'kevin'
__date__ = '2018/4/30 10:49'

import os

path = u'E:\前端学习\[全栈开发 ]Vue+Django REST framework 打造生鲜电商项目'  # project-paht
for prefix, dirs, files in os.walk(path):
    for name in files:
        if name.startswith(u'IT情报站【www.code688.com】'):
            filename = os.path.join(prefix, name)
            oldname = name
            newname = name.replace(u'IT情报站【www.code688.com】', '')
            old = prefix +"\\" + oldname
            new = prefix +"\\" + newname
            print(new)
            os.rename(old,new)
