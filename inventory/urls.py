from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryItemViewSet, InventoryChangeLogViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('items', InventoryItemViewSet)
router.register('logs', InventoryChangeLogViewSet)

# The main urlpatterns that include the router URLs and JWT authentication URLs
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),  # Include the router's URLs here
]
