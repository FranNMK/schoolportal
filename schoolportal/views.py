"""
Views for the main SchoolPortal public pages.
"""
from django.shortcuts import render


# ============================================
# Public Pages
# ============================================

def home(request):
    """Homepage view with hero section, features, and announcements."""
    return render(request, 'pages/home.html')


def about(request):
    """About page with school information and values."""
    return render(request, 'pages/about.html')


def features(request):
    """Features page showcasing all system modules."""
    return render(request, 'pages/features.html')


def admission(request):
    """Admission page with application form and requirements."""
    return render(request, 'pages/admission.html')


def academics(request):
    """Academics page with programs, calendar, and grading system."""
    return render(request, 'pages/academics.html')


def contact(request):
    """Contact page with form and contact information."""
    return render(request, 'pages/contact.html')


def announcements(request):
    """Announcements/Noticeboard page with latest news."""
    return render(request, 'pages/announcements.html')


# ============================================
# Portal Login Pages
# ============================================

def student_portal(request):
    """Student portal login page."""
    return render(request, 'portals/student_portal.html')


def teacher_portal(request):
    """Teacher portal login page."""
    return render(request, 'portals/teacher_portal.html')


def parent_portal(request):
    """Parent portal login page."""
    return render(request, 'portals/parent_portal.html')


def admin_portal(request):
    """Admin portal login page."""
    return render(request, 'portals/admin_portal.html')
