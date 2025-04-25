from django.urls import path
from . import views

urlpatterns = [
    path('api/admission/get-available-rooms/', views.get_available_rooms, name='get_available_rooms'),
    path('api/admission/book-room/<int:user_id>/', views.book_room, name='book_room'),
    path('api/admission/get_admission_history/<int:user_id>/', views.get_admission_history, name='get_admission_history'),
]

