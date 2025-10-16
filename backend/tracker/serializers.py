# backend/tracker/serializers.py
# This converts model instances ↔ JSON for API input/output. 

from rest_framework import serializers
from .models import User, Property, MaintenanceIssue, RepairJob, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone', 'address']


class PropertySerializer(serializers.ModelSerializer):
    landlord = UserSerializer(read_only=True)

    class Meta:
        model = Property
        fields = '__all__'


class MaintenanceIssueSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)
    reported_by = UserSerializer(read_only=True)

    class Meta:
        model = MaintenanceIssue
        fields = '__all__'


class RepairJobSerializer(serializers.ModelSerializer):
    issue = MaintenanceIssueSerializer(read_only=True)
    handyman = UserSerializer(read_only=True)

    class Meta:
        model = RepairJob
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
