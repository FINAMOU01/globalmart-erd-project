from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()


class Cart(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart({self.user.username})"

    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())

    def get_item_count(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart     = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product  = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_subtotal(self):
        return self.product.price * self.quantity


class Order(models.Model):

    class Status(models.TextChoices):
        PENDING    = "PENDING",    "Pending"
        CONFIRMED  = "CONFIRMED",  "Confirmed"
        PROCESSING = "PROCESSING", "Processing"
        SHIPPED    = "SHIPPED",    "Shipped"
        DELIVERED  = "DELIVERED",  "Delivered"
        CANCELLED  = "CANCELLED",  "Cancelled"

    customer         = models.ForeignKey(User, on_delete=models.SET_NULL,
                                         null=True, related_name="orders")
    created_at       = models.DateTimeField(default=timezone.now)
    updated_at       = models.DateTimeField(auto_now=True)
    status           = models.CharField(max_length=20,
                                        choices=Status.choices,
                                        default=Status.PENDING)
    total            = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_address = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} - {self.customer} [{self.status}]"

    def calculate_total(self):
        self.total = sum(item.get_subtotal() for item in self.order_items.all())
        self.save(update_fields=["total"])

    def is_cancellable(self):
        return self.status in (self.Status.PENDING, self.Status.CONFIRMED)


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product  = models.ForeignKey(Product, on_delete=models.SET_NULL,
                                 null=True, related_name="order_items")
    quantity = models.PositiveIntegerField()
    price    = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product} @ {self.price}"

    def get_subtotal(self):
        return self.price * self.quantity