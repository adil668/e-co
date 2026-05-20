from decimal import Decimal

from django.conf import settings
from django.db import models

from products.models import Product


class Order(models.Model):
    PAYMENT_CHOICES = [
        ("card", "Credit/Debit Card"),
        ("upi", "UPI"),
        ("cod", "Cash on Delivery"),
    ]
    STATUS_CHOICES = [
        ("placed", "Placed"),
        ("packed", "Packed"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    full_name = models.CharField(max_length=160)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=12)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default="cod")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="placed")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cashback_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

    @property
    def delivery_fee(self):
        return Decimal("0.00") if self.subtotal >= Decimal("999.00") else Decimal("49.00")

    @property
    def total(self):
        return self.subtotal + self.delivery_fee


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cashback = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def line_total(self):
        return self.price * self.quantity
