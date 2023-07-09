from django.contrib import admin
from .models import Category, Product, Customer, Order


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'is_active', 'id',)


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'is_active', 'id',)


admin.site.register(Product, ProductAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'id',)


admin.site.register(Customer, CustomerAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_dt', 'completed_dt', 'status', 'id',)


admin.site.register(Order, OrderAdmin)
