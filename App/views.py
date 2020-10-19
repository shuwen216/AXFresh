import uuid

from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

from AXF.settings import MEDIA_KEY_PREFIX, STATIC_URL
from App.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, AXFUser, Cart, Order, \
    OrderGoods
from App.utils import hash_str, send_email_activate, get_total_price
from App.views_constants import ALL_TYPES, ORDER_OVERALL, ORDER_PRICE_L2H, ORDER_PRICE_H2L, ORDER_SALE_L2H, \
    ORDER_SALE_H2L, HTTP_USER_EXIST, HTTP_OK, HTTP_EMAIL_EXIST, ORDER_STATUS_UNPAID, ORDER_STATUS_UNDELIVERED, \
    ORDER_STATUS_UNSHIPPED


def home(request):
    main_wheels = MainWheel.objects.all()
    main_navs = MainNav.objects.all()
    main_mustbuys = MainMustBuy.objects.all()
    main_shops = MainShop.objects.all()
    main_shop0_1 = main_shops[0:1]
    main_shop1_3 = main_shops[1:3]
    main_shop3_7 = main_shops[3:7]
    main_shop7_11 = main_shops[7:11]
    main_shows = MainShow.objects.all()
    data = {
        "title": "Home",
        "main_wheels": main_wheels,
        "main_navs": main_navs,
        "main_mustbuys": main_mustbuys,
        "main_shop0_1": main_shop0_1,
        "main_shop1_3": main_shop1_3,
        "main_shop3_7": main_shop3_7,
        "main_shop7_11": main_shop7_11,
        "main_shows": main_shows,
    }
    return render(request, 'main/home.html', context=data)


def market(request):
    return redirect(reverse('axf:market_with_params', kwargs= {
        "typeid": 104749,
        "childcid": 0,
        'order_rule': 0,
    }))

def market_with_params(request, typeid, childcid, order_rule):
    """
    Input: sql: all_catogories:0#imported fruits:103534#domestic fruits:103533]]
    Output: list: [[all_catogories, 0], [imported fruits, 103534], [domestic fruits, 103533]]
    """
    foodtypes = FoodType.objects.all()
    goods_list = Goods.objects.filter(categoryid=typeid)

    if childcid == ALL_TYPES:
        pass
    else:
        goods_list = goods_list.filter(childcid=childcid)

    foodtypechildnames = foodtypes.get(typeid=typeid).childtypenames
    foodtypechildnames_list = foodtypechildnames.split("#")
    foodtype_childname_list = []

    for name in foodtypechildnames_list:
        foodtype_childname_list.append(name.split(":"))


    # ORDER RULE FROM FRONT_end output: list sent
    if order_rule == ORDER_OVERALL:
        pass
    elif order_rule == ORDER_PRICE_L2H:
        goods_list = goods_list.order_by("price")
    elif order_rule == ORDER_PRICE_H2L:
        goods_list = goods_list.order_by("-price")
    elif order_rule == ORDER_SALE_L2H:
        goods_list = goods_list.order_by("productnum")
    elif order_rule == ORDER_SALE_H2L:
        goods_list = goods_list.order_by("-productnum")

    order_rule_list = [
        ['Best Match', ORDER_OVERALL],
        ['Price low to high', ORDER_PRICE_L2H],
        ['Price high to low', ORDER_PRICE_H2L],
        ['Sales low to high', ORDER_SALE_L2H],
        ['Sales high to low', ORDER_SALE_H2L],
    ]

    data = {
        "title": "Flash Sale",
        "foodtypes": foodtypes,
        "goods_list": goods_list,
        "typeid_from_views": int(typeid),
        "foodtype_childname_list": foodtype_childname_list,
        "childcid_from_views": childcid,
        "order_rule_list": order_rule_list,
        "order_rule_from_views": order_rule,
    }

    return render(request, 'main/market.html', context=data)


def cart(request):
    # already passed loginmiddleware
    carts = Cart.objects.filter(c_user=request.user)
    is_select_all = not carts.filter(c_is_selected=False).exists()
    data = {
        'title': 'Cart',
        'carts': carts,
        'is_select_all': is_select_all,
        'total_price': get_total_price(),
    }

    return render(request, 'main/cart.html', context=data)


def mine(request):

    user_id = request.session.get('user_id')

    data = {
        'title': 'My Account',
        'is_login': False
    }

    if user_id:
        user = AXFUser.objects.get(pk=user_id)
        data['is_login'] = True
        data['username'] = user.u_username
        if user.u_icon:
            data['usericon'] = MEDIA_KEY_PREFIX + user.u_icon.url
        else:
            data['usericon'] = STATIC_URL + 'img/cart.png'
        data['order_not_paid'] = Order.objects.filter(o_user=user_id).filter(o_status=ORDER_STATUS_UNPAID).count()
        data['order_not_received'] = Order.objects.filter(o_user=user_id).filter(o_status__in=[ORDER_STATUS_UNDELIVERED,ORDER_STATUS_UNSHIPPED]).count()
    return render(request, 'main/mine.html', context=data)


def register(request):
    if request.method == "GET":
        data = {
            "title": "User Registration",
        }
        return render(request, 'user/user_register.html', context=data )
    elif request.method == "POST":
        username = request.POST.get("username") # name attribute in user_register.html
        email = request.POST.get("email")
        password = request.POST.get("password")
        icon = request.FILES.get("icon")

        #password = hash_str(password)
        password = make_password(password) #add time point
        #check_password('user input', 'encoded') return true false as comparison result

        user = AXFUser()
        user.u_username = username
        user.u_email = email
        user.u_password = password
        user.u_icon = icon

        user.save()

        u_token = uuid.uuid4().hex

        cache.set(u_token, user.id, timeout=60*60*24)

        send_email_activate(username, email, u_token)

        return redirect(reverse('axf:login'))

def login(request):
    if request.method == "GET":
        err_msg = request.session.get('error_message')
        data = {
            "title": "Login",
        }
        if err_msg:
            del request.session['error_message'] #next time refresh the page, the err should be gone.
            data['error_message'] = err_msg

        return render(request, 'user/user_login.html', context=data)

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        users = AXFUser.objects.filter(u_username=username)
        if users.exists():
            user = users.first()
            if check_password(password, user.u_password):
                if user.is_active:
                    request.session['user_id'] = user.id

                    return redirect(reverse('axf:mine'))
                else:
                    print('user not activated')
                    request.session['error_message'] = 'not activated'
                    return redirect(reverse('axf:login'))
            else:
                request.session['error_message'] = 'incorrect password'
                return redirect(reverse('axf:login'))
        # username or password is incorrect
        request.session['error_message'] = 'user does not exist'
        return redirect(reverse('axf:login'))


def check_user(request):
    # use GET method because getJASON(url,,)
    username = request.GET.get("name")
    email = request.GET.get("email")
    users = AXFUser.objects.filter(u_username=username)
    emails = AXFUser.objects.filter(u_email=email)
    data = {
        "status": HTTP_OK,
        "msg": 'username available to use'
    }
    if users.exists():
        data["status"] = HTTP_USER_EXIST
        data["msg"] = 'username already exists'
    elif emails.exists():
        data["status"] = HTTP_EMAIL_EXIST
        data["msg"] = 'email address already taken'
    return JsonResponse(data=data)


def logout(request):
    request.session.flush()
    return redirect(reverse('axf:mine'))


def activate(request):
    u_token = request.GET.get('u_token')
    user_id = cache.get(u_token)
    if user_id:
        cache.delete(u_token)
        user = AXFUser.objects.get(pk=user_id)
        user.is_active = True
        user.save()
        return redirect(reverse('axf:login'))
    return render(request, 'user/activate_fail.html')


def addtocart(request):
    # from market.js
    goodsid = request.GET.get('goodsid')

    # AOP middleware
    # request.user saved in 'LoginMiddleware'
    carts = Cart.objects.filter(c_user=request.user).filter(c_goods_id=goodsid)
    if carts.exists():
        cart_obj = carts.first()
        cart_obj.c_goods_num = cart_obj.c_goods_num + 1
    else:
        cart_obj = Cart()
        cart_obj.c_user = request.user
        cart_obj.c_goods_id = goodsid

    cart_obj.save()

    data = {
        'status': 200,
        'msg': 'updated cart',
        'c_goods_num': cart_obj.c_goods_num,
    }
    return JsonResponse(data=data)


def subfromcart(request):
    # from market.js
    goodsid = request.GET.get('goodsid')

    # AOP middleware
    # request.user saved in 'LoginMiddleware'
    carts = Cart.objects.filter(c_user=request.user).filter(c_goods_id=goodsid)
    if carts.exists():
        cart_obj = carts.first()
        if cart_obj.c_goods_num == 0 or cart_obj.c_goods_num == 1:
            goods_num = 0
            cart_obj.delete()
        else:
            cart_obj.c_goods_num = cart_obj.c_goods_num - 1
            goods_num = cart_obj.c_goods_num
            cart_obj.save()
        data = {
            'status': 200,
            'msg': 'updated cart',
            'c_goods_num': goods_num,
        }
    else:
        pass
        #cart_obj = Cart()
        #cart_obj.c_user = request.user
        #cart_obj.c_goods_id = goodsid
        data = {
            'status': 201,
            'msg': 'cannot sub such item in cart',
        }

    return JsonResponse(data=data)


def change_cart_state(request):
    cart_id = request.GET.get('cartid')
    cart_obj = Cart.objects.get(pk=cart_id)

    cart_obj.c_is_selected = not cart_obj.c_is_selected

    cart_obj.save()

    is_select_all = not Cart.objects.filter(c_user=request.user).filter(c_is_selected=False).exists()

    data = {
        'status': 200,
        'msg': 'change ok',
        'c_is_selected': cart_obj.c_is_selected,
        'is_select_all': is_select_all,
        'total_price': get_total_price(),
    }

    return JsonResponse(data=data)


def sub_shoppingcart(request):

    cartid = request.GET.get('cartid')
    cart_obj = Cart.objects.get(pk=cartid)
    data = {
        'status': 200,
        'msg': 'ok',
    }
    if cart_obj.c_goods_num > 1:
        cart_obj.c_goods_num = cart_obj.c_goods_num - 1
        cart_obj.save()
        data['c_goods_num'] = cart_obj.c_goods_num
    else:
        cart_obj.delete()
        data['c_goods_num'] = 0

    data['total_price'] = get_total_price()
    return JsonResponse(data=data)


def add_shoppingcart(request):
    cartid = request.GET.get('cartid')
    cart_obj = Cart.objects.get(pk=cartid)
    data = {
        'status': 200,
        'msg': 'ok',
    }

    cart_obj.c_goods_num = cart_obj.c_goods_num + 1
    cart_obj.save()
    data['c_goods_num'] = cart_obj.c_goods_num
    data['total_price'] = get_total_price()
    return JsonResponse(data=data)


def select_all(request):
    cart_list = request.GET.get("cart_list")

    cart_list = cart_list.split("#")
    carts = Cart.objects.filter(id__in=cart_list)
    #print(carts)

    for cart_obj in carts:
        cart_obj.c_is_selected = not cart_obj.c_is_selected
        cart_obj.save()

    data = {
        'status':200,
        'msg': 'ok',
        'total_price': get_total_price(),
    }
    return JsonResponse(data=data)


def create_order(request):

    carts = Cart.objects.filter(c_user=request.user).filter(c_is_selected=True)

    order = Order()
    order.o_user = request.user
    order.o_price = get_total_price() # get it again at backend
    order.save()
    # create order from selected in cart
    for cart_obj in carts:
        ordergoods = OrderGoods()
        ordergoods.o_order = order
        ordergoods.o_goods_num = cart_obj.c_goods_num
        ordergoods.o_goods = cart_obj.c_goods
        ordergoods.save()
        cart_obj.delete()  # removed cart obj

    data = {
        'status': 200,
        'msg': 'ok',
        'order_id': order.id,
    }
    return JsonResponse(data=data)


def order_detail(request):

    order_id = request.GET.get('orderid')
    order = Order.objects.get(pk=order_id)

    data = {
        'title': 'Order Details',
        'order': order,
    }

    return render(request, 'order/order_detail.html', context=data)


def order_list_not_paid(request):
    # require login to get request user
    orders = Order.objects.filter(o_user=request.user).filter(o_status=ORDER_STATUS_UNPAID)
    data = {
        'title': 'order list',
        'orders': orders,
    }

    return render(request, 'order/order_list_not_paid.html', context=data)


def paid(request):

    order_id = request.GET.get("orderid")
    order = Order.objects.get(pk=order_id)
    order.o_status = ORDER_STATUS_UNSHIPPED
    order.save()

    data = {
        "status": 200,
        "msg": "paid successfully",
    }
    return JsonResponse(data=data)