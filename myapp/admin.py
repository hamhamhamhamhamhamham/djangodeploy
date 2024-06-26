from django.contrib import admin
from .models import Product
# Register your models here.


# admin.site.register(Product)
admin.site.site_title="Admin"
admin.site.site_header="Hamidreza Ecommerce"
admin.site.index_title="Titles"


# Product Model  in admin panel
class ProductAdmin(admin.ModelAdmin):
    # show x fields  
    list_display = ("name","price","desc","seller_name","create_date")
    # search by field x
    # ***tuple ("",)***
    search_fields =("desc",)

    # custom actions
    # ***tuple ("",)***
    actions=("set_price_ZERO","set_desc_xxx",)
    def set_price_ZERO(self,request, queryset):
        queryset.update(price=0)
    def set_desc_xxx(self,req,qset):
        qset.update(desc="XXX")
     # easily set values
     # ***tuple ("",)***
    list_editable=("name","desc",)
    list_display_links = ["create_date"]
    # view site
    admin.site.site_url = "/myapp/products"

#first add Product to Admin
#second : appearance
admin.site.register(Product,ProductAdmin)    