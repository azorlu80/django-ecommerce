from django.contrib import admin

# Register your models here.
from carts.models import Cart, CartItem

admin.site.register(Cart)
admin.site.register(CartItem)