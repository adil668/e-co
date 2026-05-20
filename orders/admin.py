from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price", "cashback")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "full_name", "subtotal", "cashback_earned", "payment_method", "status", "created_at")
    list_filter = ("status", "payment_method", "created_at")
    search_fields = ("id", "user__username", "full_name", "email", "phone")
    inlines = [OrderItemInline]
