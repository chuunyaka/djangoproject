from django.db import models
from datetime import datetime

class Appointment(models.Model):
    date = models.DateField(
        default=datetime.utcnow,
    )
    client_name = models.CharField(
        max_length=50
    )
    message = models.TextField()

    def __str__(self):
        return f'{self.client_name}: {self.message}'