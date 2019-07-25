import hashlib

from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect

from Store.models import *


def loginValid(fun):
    def inner(request,*args,**kwargs):
        c_user = request.COOKIES.get("username")
        s_user = request.session.get("username")
        if c_user and s_user and c_user == s_user:
            user = Seller.objects.filter(username=c_user).first()
            if user:
                return fun(request,*args,**kwargs)
        return HttpResponseRedirect("/Store/login/")
    return inner

def set_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result

def register(request):
    """
    register注册
    返回注册页面
    进行注册数据保存
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            seller = Seller()
            seller.username = username
            seller.password = set_password(password)
            seller.nickname = username
            seller.save()
            return HttpResponseRedirect("/Store/login/")
    return render(request,"store/register.html")

def login(request):
    """
    登陆功能，如果登陆成功，跳转到首页
    如果失败，跳转到登陆页
    """
    response = render(request,"store/login.html")
    response.set_cookie("login_from","login_page")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user = Seller.objects.filter(username = username).first()
            if user:
                web_password = set_password(password)
                cookies = request.COOKIES.get("login_from")
                if user.password == web_password and cookies == "login_page":
                    response = HttpResponseRedirect("/Store/index/")
                    response.set_cookie("username",username)
                    response.set_cookie("user_id",user.id)
                    request.session["username"] = username
                    store = Store.objects.filter(user_id=user.id).first()
                    if store:
                        response.set_cookie("has_store",store.id)
                    else:
                        response.set_cookie("has_store","")
                    return response
    return response

@loginValid
def index(request):
    user_id = request.COOKIES.get("user_id")
    if user_id:
        user_id = int(user_id)
    else:
        user_id = 0
    store = Store.objects.filter(user_id=user_id).first()
    if store:
        is_store = 1
    else:
        is_store = 0
    return render(request,"store/index.html",{"is_store":is_store})


def base(request):
    return render(request,"store/base.html")
def register_store(request):

    type_list = StoreType.objects.all()
    if request.method == "POST":
        post_data = request.POST #接收post数据
        store_name = post_data.get("store_name")
        store_description = post_data.get("store_description")
        store_phone = post_data.get("store_phone")
        store_money = post_data.get("store_money")
        store_address = post_data.get("store_address")

        user_id =int(request.COOKIES.get("user_id")) #通过cookie来得到user_id
        type_list = post_data.get("type") #通过request.post得到类型，但是是一个列表

        store_logo = request.FILES.get("store_logo") #通过request.FILES得到

        #保存非多对多数据
        store = Store()
        store.store_name = store_name
        store.store_description = store_description
        store.store_phone = store_phone
        store.store_money = store_money
        store.store_address = store_address
        store.user_id = user_id
        store.store_logo = store_logo
        store.save()

        for i in type_list:
            store_type = StoreType.objects.get(id = i)
            store.type.add(store_type)
        store.save()

    return render(request,"Store/register_store.html",locals())
# Create your views here.
def add_goods(request):
    if request.method == "POST":
        goods_name = request.POST.get("goods_name")
        goods_price = request.POST.get("goods_price")
        goods_number = request.POST.get("goods_number")
        goods_description = request.POST.get("goods_description")
        goods_safeDate = request.POST.get("goods_safeDate")
        goods_image = request.FILES.get("goods_image")
        goods_date = request.POST.get("goods_date")

        goods = Goods()
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        goods.goods_image = goods_image
        goods.save()

        # goods.store_id.add(
        #     Store.objects.get(id = int(goods_store))
        # )
        goods.save()
    return render(request,"store/add_goods.html")
def list_goods(request):
    keywords = request.GET.get("keywords", "")
    page_num = request.GET.get("page_num", 1)
    if keywords:
        goods_list = Goods.objects.filter(goods_name__contains=keywords,goods_under=1)  # 完成了模糊查询
    else:
        goods_list = Goods.objects.filter(goods_under=1)
    paginator = Paginator(goods_list, 3)
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    return render(request, "store/goods_list.html", {"page": page, "page_range": page_range, "keywords": keywords})


def goods(request,goods_id):
    goods_data = Goods.objects.filter(id = goods_id).first()
    return render(request,"store/goods.html",locals())

def update_goods(request,goods_id):
    goods_data = Goods.objects.filter(id=goods_id).first()
    if request.method == "POST":
        goods_name = request.POST.get("goods_name")
        goods_price = request.POST.get("goods_price")
        goods_number = request.POST.get("goods_number")
        goods_description = request.POST.get("goods_description")
        goods_date = request.POST.get("goods_date")
        goods_safeDate = request.POST.get("goods_safeDate")
        goods_image = request.POST.get("goods_image")

        goods = Goods.objects.get(id = int(goods_id))
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        if goods_image:
            goods.goods_image = goods_image
        goods.save()
        return HttpResponseRedirect("/Store/goods/%s/"%goods_id)
    return render(request,"store/update_goods.html",locals())

def under_goods(request):
    id = request.GET.get("id")
    referer = request.META.get("HTTP_REFERER")
    if id:
        goods = Goods.objects.filter(id=id).first()
        goods.goods_under = 0
        goods.save()
    return HttpResponseRedirect(referer)




