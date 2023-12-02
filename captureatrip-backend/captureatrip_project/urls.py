"""captureatrip_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

urlpatterns = [
    path('superadmin/', admin.site.urls),
    
    path('', include('common_app.urls.customer_urls')),
    path('admin/', include('common_app.urls.admin_urls')),
    
    path('trip/', include('trip_app.urls.customer_urls')),
    path('admin/trip/', include('trip_app.urls.admin_urls')),
    
    path('category/', include('category_app.urls.customer_urls')),
    path('admin/category/', include('category_app.urls.admin_urls')),

    path('silk/', include('silk.urls', namespace='silk')),
        
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)