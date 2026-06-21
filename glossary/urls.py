from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='glossary_index'),
]
