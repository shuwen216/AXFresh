from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from App.models import AXFUser

REQUIRE_LOGIN_JSON = [
    '/axf/addtocart/',
    '/axf/subfromcart/',
    '/axf/changecartstate/',
    '/axf/createorder/',
]

REQUIRE_LOGIN = [
    '/axf/cart/',
    '/axf/orderdetail/',
    '/axf/orderlistnotpaid/',
]

class LoginMiddleware(MiddlewareMixin):

    def process_request(self, request):

        if request.path in REQUIRE_LOGIN_JSON:

            user_id = request.session.get('user_id')

            if user_id:
                try:
                    user = AXFUser.objects.get(pk=user_id)
                    request.user = user # save this info for next
                except:
                    data = {
                        'status': 302,
                        'msg': 'user not available',
                    }
                    return JsonResponse(data=data)
            else:
                data = {
                    'status': 302,
                    'msg': 'user not logged in'
                }
                return JsonResponse(data=data)

        if request.path in REQUIRE_LOGIN:

            user_id = request.session.get('user_id')

            if user_id:
                try:
                    user = AXFUser.objects.get(pk=user_id)
                    request.user = user  # save this info for next
                except:
                    return redirect(reverse('axf:login'))
            else:
                return redirect(reverse('axf:login'))
