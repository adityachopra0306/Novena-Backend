from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    treatment = models.TextField()

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey("Department", on_delete=models.CASCADE, related_name="doctors")
    age = models.IntegerField()
    address = models.TextField()
    designation = models.CharField(max_length=50)
    doc_type = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name