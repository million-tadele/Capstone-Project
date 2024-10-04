from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryItemViewSet, UserViewSet, InventoryChangeLogViewSet, CategoryViewSet, SupplierViewSet

router = DefaultRouter()
router.register(r'inventory-items', InventoryItemViewSet)
router.register(r'users', UserViewSet)
router.register(r'inventory-change-logs', InventoryChangeLogViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'suppliers', SupplierViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
