from django.db import models

class Seller(models.Model):#卖家
    username = models.CharField(max_length=32,verbose_name="用户名")#用户名
    password = models.CharField(max_length=32, verbose_name="密码")#密码
    nickname = models.CharField(max_length=32, verbose_name="昵称",null=True,blank=True)#昵称
    phone = models.CharField(max_length=32, verbose_name="电话",null=True,blank=True)#电话
    email = models.EmailField(verbose_name="邮箱",null=True,blank=True)#邮箱
    picture = models.ImageField(upload_to="store/images", verbose_name="用户头像",null=True,blank=True)#图片
    address = models.CharField(max_length=32, verbose_name="地址",null=True,blank=True)#地址
    card_id = models.CharField(max_length=32, verbose_name="身份证",null=True,blank=True)#身份证


class StoreType(models.Model):#店铺类型
    store_type = models.CharField(max_length=32,verbose_name="类型名称")#类型名称
    type_description = models.TextField(verbose_name="类型描述")#类型描述


class Store(models.Model):#店铺
    store_name = models.CharField(max_length=32, verbose_name="店铺名称")#店铺名
    store_address = models.CharField(max_length=32,verbose_name="店铺地址")#店铺地址
    store_description = models.TextField(verbose_name="店铺描述")#店铺描述
    store_logo = models.ImageField(upload_to="store/images",verbose_name="店铺logo")#店铺logo
    store_phone = models.CharField(max_length=32,verbose_name="店铺电话")#店铺电话
    store_money = models.FloatField(verbose_name="店铺注册资金")#店铺注册资金
    user_id = models.IntegerField(verbose_name="店铺主人")#用户ID
    type = models.ManyToManyField(to=StoreType,verbose_name="店铺类型")#店铺类型


class Goods(models.Model):#商品
    goods_name = models.CharField(max_length=32,verbose_name="商品名称")#商品名称
    goods_price = models.FloatField(verbose_name="商品价格")#商品价格
    goods_image = models.ImageField(upload_to="store/images", verbose_name="商品图片")#商品图片
    goods_number = models.IntegerField(verbose_name="商品数量库存")#商品库存
    goods_description = models.TextField(verbose_name="商品描述")#商品描述
    goods_date = models.DateField(verbose_name="出厂日期")#出厂日期
    goods_safeDate = models.IntegerField(verbose_name="保质期")#保质期

    store_id = models.ManyToManyField(to=Store,verbose_name="商品店铺")#商品店铺


class GoodsImg(models.Model):#商品图片
    img_address = models.ImageField(upload_to="store/images",verbose_name="图片地址")#图片地址
    img_description = models.TextField(max_length=32, verbose_name="图片描述")#图片描述

    goods_id = models.ForeignKey(to = Goods,on_delete = models.CASCADE, verbose_name="商品id")#商品ID
# Create your models here.
