from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import InventoryItem, InventoryChangeLog
from .serializers import InventoryItemSerializer, InventoryChangeLogSerializer

class LowStockFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        threshold = request.query_params.get('low_stock', None)
        if threshold:
            return queryset.filter(quantity__lte=int(threshold))
        return queryset

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, LowStockFilter]
    ordering_fields = ['name', 'quantity', 'price', 'date_added']
    ordering = ['date_added']  # Default ordering

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()
        quantity_change = instance.quantity - InventoryItem.objects.get(pk=instance.pk).quantity
        # Log the change
        InventoryChangeLog.objects.create(
            item=instance,
            quantity_change=quantity_change,
            changed_by=self.request.user
        )

class InventoryChangeLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InventoryChangeLog.objects.all()
    serializer_class = InventoryChangeLogSerializer
    permission_classes = [IsAuthenticated]
