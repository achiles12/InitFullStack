# backend/tracker/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    PropertyViewSet,
    MaintenanceIssueViewSet,
    RepairJobViewSet,
    MessageViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'properties', PropertyViewSet)
router.register(r'issues', MaintenanceIssueViewSet)
router.register(r'repairs', RepairJobViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
