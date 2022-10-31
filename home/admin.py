from django.contrib import admin
from .models import Product,Cart,Address,PlacedOrder ,Customer

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('id','title','brand','discounted_price','actual_price','category','gender_category','product_image')
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=('id','user','product','quantity')
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user','name','house_no','street','locality','city','zip_code','state')
@admin.register(PlacedOrder)
class PlacedOrderAdmin(admin.ModelAdmin):
    list_display = ('user','address','product','quantity','order_date','status')    
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user','phone','created')    