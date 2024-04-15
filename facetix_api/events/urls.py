"""Events urls."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from facetix_api.events import views

router = DefaultRouter()
router.register(r'events', views.EventViewSet, basename='event')
router.register(r'media-file-event', views.EventMediaViewSet, basename='media-file-event')
router.register(r'buy-ticket-event', views.BuyEventTicketViewSet, basename='buy-ticket-event')

urlpatterns = [
    path('', include(router.urls)),
]