from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url(r'^market/', views.market, name='market'),
    url(r'^marketwithparams/(?P<typeid>\d+)/(?P<childcid>\d+)/(?P<order_rule>\d+)/', views.market_with_params, name='market_with_params'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^mine/', views.mine, name='mine'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^checkuser/', views.check_user, name='check_user'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^activate/', views.activate, name='activate'),
    url(r'^addtocart/', views.addtocart, name='addtocart'),

    url(r'^subfromcart/', views.subfromcart, name='subfromcart'),
    url(r'^changecartstate/', views.change_cart_state, name='change_cart_state'),

    url(r'^subshoppingcart/', views.sub_shoppingcart, name='sub_shoppingcart'),
    url(r'^addshoppingcart/', views.add_shoppingcart, name='add_shoppingcart'),
    url(r'^selectall/', views.select_all, name='select_all'),
    url(r'^createorder/', views.create_order, name='create_order'),
    url(r'^orderdetail/', views.order_detail, name='order_detail'),
    url(r'^orderlistnotpaid/', views.order_list_not_paid, name='order_list_not_paid'),

    url(r'^paid/', views.paid, name='paid'),
]