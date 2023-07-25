from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from djangoql.admin import DjangoQLSearchMixin
from import_export import resources
from import_export.admin import ImportExportMixin

from .models import Category, Product, Customer, Order
from .tuples import ORDER_STATUSES


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'is_active', 'id',)


admin.site.register(Category, CategoryAdmin)


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('name', 'slug', 'is_active', 'id',)


class ProductAdmin(ImportExportMixin, DjangoQLSearchMixin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'is_active', 'id',)
    filter_horizontal = ('category',)
    search_fields = ('name',)
    list_filter = ('category', 'is_active',)
    resource_classes = (ProductResource,)
    ordering = ('name',)


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
    list_display = (
        'id',
        'created_dt',
        'completed_dt',
        'status',
        'link_to_customer',
    )
    list_filter = ('status', OnlyActiveOrdersFilter,)
    list_display_links = ('id', 'created_dt',)
    list_select_related = ('customer',)

    def link_to_customer(self, obj):
        link = reverse("admin:myapp_customer_change", args=[obj.customer.id])
        return format_html(
            '<a href="{}">{}</a>',
            link,
            obj.customer,
        )

    link_to_customer.short_description = 'Customer'


admin.site.register(Order, OrderAdmin)
