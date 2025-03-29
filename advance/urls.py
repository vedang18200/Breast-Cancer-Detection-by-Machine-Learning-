from django.urls import path
from .views import advance_page

urlpatterns = [
    path('', advance_page, name='advance'),
]
