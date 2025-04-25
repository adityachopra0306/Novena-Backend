from django.urls import path
from . import views

urlpatterns = [
    path('staff/<str:category>/', views.staff_list, name='staff_list'),
]
