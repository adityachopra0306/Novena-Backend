from django.db import models

class Room(models.Model):
    number = models.IntegerField(unique=True)
    room_type = models.CharField(max_length=50)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Room {self.number} ({self.room_type})"
