from django.db import models

class Accountant(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    working_time = models.CharField(max_length=50)
    address = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    mobile = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name

class Bill(models.Model):
    purpose = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Bill: {self.purpose}"

class Payment(models.Model):
    type = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self):
        return f"Payment: {self.type} on {self.date}"
