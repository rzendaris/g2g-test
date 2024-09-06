from django.contrib import admin

from services.user.models import Customer, CustomerPoint, CustomerPointRedemptionHistory


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "email"]


@admin.register(CustomerPoint)
class CustomerPointAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "granted_point", "used_point", "expired_at"]


@admin.register(CustomerPointRedemptionHistory)
class CustomerPointRedemptionHistoryAdmin(admin.ModelAdmin):
    list_display = ["id", "customer_point_id", "used_point", "reference_name", "reference_id", "created_at"]
