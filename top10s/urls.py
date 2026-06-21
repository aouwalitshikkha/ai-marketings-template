from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProfileListView.as_view(), name="profile_list"),
    path("<slug:slug>/", views.ProfileDetailView.as_view(), name="profile_detail"),
]
