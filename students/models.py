from django.db import models
from django.conf import settings
from django.utils import timezone
from classes.models import Stream


class Student(models.Model):
    """
    Student profile model linking to the custom User model.
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('alumni', 'Alumni'),
        ('suspended', 'Suspended'),
        ('transferred', 'Transferred'),
        ('withdrawn', 'Withdrawn'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    # Links
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='student_profile',
        blank=True, null=True,
        help_text="Reference to the user account for portal access"
    )
    current_stream = models.ForeignKey(
        Stream, 
        on_delete=models.SET_NULL, 
        related_name='students', 
        blank=True, null=True
    )
    
    # Identification
    admission_number = models.CharField(max_length=50, unique=True, help_text="Unique admission number")
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    
    # Personal info
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    admission_date = models.DateField(default=timezone.now)
    
    # Contact (Usually for students who are independent or for older students)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    # Physical/Health info
    profile_picture = models.ImageField(upload_to='students/profiles/', blank=True, null=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    allergies = models.TextField(blank=True, help_text="Medical allergies or conditions")
    disability = models.TextField(blank=True, help_text="Any physical disabilities")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ['admission_number', 'last_name', 'first_name']

    def __str__(self):
        return f"{self.admission_number} - {self.full_name}"

    @property
    def full_name(self):
        names = [self.first_name, self.middle_name, self.last_name]
        return " ".join([n for n in names if n])


class Parent(models.Model):
    """
    Parent/Guardian model linking to students.
    """
    RELATIONSHIP_CHOICES = [
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Guardian'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='parent_profile',
        blank=True, null=True
    )
    
    # Personal Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    occupation = models.CharField(max_length=100, blank=True)
    
    # Contact
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    # Links to students
    students = models.ManyToManyField(Student, related_name='parents', blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Parent/Guardian'
        verbose_name_plural = 'Parents/Guardians'

    def __str__(self):
        return f"{self.full_name} ({self.get_relationship_display()})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class StudentDocument(models.Model):
    """
    Documents uploaded for a student (e.g., Birth cert, Report cards).
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='students/documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.admission_number} - {self.title}"
