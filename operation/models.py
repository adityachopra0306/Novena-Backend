from django.db import models

class Operation(models.Model):
    patient = models.ForeignKey("patient.Patient", on_delete=models.CASCADE, related_name="operations")
    doctor = models.ForeignKey("doctor.Doctor", on_delete=models.CASCADE, related_name="operations")
    date = models.DateField()
    time = models.TimeField()
    operating_room_number = models.IntegerField()

    def __str__(self):
        return f"Operation {self.id} for {self.patient.name}"
