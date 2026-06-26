from django.urls import path
from . import views

urlpatterns = [
    path('', views.GlossaryIndexView.as_view(), name='glossary_index'),
]
