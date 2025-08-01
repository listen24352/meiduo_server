"""

https://docs.djangoproject.com/en/1.11/howto/custom-file-storage/

1. 您的自定义存储系统必须是的子类 django.core.files.storage.Storage
2. Django必须能够在没有任何参数的情况下实例化您的存储系统
        我们在创建存储类的时候，不传递任何参数
3. 您的存储类必须实现_open()和_save() 方法，以及适用于您的存储类的任何其他方法
    url
"""

from django.core.files.storage import Storage


class MyStorage(Storage):

    def _open(self, name, mode='rb'):
        """Retrieve the specified file from storage."""
        pass

    def _save(self, name, content, max_length=None):
        pass

    def exists(self, name):
        # 判断图片是否存在
        # Fdfs 自己可以实现 图片重名的处理
        # 返回False 说明图片不存在,就直接上传就可以
        return False

    def url(self, name):
        # return "http://192.168.154.133:8888/" + name
        return "http://47.92.126.69:8888/" + name
