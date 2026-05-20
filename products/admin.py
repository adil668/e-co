from django.contrib import admin
from django.utils.html import format_html

from .models import CashbackOffer, Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_featured", "product_count")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

    def product_count(self, obj):
        return obj.products.count()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "preview",
        "name",
        "brand",
        "category",
        "price",
        "discount_percentage",
        "stock_quantity",
        "is_featured",
        "is_trending",
    )
    list_filter = ("category", "brand", "is_featured", "is_trending")
    search_fields = ("name", "brand", "tags")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:46px;border-radius:8px;" />', obj.image.url)
        if obj.image_url:
            return format_html('<img src="{}" style="height:46px;border-radius:8px;" />', obj.image_url)
        return "No image"


@admin.register(CashbackOffer)
class CashbackOfferAdmin(admin.ModelAdmin):
    list_display = ("title", "percentage", "minimum_order_value", "valid_until", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title",)
