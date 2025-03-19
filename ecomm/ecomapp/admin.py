from django.contrib import admin
from ecomapp.models import Category,Product
# Register your models here.
# admin.site.register(Category)
# admin.site.register(Product)

class CategoryAdmin(admin.ModelAdmin):
    list_display=['name']
admin.site.register(Category,CategoryAdmin)   

class ProductAdmin(admin.ModelAdmin):
    list_display=['name','price','category','is_active']
    list_filter=['category','is_active']
admin.site.register(Product,ProductAdmin)          