from django.urls import path
from .views import create_product  # Import the view or other views you have

urlpatterns = [
    path('', create_product, name='create_product'),
    # Add other URL patterns for the task app here
]