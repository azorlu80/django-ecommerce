from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from carts.models import Cart, CartItem
from store.models import Product


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass #ignore
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items
    }
    return render(request, 'store/cart.html', context)


def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)  # get added product

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # get the cart using ht cart_id present in the session
        #database de cart varsa getir yoksa yeni cart oluştur.
    except ObjectDoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    try:
         cart_item = CartItem.objects.get(product=product, cart=cart)
         cart_item.quantity += 1  #added 1 quantity
         cart_item.save()
    except ObjectDoesNotExist:
         cart_item = CartItem.objects.create(
             product=product,
             quantity=1,
             cart=cart,

         )
    cart_item.save()

    return redirect('cart')
