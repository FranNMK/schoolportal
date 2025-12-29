"""
Admin configuration for School Management models.
"""

from django.contrib import admin
from .models import (
    School, Department, GradeClass, Stream,
    AcademicYear, Term, Subject, ClassSubject, AcademicCalendarEvent,
    GradingScale, GradingLevel, ClassPeriod, Lesson
)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    """Admin configuration for School model."""
    list_display = ['name', 'school_type', 'phone', 'email', 'is_active']
    list_filter = ['school_type', 'is_active', 'country']
    search_fields = ['name', 'email', 'phone', 'registration_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'motto', 'logo', 'school_type')
        }),
        ('Contact Information', {
            'fields': ('address', 'city', 'country', 'phone', 'phone_secondary', 'email', 'website')
        }),
        ('Administration', {
            'fields': ('principal_name', 'registration_number', 'established_date')
        }),
        ('Social Media', {
            'fields': ('facebook', 'twitter', 'instagram'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin configuration for Department model."""
    list_display = ['name', 'code', 'school', 'is_active']
    list_filter = ['school', 'is_active']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(GradeClass)
class GradeClassAdmin(admin.ModelAdmin):
    """Admin configuration for GradeClass model."""
    list_display = ['name', 'level', 'school', 'total_streams', 'is_active']
    list_filter = ['school', 'is_active', 'level']
    search_fields = ['name']
    ordering = ['level', 'name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    """Admin configuration for Stream model."""
    list_display = ['__str__', 'grade_class', 'capacity', 'room_number', 'is_active']
    list_filter = ['grade_class__school', 'grade_class', 'is_active']
    search_fields = ['name', 'grade_class__name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    """Admin configuration for AcademicYear model."""
    list_display = ['name', 'school', 'start_date', 'end_date', 'is_current', 'is_active']
    list_filter = ['school', 'is_current', 'is_active']
    search_fields = ['name']
    ordering = ['-start_date']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    """Admin configuration for Term model."""
    list_display = ['name', 'academic_year', 'term_number', 'start_date', 'end_date', 'is_current', 'is_active']
    list_filter = ['academic_year__school', 'academic_year', 'term_number', 'is_current', 'is_active']
    search_fields = ['name', 'academic_year__name']
    ordering = ['academic_year', 'term_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('academic_year', 'name', 'term_number')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
        ('Important Dates', {
            'fields': ('mid_term_break_start', 'mid_term_break_end', 'exam_start_date', 'exam_end_date'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_current', 'is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(GradingScale)
class GradingScaleAdmin(admin.ModelAdmin):
    """Admin configuration for GradingScale model."""
    list_display = ['name', 'school', 'is_active']
    list_filter = ['school', 'is_active']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(GradingLevel)
class GradingLevelAdmin(admin.ModelAdmin):
    """Admin configuration for GradingLevel model."""
    list_display = ['name', 'abbreviation', 'min_score', 'max_score', 'scale']
    list_filter = ['scale__school', 'scale']
    search_fields = ['name', 'abbreviation']
    ordering = ['scale', '-min_score']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Admin configuration for Subject model."""
    list_display = ['name', 'code', 'department', 'school', 'grading_scale', 'is_elective', 'is_examinable', 'is_active']
    list_filter = ['school', 'department', 'grading_scale', 'is_elective', 'is_examinable', 'is_active']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('school', 'department', 'name', 'code', 'description')
        }),
        ('Configuration', {
            'fields': ('grading_scale', 'is_elective', 'is_examinable', 'max_marks', 'pass_marks')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    """Admin configuration for ClassSubject model."""
    list_display = ['grade_class', 'subject', 'periods_per_week', 'is_active']
    list_filter = ['grade_class__school', 'grade_class', 'subject', 'is_active']
    search_fields = ['grade_class__name', 'subject__name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ClassPeriod)
class ClassPeriodAdmin(admin.ModelAdmin):
    """Admin configuration for ClassPeriod model."""
    list_display = ['name', 'start_time', 'end_time', 'order', 'school', 'is_break']
    list_filter = ['school', 'is_break']
    ordering = ['school', 'order']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Admin configuration for Lesson model."""
    list_display = ['day_of_week', 'period', 'stream', 'subject', 'room']
    list_filter = ['stream__grade_class__school', 'day_of_week', 'stream', 'subject']
    search_fields = ['stream__grade_class__name', 'subject__name', 'room']


@admin.register(AcademicCalendarEvent)
class AcademicCalendarEventAdmin(admin.ModelAdmin):
    """Admin configuration for AcademicCalendarEvent model."""
    list_display = ['title', 'event_type', 'start_date', 'end_date', 'school', 'is_public', 'is_active']
    list_filter = ['school', 'event_type', 'is_public', 'is_active', 'academic_year', 'term']
    search_fields = ['title', 'description']
    date_hierarchy = 'start_date'
    ordering = ['-start_date']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Event Details', {
            'fields': ('school', 'academic_year', 'term', 'title', 'description', 'event_type')
        }),
        ('Date & Time', {
            'fields': ('start_date', 'end_date', 'is_all_day', 'start_time', 'end_time')
        }),
        ('Settings', {
            'fields': ('is_public', 'is_active', 'created_at', 'updated_at')
        }),
    )
