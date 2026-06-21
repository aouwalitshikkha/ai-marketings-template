from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogHomeView.as_view(), name='blog_home'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='blog_category'),
]
