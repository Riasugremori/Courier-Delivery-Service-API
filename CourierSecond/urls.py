from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, ParcelViewSet, DeliveryProofViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'parcels', ParcelViewSet)
router.register(r'delivery-proofs', DeliveryProofViewSet)

urlpatterns = [
    path('', include(router.urls)),  
]
