from django.urls import path
from .views import ussd_callback

urlpatterns = [
    # Namespaced under /api/ussd/ by project urls
    path('ussd/', ussd_callback, name='api_ussd_callback'),
]