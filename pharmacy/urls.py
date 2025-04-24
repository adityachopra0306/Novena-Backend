from django.urls import path
from . import views

urlpatterns = [
    path('api/prescription/<int:patient_id>/', views.get_prescriptions),
    path('api/prescription/details/<int:prescription_id>/', views.get_prescription_details),
]
