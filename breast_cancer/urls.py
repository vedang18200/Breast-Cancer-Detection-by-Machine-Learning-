from . import views
from django.urls import path
urlpatterns = [
    path("", views.predict_cancer, name="predict_cancer"),
    
]