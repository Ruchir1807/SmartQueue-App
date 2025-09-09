from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Token(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    token_number = models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=[
        ('waiting', 'Waiting'),
        ('served', 'Served'),
        ('cancelled', 'Cancelled'),
    ], default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.token_number} - {self.status}"

