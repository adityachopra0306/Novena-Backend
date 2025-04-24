from django.urls import path
from .views import login_view, profile_view, fetch_appointments_view, book_appointment_view, filter_appointments_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("profile/<int:user_id>/", profile_view, name="profile"),
    path("appointments/<int:user_id>/", fetch_appointments_view, name="fetch_appointments"),
    path("appointments/book/", book_appointment_view, name="book_appointment"),
    path('appointments/filter/<int:user_id>/', filter_appointments_view, name='filter_appointments'),
]
