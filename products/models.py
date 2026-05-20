from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    image = models.ImageField(upload_to="categories/", blank=True)
    image_url = models.URLField(blank=True, help_text="Optional remote demo image URL.")
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def fallback_image(self):
        return f"images/categories/{self.slug}.svg"

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return ""


class Product(models.Model):
    name = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    description = models.TextField()
    specifications = models.TextField(blank=True, help_text="One specification per line.")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.PositiveIntegerField(default=0)
    cashback_percentage = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/", blank=True)
    image_url = models.URLField(blank=True, help_text="Optional remote demo image URL.")
    stock_quantity = models.PositiveIntegerField(default=0)
    brand = models.CharField(max_length=120, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=Decimal("4.5"))
    tags = models.CharField(max_length=250, blank=True)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})

    @property
    def discount_price(self):
        discount = self.price * Decimal(self.discount_percentage) / Decimal(100)
        return max(self.price - discount, Decimal("0.00"))

    @property
    def cashback_amount(self):
        return self.discount_price * Decimal(self.cashback_percentage) / Decimal(100)

    @property
    def in_stock(self):
        return self.stock_quantity > 0

    @property
    def spec_list(self):
        return [line.strip() for line in self.specifications.splitlines() if line.strip()]

    @property
    def fallback_image(self):
        return f"images/products/{self.slug}.svg"

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return ""


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to="products/gallery/", blank=True)
    image_url = models.URLField(blank=True, help_text="Optional remote gallery image URL.")
    alt_text = models.CharField(max_length=160, blank=True)

    def __str__(self):
        return f"{self.product.name} image"

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url


class CashbackOffer(models.Model):
    title = models.CharField(max_length=160)
    description = models.TextField()
    percentage = models.PositiveIntegerField(default=5)
    minimum_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-valid_until"]

    def __str__(self):
        return self.title
