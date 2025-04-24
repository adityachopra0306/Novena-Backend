from django.db import models

class Nurse(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.TextField()
    work_shift = models.CharField(max_length=50)
    experience = models.IntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
