from django.db import models

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    manufacture_date = models.DateField()
    expiry_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Prescription(models.Model):
    patient = models.ForeignKey("patient.Patient", on_delete=models.CASCADE, related_name="prescriptions")
    doctor = models.ForeignKey("doctor.Doctor", on_delete=models.CASCADE, related_name="prescriptions")
    date = models.DateField()
    time = models.TimeField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    serial_number = models.IntegerField()

    def __str__(self):
        return f"Prescription {self.serial_number} for {self.patient.name}"

class PrescribedMedicines(models.Model):
    prescription = models.ForeignKey("Prescription", on_delete=models.CASCADE, related_name="medicines")
    medicine = models.ForeignKey("Medicine", on_delete=models.CASCADE, related_name="prescriptions")

    class Meta:
        unique_together = ('prescription', 'medicine')

    def __str__(self):
        return f"{self.medicine.name} for Prescription {self.prescription.serial_number}"
