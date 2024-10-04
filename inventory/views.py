from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from django.core.mail import send_mail
from .models import InventoryItem, InventoryChangeLog, Category
from .serializers import InventoryItemSerializer, UserSerializer, InventoryChangeLogSerializer, CategorySerializer, SupplierSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.db.models import Sum, F, FloatField
from django.contrib.auth.models import User
from .models import Supplier  # Add this line


# Inventory Item ViewSet
class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'price']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'date_added', 'quantity']

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        InventoryChangeLog.objects.create(
            inventory_item=instance,
            change_type='restocked',
            quantity_changed=instance.quantity,
            user=self.request.user
        )

    def perform_update(self, serializer):
        inventory_item = self.get_object()
        quantity_before = inventory_item.quantity
        updated_item = serializer.save()

        if quantity_before != updated_item.quantity:
            change_type = 'restock' if updated_item.quantity > quantity_before else 'sale'
            InventoryChangeLog.objects.create(
                inventory_item=updated_item,
                user=self.request.user,
                change_type=change_type,
                quantity_before=quantity_before,
                quantity_after=updated_item.quantity
            )

        if updated_item.is_low_stock():
            self.send_low_stock_alert(updated_item)

    def send_low_stock_alert(self, inventory_item):
        subject = f"Low Stock Alert: {inventory_item.name}"
        message = f"The inventory item '{inventory_item.name}' is running low on stock. Only {inventory_item.quantity} items left."
        recipient_list = [self.request.user.email]

        send_mail(
            subject,
            message,
            'noreply@yourdomain.com',
            recipient_list,
            fail_silently=False,
        )

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this item.")
        instance.delete()


# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


# Inventory Change Log ViewSet
class InventoryChangeLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InventoryChangeLog.objects.all()
    serializer_class = InventoryChangeLogSerializer
    permission_classes = [permissions.IsAuthenticated]


# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


# Pagination class for inventory change logs
class InventoryChangePagination(PageNumberPagination):
    page_size = 10


# Supplier ViewSet
class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


# Inventory Report View
class InventoryReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        total_inventory_value = InventoryItem.objects.aggregate(
            total_value=Sum(F('quantity') * F('price'), output_field=FloatField())
        )['total_value'] or 0.0

        total_items_in_stock = InventoryItem.objects.aggregate(
            total_quantity=Sum('quantity')
        )['total_quantity'] or 0

        inventory_change_history = InventoryChangeLog.objects.values(
            'inventory_item__name', 'change_type', 'quantity_changed', 'date', 'user__username'
        ).order_by('-date')

        paginator = InventoryChangePagination()
        paginated_changes = paginator.paginate_queryset(inventory_change_history, request)

        report_data = {
            'total_inventory_value': total_inventory_value,
            'total_items_in_stock': total_items_in_stock,
            'inventory_change_history': paginated_changes
        }

        return paginator.get_paginated_response(report_data)


    from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to the Inventory Management API!</h1>")

