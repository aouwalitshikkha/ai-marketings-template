"""
URL configuration for aimrarket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.authtoken.views import obtain_auth_token
from glossary.views import GlossaryMarkdownView
from .views import home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    re_path(r'^glossary\.md$', GlossaryMarkdownView.as_view(), name='glossary_markdown'),
    path('blog/', include('blog.urls')),
    path('glossary/', include('glossary.urls')),
    path('top10/', include('top10s.urls')),
    path('courses/', include('courses.urls')),
    path('search/', include('search.urls')),
    path('', include('pages.urls')),
    path('api/', include('api.urls')),
    path('api/auth/', include('rest_framework.urls')),
    path('api/token/', obtain_auth_token, name='api_token'),
]
