from django.contrib import admin
from .models import Category, Product, Customer, Order
from .tuples import ORDER_STATUSES


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'is_active', 'id',)


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'is_active', 'id',)
    filter_horizontal = ('category',)
    search_fields = ('name',)
    list_filter = ('category', 'is_active',)


admin.site.register(Product, ProductAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'id',)


admin.site.register(Customer, CustomerAdmin)


class OnlyActiveOrdersFilter(admin.SimpleListFilter):
    title = 'Show Only Active Orders'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('active', 'Active'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(status__in=(ORDER_STATUSES.new, ORDER_STATUSES.processing, ORDER_STATUSES.shipped))
        return queryset


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_dt', 'completed_dt', 'status', 'id',)
    list_filter = ('status', OnlyActiveOrdersFilter,)


admin.site.register(Order, OrderAdmin)
