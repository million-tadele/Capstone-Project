from django.db import models
from django.contrib.auth.models import User

class InventoryItem(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('groceries', 'Groceries'),
        ('clothing', 'Clothing'),
        ('furniture', 'Furniture'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class InventoryChangeLog(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity_change = models.IntegerField()  # Positive for additions, negative for subtractions
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    change_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} ({self.quantity_change})"

    class Meta:
        indexes = [
            models.Index(fields=['change_date']),
            models.Index(fields=['changed_by']),
        ]
