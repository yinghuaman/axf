from django.shortcuts import render,redirect

# Create your views here.
from django.shortcuts import render
from .models import Wheel,Nav,Mustbuy,Shop,Mainshow,FoodType,Goods,User,Cart
import time
import random
from django.conf import settings
import os
# Create your views here.
def home(request):
    wheel = Wheel.objects.all()
    nav = Nav.objects.all()
    mustbuyList = Mustbuy.objects.all()
    mainList = Mainshow.objects.all()
    shopList = Shop.objects.all()
    shop1 = shopList[0]
    shop2 = shopList[1:3]
    shop3 = shopList[3:7]
    shop4 = shopList[7:]
    return render(request,"axfApp/home.html",{"title":"首页","wheelsList":wheel,"navList":nav,"mustbuyList":mustbuyList,"shop1":shop1,"shop2":shop2,"shop3":shop3,"shop4":shop4,"mainList":mainList})

def market(request,categoryid,cid,sortid):
    foodTypes = FoodType.objects.all()
    if cid == '0':
        goods = Goods.objects.all().filter(categoryid = categoryid)
    else:
        goods = Goods.objects.all().filter(categoryid=categoryid,childcid=cid)
    childtypenames = foodTypes.get(typeid = categoryid).childtypenames
    childList = []
    arr = childtypenames.split("#")
    for item in arr:
        arr2 = item.split(":")
        child = {"childName":arr2[0],"childid":arr2[1]}
        childList.append(child)

    #排序
    if sortid == '1':
        goods = goods.order_by("productnum")
    elif sortid == '2':
        goods = goods.order_by("price")
    else:
        goods = goods.order_by("-price")

    return render(request,"axfApp/market.html",{"title":"闪购超市","leftSlider":foodTypes,"productList":goods,"childList":childList,"categoryid":categoryid,"cid":cid})

def car(request):
    return render(request,"axfApp/cart.html",{"title":"购物车"})

#修改购物车
def changecart(request,flag):
    #判断用户是否登录
    token = request.session.get("userToken")
    #print(token)
    if token == None:
        return JsonResponse({"data":-1,"status":"error"})

    productid = request.POST.get("productid")
    product = Goods.objects.get(productid=productid)
    user = User.objects.get(userToken=token)
    if flag == '0':
        carts = Cart.objects.filter(userAccount=user.userAccount)
        car = None
        if carts.count() == 0:
            #直接增加一条订单
            car = Cart.createcart(user.userAccount,productid,1,product.price,True,product.productimg,product.productlongname,0,False)
            car.save()
        else:
            try:
                car = carts.get(productid=productid)
                #拿到订单，则修改数量和价格
                car.productnum += 1
                car.productprice = car.productprice*car.productnum
                car.save()
            except Cart.DoesNotExist as e:
                #直接增加订单
                car = Cart.createcart(user.userAccount, productid, 1, product.price, True, product.productimg,product.productlongname, 0, False)
                car.save()

        return JsonResponse({"data":car.productnum,"status":"success"})
















def mine(request):
    username = request.session.get("username","未登录")
    if username == "未登录":
        userRank = 0
    else:
        userRank = User.objects.get(username=username).userRank
    return render(request,"axfApp/mine.html",{"title":"我的","username":username,"userRank":userRank})

from .forms.login import LoginForm
from django.http import HttpResponse,JsonResponse
def login(request):
    if request.method == 'POST':
        name = request.POST.get("username")
        pwd = request.POST.get("password")
        try:
            user = User.objects.get(username=name)
            if user.password != pwd:
                return redirect("/login/")
        except User.DoesNotExist as e:
            return redirect("/login/")
        #登陆成功
        user.userToken = str(time.time() + random.randrange(1,1000000))
        user.save()
        request.session["userToken"] = user.userToken
        request.session["username"] = user.username
        return redirect("/mine/")
    else:
        return render(request,"axfApp/login.html",{"title":"登陆"})

def register(request):
    if request.method == 'POST':
        userAccount = request.POST.get("userAccount")
        username = request.POST.get("username")
        passwd =request.POST.get("password")
        userPhone = request.POST.get("userPhone")
        userRank = 0
        email = request.POST.get("email")
        userToken = str(time.time() + random.randrange(1,1000000))
        f = request.FILES["img"]
        icon = os.path.join(settings.META_ROOT,userAccount + ".png")
        with open(icon,"wb") as fp:
            for data in f.chunks():
                fp.write(data)

        user = User.createuser(userAccount,username,passwd,userPhone,userRank,email,userToken,icon)
        user.save()

        request.session["username"] = username
        request.session["userToken"] = userToken

        return redirect("/mine/")
    else:
        return render(request,"axfApp/register.html",{"title":"注册"})

from django.contrib.auth import logout
def quit(request):
    logout(request)
    return redirect("/mine/")

def checkuserid(request):
    userid = request.POST.get("userid")

    try:
        user = User.objects.get(userAccount=userid)
        return JsonResponse({"data":"该用户已被注册","status":'error'})
    except User.DoesNotExist as e:
        return JsonResponse({"data":"不存在","status":'success'})

def checkemail(request):
    email = request.POST.get("email")

    try:
        email = User.objects.get(email=email)
        return JsonResponse({"data":"该邮箱已被注册","status":'error'})
    except User.DoesNotExist as e:
        return JsonResponse({"data":"不存在","status":'success'})

def checkusertel(request):
    usertel = request.POST.get("usertel")
    try:
        userphone = User.objects.get(userPhone=usertel)
        return JsonResponse({"data":"该号码已被注册","status":"error"})
    except User.DoesNotExist as e:
        return JsonResponse({"data":"该号码未被注册","status":"success"})




