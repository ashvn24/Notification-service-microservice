from django.urls import path
from .views import getNotificationAPIView

urlpatterns = [
    path('get/', getNotificationAPIView.as_view()),
]
