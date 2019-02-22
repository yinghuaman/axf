from django.db import models

# Create your models here.
class Wheel(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)

class Nav(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)

class Mustbuy(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)

class Shop(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)

class Mainshow(models.Model):
    trackid = models.CharField(max_length=20)
    categoryid = models.CharField(max_length=10)
    brandname = models.CharField(max_length=20)
    img = models.CharField(max_length=100)
    name = models.CharField(max_length=20)

    img1 = models.CharField(max_length=100)
    childcid1 = models.CharField(max_length=10)
    productid1 = models.CharField(max_length=10)
    longname1 = models.CharField(max_length=50)
    price1 = models.CharField(max_length=10)
    marketprice1 = models.CharField(max_length=10)

    img2 = models.CharField(max_length=100)
    childcid2 = models.CharField(max_length=10)
    productid2 = models.CharField(max_length=10)
    longname2 = models.CharField(max_length=50)
    price2 = models.CharField(max_length=10)
    marketprice2 = models.CharField(max_length=10)

    img3 = models.CharField(max_length=100)
    childcid3 = models.CharField(max_length=10)
    productid3 = models.CharField(max_length=10)
    longname3 = models.CharField(max_length=50)
    price3 = models.CharField(max_length=10)
    marketprice3 = models.CharField(max_length=10)

class FoodType(models.Model):
    typeid = models.CharField(max_length=10)
    typename = models.CharField(max_length=50)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField(default=1)

class Goods(models.Model):
    productid = models.CharField(max_length=16)  # 商品的id
    productimg = models.CharField(max_length=200)  # 商品的图片
    productname = models.CharField(max_length=100)  # 商品的名称
    productlongname = models.CharField(max_length=200)  # 商品的规格
    isxf = models.IntegerField(default=1) #是否精选
    pmdesc = models.CharField(max_length=100)  #是否买一送一
    specifics = models.CharField(max_length=100)  # 规格
    price = models.FloatField(default=0)  # 商品的折后价格
    marketprice = models.FloatField(default=1)  # 商品的原价
    categoryid = models.CharField(max_length=16)  # 分类的id
    childcid = models.CharField(max_length=16)  # 子分类的id
    childcidname = models.CharField(max_length=100)  # 子分类的名称
    dealerid = models.CharField(max_length=16)
    storenums = models.IntegerField(default=1)  # 库存
    productnum = models.IntegerField(default=1)  # 销量排序

class User(models.Model):
    userAccount = models.CharField(max_length=20)
    username = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=256)
    userPhone = models.CharField(max_length=15)
    userRank = models.IntegerField()
    email = models.CharField(max_length=64, unique=True)
    userToken = models.CharField(max_length=50)#保证在没有关闭网站前一直保存用户信息
    icon = models.CharField(max_length=150)
    is_delete = models.BooleanField(default=False)
    @classmethod
    def createuser(cls,userAccount,username,password,userPhone,userRank,email,userToken,icon,is_delete=False):
        u = cls(userAccount=userAccount,username=username,password=password,userPhone=userPhone,userRank=userRank,email=email,userToken=userToken,icon=icon,is_delete=is_delete)
        return u
class CartManager1(models.Manager):
    def get_queryset(self):
        return super(CartManager1,self).get_queryset().filter(lsDelete=False)
class CartManager2(models.Manager):
    def get_queryset(self):
        return super(CartManager2,self).get_queryset().filter(lsDelete=True)
class Cart(models.Model):
    userAccount = models.CharField(max_length=20)
    productid = models.CharField(max_length=10)
    productnum = models.IntegerField()
    productprice = models.FloatField()
    isChose = models.BooleanField(default=True)
    productimg = models.CharField(max_length=150)
    productname = models.CharField(max_length=100)
    orderid = models.CharField(max_length=20,default="0")
    lsDelete = models.BooleanField(default=False)
    objects = CartManager1()#不用更改数据库字段，所以就不用再迁移
    obj = CartManager2()
    @classmethod
    def createcart(cls,userAccount,productid,productnum,productprice,isChose,productimg,productname,orderid,lsDelete):
        cart = cls(userAccount=userAccount,productid=productid,productnum=productnum,productprice=productprice,isChose=isChose,productimg=productimg,productname=productname,orderid=orderid,lsDelete=lsDelete)
        return cart


class Order(models.Model):
    orderid = models.CharField(max_length=20)
    userAccount = models.CharField(max_length=20)
    progress = models.IntegerField()

    @classmethod
    def createorder(cls,orderid,userAccount,progress):
        order = cls(orderid=orderid,userAccount=userAccount,progress=progress)
        return order

