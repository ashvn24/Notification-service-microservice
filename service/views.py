from django.shortcuts import render
from rest_framework import generics
from .models import Notification
from .serializer import notificationSerializer
# Create your views here.

class getNotificationAPIView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = notificationSerializer
