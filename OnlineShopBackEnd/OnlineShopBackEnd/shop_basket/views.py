from django.shortcuts import render

from OnlineShopBackEnd.shop_basket.models import Basket, BasketItem


def basket_view(request):
    basket = Basket.objects.get(user=request.user)
    basket_items = basket.basketitem_set.all()
    context = {
        'basket_items': basket_items,
        'basket': basket
    }
    return render(request, 'basket.html', context)
