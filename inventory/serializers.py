from rest_framework import serializers
from .models import InventoryItem, InventoryChangeLog

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ['id', 'name', 'description', 'quantity', 'price', 'category', 'date_added', 'last_updated', 'user']

class InventoryChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryChangeLog
        fields = ['item', 'quantity_change', 'changed_by', 'change_date']
