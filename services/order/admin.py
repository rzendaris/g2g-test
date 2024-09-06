from django.contrib import admin

from services.order.constants import OrderStatus
from services.order.functions import granted_reward_point
from services.order.models import Product, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "currency"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "product", "total_discount", "total_amount", "currency", "status"]

    def save_model(self, request, obj, form, change):
        super(OrderAdmin, self).save_model(request, obj, form, change)
        if 'status' in form.changed_data:
            if form.cleaned_data['status'] == OrderStatus.DELIVERED:
                granted_reward_point(obj)
