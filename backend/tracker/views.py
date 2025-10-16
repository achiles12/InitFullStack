# backend/tracker/views.py
# Define how API endpoints behave (CRUD + auth).

from rest_framework import viewsets, permissions
from .models import User, Property, MaintenanceIssue, RepairJob, Message
from .serializers import (
    UserSerializer,
    PropertySerializer,
    MaintenanceIssueSerializer,
    RepairJobSerializer,
    MessageSerializer,
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    #permission_classes = [permissions.AllowAny
    permission_classes = [permissions.IsAuthenticated]  # ✅ requires login


class MaintenanceIssueViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceIssue.objects.all()
    serializer_class = MaintenanceIssueSerializer
    permission_classes = [permissions.AllowAny]


class RepairJobViewSet(viewsets.ModelViewSet):
    queryset = RepairJob.objects.all()
    serializer_class = RepairJobSerializer
    permission_classes = [permissions.AllowAny]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.AllowAny]

