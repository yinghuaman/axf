from django.shortcuts import render,redirect

# Create your views here.
from django.shortcuts import render
from .models import Wheel,Nav,Mustbuy,Shop,Mainshow,FoodType,Goods,User,Cart,Order
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
        productList = Goods.objects.all().filter(categoryid = categoryid)
    else:
        productList = Goods.objects.all().filter(categoryid=categoryid,childcid=cid)
    childtypenames = foodTypes.get(typeid = categoryid).childtypenames
    childList = []
    arr = childtypenames.split("#")
    for item in arr:
        arr2 = item.split(":")
        child = {"childName":arr2[0],"childid":arr2[1]}
        childList.append(child)

    #排序
    if sortid == '1':
        productList = productList.order_by("productnum")
    elif sortid == '2':
        productList = productList.order_by("price")
    else:
        productList = productList.order_by("-price")

    #显示某用户购物车里的所有商品
    token = request.session.get("userToken")#验证登录
    cartList = []
    if token:
        userAccount = User.objects.get(userToken=token).userAccount
        cartList = Cart.objects.filter(userAccount=userAccount)

    for pro in productList:
        pro.num = 0
        for cart in cartList:
            if pro.productid == cart.productid:
                pro.num = cart.productnum #不是数据库中的表字段，不用save()
                continue
    return render(request,"axfApp/market.html",{"title":"闪购超市","leftSlider":foodTypes,"productList":productList,"childList":childList,"categoryid":categoryid,"cid":cid})

def car(request):
    # 判断用户是否登录
    token = request.session.get("userToken")
    # print(token)
    cartList = []
    userAccount = ""
    userPhone = ""
    if token != None:
        userAccount = User.objects.get(userToken=token).userAccount
        userPhone = User.objects.get(userAccount=userAccount).userPhone
        cartList = Cart.objects.filter(userAccount=userAccount)
    totalprice = 0
    for cart in cartList:
        totalprice += cart.productprice
    return render(request,"axfApp/cart.html",{"title":"购物车","cartList":cartList,"userAccount":userAccount,"userPhone":userPhone,"totalprice":totalprice})

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
        if product.storenums == 0:
            return JsonResponse({"data": -2, "status": "error"})
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
                car.productprice = "%.2f"%(product.price*car.productnum)
                car.save()
            except Cart.DoesNotExist as e:
                #直接增加订单
                car = Cart.createcart(user.userAccount, productid, 1, product.price, True, product.productimg,product.productlongname, 0, False)
                car.save()
        product.storenums -= 1
        product.save()
        totalprice = float(request.POST.get("totalprice"))
        totalprice += product.price
        return JsonResponse({"data":[car.productnum,car.productprice],"totalprice":totalprice,"status":"success"})

    elif flag == "1":
        carts = Cart.objects.filter(userAccount=user.userAccount)
        car = None
        if carts.count() == 0:
            return JsonResponse({"data":-3,"status":"error"})
        else:

            try:
                car = carts.get(productid=productid)
                #拿到订单，则修改数量和价格
                car.productnum -= 1
                car.productprice = "%.2f"%(product.price*car.productnum)
                if car.productnum == 0:
                    car.delete()#数据库中删除数据，但网页的DOM元素要在JS中删除
                else:
                    car.save()
            except Cart.DoesNotExist as e:
                return JsonResponse({"data": -3, "status": "error"})
        product.storenums += 1
        product.save()
        totalprice = float(request.POST.get("totalprice"))
        totalprice -= product.price
        return JsonResponse({"data":[car.productnum,car.productprice],"totalprice":totalprice,"status":"success"})

    elif flag == "2":
        carts = Cart.objects.filter(userAccount=user.userAccount)
        c = carts.get(productid=productid)
        c.isChose = not c.isChose
        c.save()
        str1 = ""
        totalprice = float(request.POST.get("totalprice"))
        if c.isChose:
            str1 = "√"
            totalprice += c.productprice
        else:
            totalprice -= c.productprice
        return JsonResponse({"data":str1,"totalprice":totalprice,"status": "success"})


def saveorder(request):
    token = request.session.get("userToken")
    if not token:
        return JsonResponse({"data": -3, "status": "error"})

    user = User.objects.get(userToken=token)
    carts = Cart.objects.filter(userAccount=user.userAccount)
    if carts.count() == 0:
        return JsonResponse({"data": -3, "status": "error"})

    oid = time.time() + random.randrange(1,10000)
    oid = "%d"%(oid)
    order = Order.createorder(oid,user.userAccount,0)
    order.save()

    for item in carts.filter(isChose=True):
        item.orderid = oid
        item.lsDelete = True
        item.save()#保存到数据库
    return JsonResponse({"status": "success"})

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




