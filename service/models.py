from django.db import models

# Create your models here.

class Notification(models.Model):
    content = models.CharField(max_length = 200)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=100)
    user = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.type