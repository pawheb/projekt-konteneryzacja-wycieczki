# trips/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_trips, name='list_trips'),
    path('<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('generate-pdf/<int:trip_id>/', views.generate_trip_pdf, name='generate_trip_pdf'),
    path('generate-individual-pdf/', views.create_individual_plan, name='generate_individual_pdf'),
]
