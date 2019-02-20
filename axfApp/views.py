from django.shortcuts import render,redirect

# Create your views here.
from django.shortcuts import render
from .models import Wheel,Nav,Mustbuy,Shop,Mainshow,FoodType,Goods,User
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

def mine(request):
    return render(request,"axfApp/mine.html",{"title":"我的"})

from .forms.login import LoginForm
from django.http import HttpResponse,JsonResponse
def login(request):
    if request.method == 'POST':
        f = LoginForm(request.POST)
        if f.is_valid():
            #信息格式没有问题，验证账号和密码的正确性
            name = f.cleaned_data["username"]
            pwd = f.cleaned_data["password"]
            return redirect("/mine/")
        else:
            return render(request,"axf/login.html",{"title":"登陆","form":f,"error":f.errors})
    else:
        f = LoginForm()
    return render(request,"axfApp/login.html",{"title":"登陆"})


def register(request):
    if request.method == 'POST':
        pass
    else:
        return render(request,"axfApp/register.html")

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




