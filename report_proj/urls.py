"""
URL configuration for report_proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  include("sales.urls"), name='sales'), # Main app urls
    path('reports/',  include("reports.urls"), name='reports'), # Main app urls
    path('my_profile/',  include("profiles.urls"), name='profiles'), # Main app urls

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

# Serve static files during development (only)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)