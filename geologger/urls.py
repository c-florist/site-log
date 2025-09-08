from django.urls import path
from .views import TechnicianLocationPingView

urlpatterns = [
    path('technicians/<int:technician_id>/ping/', TechnicianLocationPingView.as_view(), name='technician-ping'),
]
