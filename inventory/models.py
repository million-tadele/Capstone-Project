from django.db import models
from django.contrib.auth.models import User

# Category model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Supplier model
class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Inventory Item model
class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="inventory_items")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name="inventory_items")
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    low_stock_threshold = models.IntegerField(default=10)

    def __str__(self):
        return self.name

    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold

# Inventory Change Log model
class InventoryChangeLog(models.Model):
    CHANGE_TYPES = (
        ('restocked', 'Restocked'),
        ('sold', 'Sold'),
    )

    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    change_type = models.CharField(max_length=10, choices=CHANGE_TYPES)
    quantity_changed = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.inventory_item.name} - {self.change_type} - {self.quantity_changed}"

