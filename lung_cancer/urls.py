from . import views
from django.urls import path
urlpatterns = [
    path("", views.lung_cancer_detection, name="lung_cancer_detection"),
    
]