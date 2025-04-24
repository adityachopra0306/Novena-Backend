from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Patient, Appointment
from doctor.models import Doctor

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone = data.get("phoneNumber")

            if not phone:
                return JsonResponse({"message": "Phone number is required!"}, status=400)

            user = get_object_or_404(Patient, mob=phone)

            return JsonResponse({
                "message": "Login successful!",
                "user_id": user.id,
                "patient_name": user.name,
                "phone": user.mob
            }, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON format!"}, status=400)

    return JsonResponse({"message": "Invalid request method!"}, status=405)

def profile_view(request, user_id):
    if request.method == 'GET':
        try:
            patient = get_object_or_404(Patient, id=user_id)

            return JsonResponse({
                "name": patient.name,
                "age": patient.age,
                "sex": patient.sex,
                "dob": patient.dob.strftime("%Y-%m-%d"),
                "address": patient.address,
                "mob": patient.mob,
            }, status=200)

        except Patient.DoesNotExist:
            return JsonResponse({"message": "Patient not found!"}, status=404)

    return JsonResponse({"message": "Invalid request method!"}, status=405)

@csrf_exempt
def fetch_appointments_view(request, user_id):
    if request.method == 'GET':
        try:
            patient = get_object_or_404(Patient, id=user_id)
            appointments = patient.appointments.select_related('doctor').all()

            data = [
                {
                    "appointment_id": appointment.id,
                    "doctor_name": appointment.doctor.name,
                    "date": appointment.date.strftime("%Y-%m-%d"),
                    "time": appointment.time.strftime("%H:%M:%S"),
                }
                for appointment in appointments
            ]

            return JsonResponse(data, safe=False, status=200)

        except Patient.DoesNotExist:
            return JsonResponse({"message": "Patient not found!"}, status=404)

    return JsonResponse({"message": "Invalid request method!"}, status=405)


@csrf_exempt
def book_appointment_view(request):
    """
    Book a new appointment for a patient.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            patient_id = data.get("patientId")
            doctor_id = data.get("doctorId")
            date = data.get("date")
            time = data.get("time")

            if not all([patient_id, doctor_id, date, time]):
                return JsonResponse({"message": "All fields are required!"}, status=400)

            patient = get_object_or_404(Patient, id=patient_id)
            doctor = get_object_or_404(Doctor, id=doctor_id)

            # Create new appointment
            Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                date=date,
                time=time
            )

            return JsonResponse({"message": "Appointment booked successfully!"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON format!"}, status=400)

        except Patient.DoesNotExist:
            return JsonResponse({"message": "Patient not found!"}, status=404)

        except Doctor.DoesNotExist:
            return JsonResponse({"message": "Doctor not found!"}, status=404)

    return JsonResponse({"message": "Invalid request method!"}, status=405)


def filter_appointments_view(request, user_id):
    if request.method == 'GET':
        try:
            date = request.GET.get("date") 
            doctor_name = request.GET.get("doctorName") 

            patient = get_object_or_404(Patient, id=user_id)
            appointments = patient.appointments.select_related('doctor').all()

            if date:
                appointments = appointments.filter(date=date)
            if doctor_name:
                appointments = appointments.filter(doctor__name__icontains=doctor_name)


            data = [
                {
                    "appointment_id": appointment.id,
                    "doctor_name": appointment.doctor.name,
                    "date": appointment.date.strftime("%Y-%m-%d"),
                    "time": appointment.time.strftime("%H:%M:%S"),
                }
                for appointment in appointments
            ]

            return JsonResponse(data, safe=False, status=200)

        except Patient.DoesNotExist:
            return JsonResponse({"message": "Patient not found!"}, status=404)

    return JsonResponse({"message": "Invalid request method!"}, status=405)