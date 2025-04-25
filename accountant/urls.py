from django.urls import path
from . import views

urlpatterns = [
    path('api/admission/get-patient-amount-owed/<int:user_id>/', views.get_patient_amount_owed, name='get_patient_amount_owed'),
    path('api/admission/get-top-5-expensive-bills/<int:user_id>/', views.get_top_5_expensive_bills, name='get_top_5_expensive_bills'),
    path('api/admission/get-average-payment-per-bill/<int:user_id>/', views.get_average_payment_per_bill, name='get_average_payment_per_bill'),
    path('api/admission/get-bills-in-timeframe/<int:user_id>/', views.get_bills_in_timeframe, name='get_bills_in_timeframe'),
    path('api/admission/delete-payment-record/', views.delete_payment_record, name='delete_payment_record'),
]
