"""
URL configuration for schoolportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # ============================================
    # Public Pages
    # ============================================
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('features/', views.features, name='features'),
    path('admission/', views.admission, name='admission'),
    path('academics/', views.academics, name='academics'),
    path('contact/', views.contact, name='contact'),
    path('announcements/', views.announcements, name='announcements'),
    
    # ============================================
    # Portal Login Pages
    # ============================================
    path('portal/student/', views.student_portal, name='student_portal'),
    path('portal/teacher/', views.teacher_portal, name='teacher_portal'),
    path('portal/parent/', views.parent_portal, name='parent_portal'),
    path('portal/admin/', views.admin_portal, name='admin_portal'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
