from OnlineShopBackEnd.orders.models import DiscountCode
from OnlineShopBackEnd.shop_basket.models import Basket


def update_basket_discounted_price(basket_pk):
    basket = Basket.objects.filter(pk=basket_pk).get()
    if not basket.discount_code:
        return

    try:
        code_from_basket = basket.discount_code
        code_object = DiscountCode.objects.get(code=code_from_basket)
    except DiscountCode.DoesNotExist:
        pass

    discount_percentage = int(code_object.discount)
    basket_cost = sum(((item.product.product_price * item.quantity) for item in basket.basketitem_set.all()))
    discounted_cost = basket_cost - (basket_cost * (discount_percentage / 100))
    basket.discounted_price = discounted_cost
    basket.save()
    return basket.discounted_price

