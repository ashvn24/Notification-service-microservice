from rest_framework import serializers
from .models import Notification

class notificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'