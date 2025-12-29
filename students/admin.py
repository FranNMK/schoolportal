from django.contrib import admin
from .models import Student, Parent, StudentDocument


class StudentDocumentInline(admin.TabularInline):
    model = StudentDocument
    extra = 1


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Student model.
    """
    list_display = ('admission_number', 'full_name', 'current_stream', 'gender', 'status', 'is_active')
    list_filter = ('status', 'gender', 'is_active', 'current_stream', 'admission_date')
    search_fields = ('admission_number', 'first_name', 'last_name', 'email')
    inlines = [StudentDocumentInline]
    
    fieldsets = (
        ('Identification', {
            'fields': ('user', 'admission_number', 'profile_picture')
        }),
        ('Personal Information', {
            'fields': (('first_name', 'middle_name', 'last_name'), ('date_of_birth', 'gender'), 'admission_date')
        }),
        ('Academic Details', {
            'fields': ('current_stream', 'status', 'is_active')
        }),
        ('Medical Information', {
            'fields': ('blood_group', 'allergies', 'disability'),
            'classes': ('collapse',)
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Parent model.
    """
    list_display = ('full_name', 'relationship', 'phone', 'email')
    list_filter = ('relationship', 'is_active')
    search_fields = ('first_name', 'last_name', 'phone', 'email')
    filter_horizontal = ('students',)
    
    fieldsets = (
        ('Account', {
            'fields': ('user',)
        }),
        ('Personal Details', {
            'fields': (('first_name', 'last_name'), 'relationship', 'occupation')
        }),
        ('Contact Details', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Linked Students', {
            'fields': ('students',)
        }),
    )
