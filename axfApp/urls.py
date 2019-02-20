from django.conf.urls import url
from . import views
urlpatterns = [
    url(r"^home/$",views.home,name="home"),
    url(r"^market/(\d+)/(\d+)/(\d+)/$",views.market,name="market"),
    url(r"^car/$",views.car,name="car"),
    url(r"^mine/$",views.mine,name="mine"),
    url(r"^login/$",views.login,name="login"),
    url(r"^register/$",views.register,name="register"),
    url(r"^checkuserid/$",views.checkuserid,name="checkuserid"),
    url(r"^checkemail/$",views.checkemail,name="checkemail"),

]