from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    sex = models.CharField(max_length=1)
    dob = models.DateField()
    address = models.TextField()
    mob = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey("doctor.Doctor", on_delete=models.CASCADE, related_name="appointments")
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"Appointment: {self.patient.name} with {self.doctor.name}"

class Admission(models.Model):
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE, related_name="admissions")
    room = models.ForeignKey("room.Room", on_delete=models.CASCADE, related_name="admissions")
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"Admission: {self.patient.name} in Room {self.room.number}"
