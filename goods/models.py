from django.db import models

# Create your models here.
# 商品分类表

class GoodsCategary(models.Model):
    # 分类名称
    cag_name = models.CharField(max_length=30)
    # 分类样式
    cag_css = models.CharField(max_length=20)
    # 分类图片
    cag_img = models.ImageField(upload_to='cag')

# 商品表
class GoodsInfo(models.Model):
    # 商品名字
    goods_name = models.CharField(max_length=100, verbose_name='商品名字')
    # 商品价格
    goods_price = models.IntegerField(default=0, verbose_name='价格')
    # 商品描述
    goods_desc = models.CharField(max_length=2000)
    # 商品图片
    goods_img = models.ImageField(upload_to='goods')
    # 商品的分类
    goods_cag = models.ForeignKey('GoodsCategary', on_delete=models.CASCADE)

    def __str__(self):
        return self.goods_name