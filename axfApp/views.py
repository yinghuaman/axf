from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Wheel,Nav,Mustbuy,Shop,Mainshow
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

def market(request):
    return render(request,"axfApp/market.html",{"title":"闪购超市"})

def car(request):
    return render(request,"axfApp/cart.html",{"title":"购物车"})

def mine(request):
    return render(request,"axfApp/mine.html",{"title":"我的"})


