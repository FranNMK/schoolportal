"""
School Management Models

This module contains all models related to school management including:
- School profile and settings
- Departments
- Classes and Streams
- Academic Years and Terms
- Subjects and Class-Subject assignments
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class School(models.Model):
    """
    School Profile - stores basic information about the school.
    This is the root model that other models reference.
    """
    SCHOOL_TYPE_CHOICES = [
        ('primary', 'Primary School'),
        ('secondary', 'Secondary School'),
        ('combined', 'Combined (Primary & Secondary)'),
    ]
    
    name = models.CharField(max_length=200, help_text="Official school name")
    motto = models.CharField(max_length=255, blank=True, help_text="School motto")
    logo = models.ImageField(upload_to='school/logos/', blank=True, null=True)
    address = models.TextField(help_text="Physical address")
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='Kenya')
    phone = models.CharField(max_length=20, help_text="Primary contact phone")
    phone_secondary = models.CharField(max_length=20, blank=True, help_text="Secondary phone")
    email = models.EmailField(help_text="Official school email")
    website = models.URLField(blank=True, help_text="School website URL")
    established_date = models.DateField(blank=True, null=True, help_text="When school was founded")
    registration_number = models.CharField(max_length=100, blank=True, help_text="Government registration number")
    principal_name = models.CharField(max_length=200, blank=True, help_text="Current principal's name")
    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPE_CHOICES, default='combined')
    
    # Social media
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'School'
        verbose_name_plural = 'Schools'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Department(models.Model):
    """
    Academic departments within the school (e.g., Science, Languages, Arts).
    """
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100, help_text="Department name")
    code = models.CharField(max_length=10, blank=True, help_text="Short code (e.g., SCI, LANG)")
    description = models.TextField(blank=True)
    # head_of_department will be added when Teacher model is available
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        ordering = ['name']
        unique_together = ['school', 'name']
    
    def __str__(self):
        return f"{self.name}"


class GradeClass(models.Model):
    """
    Grade/Class levels (e.g., Grade 1, Grade 2, Form 1, Form 2).
    Named GradeClass to avoid conflict with Python's 'class' keyword.
    """
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='grade_classes')
    name = models.CharField(max_length=50, help_text="Class name (e.g., Grade 1, Form 1)")
    level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        help_text="Numeric level for ordering (1-20)"
    )
    description = models.TextField(blank=True)
    # class_teacher will be added when Teacher model is available
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'
        ordering = ['level', 'name']
        unique_together = ['school', 'name']
    
    def __str__(self):
        return self.name
    
    @property
    def total_streams(self):
        return self.streams.filter(is_active=True).count()
    
    @property
    def total_students(self):
        # Will be implemented when Student model is available
        return 0


class Stream(models.Model):
    """
    Streams/Sections within a class (e.g., Grade 1A, Grade 1B, Grade 1 East).
    Each stream can hold a certain number of students.
    """
    grade_class = models.ForeignKey(GradeClass, on_delete=models.CASCADE, related_name='streams')
    name = models.CharField(max_length=50, help_text="Stream name (e.g., A, B, East, West)")
    capacity = models.PositiveIntegerField(default=40, help_text="Maximum number of students")
    # class_teacher will be added when Teacher model is available
    room_number = models.CharField(max_length=20, blank=True, help_text="Classroom number/name")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Stream'
        verbose_name_plural = 'Streams'
        ordering = ['grade_class__level', 'name']
        unique_together = ['grade_class', 'name']
    
    def __str__(self):
        return f"{self.grade_class.name} {self.name}"
    
    @property
    def full_name(self):
        return f"{self.grade_class.name} {self.name}"
    
    @property
    def current_enrollment(self):
        # Will be implemented when Student model is available
        return 0
    
    @property
    def available_slots(self):
        return self.capacity - self.current_enrollment


class AcademicYear(models.Model):
    """
    Academic year periods (e.g., 2024/2025).
    """
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='academic_years')
    name = models.CharField(max_length=50, help_text="Year name (e.g., 2024/2025)")
    start_date = models.DateField(help_text="Academic year start date")
    end_date = models.DateField(help_text="Academic year end date")
    is_current = models.BooleanField(default=False, help_text="Mark as current active year")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Academic Year'
        verbose_name_plural = 'Academic Years'
        ordering = ['-start_date']
        unique_together = ['school', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Ensure only one current year per school
        if self.is_current:
            AcademicYear.objects.filter(school=self.school, is_current=True).update(is_current=False)
        super().save(*args, **kwargs)


class Term(models.Model):
    """
    Academic terms/semesters within an academic year.
    """
    TERM_CHOICES = [
        (1, 'Term 1 / Semester 1'),
        (2, 'Term 2 / Semester 2'),
        (3, 'Term 3'),
    ]
    
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='terms')
    name = models.CharField(max_length=50, help_text="Term name (e.g., Term 1, First Semester)")
    term_number = models.PositiveIntegerField(choices=TERM_CHOICES, help_text="Term order (1, 2, or 3)")
    start_date = models.DateField(help_text="Term start date")
    end_date = models.DateField(help_text="Term end date")
    is_current = models.BooleanField(default=False, help_text="Mark as current active term")
    
    # Important dates within the term
    mid_term_break_start = models.DateField(blank=True, null=True)
    mid_term_break_end = models.DateField(blank=True, null=True)
    exam_start_date = models.DateField(blank=True, null=True, help_text="Final exams start")
    exam_end_date = models.DateField(blank=True, null=True, help_text="Final exams end")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Term'
        verbose_name_plural = 'Terms'
        ordering = ['academic_year', 'term_number']
        unique_together = ['academic_year', 'term_number']
    
    def __str__(self):
        return f"{self.academic_year.name} - {self.name}"
    
    def save(self, *args, **kwargs):
        # Ensure only one current term per academic year's school
        if self.is_current:
            Term.objects.filter(
                academic_year__school=self.academic_year.school, 
                is_current=True
            ).update(is_current=False)
        super().save(*args, **kwargs)


class GradingScale(models.Model):
    """
    Defines a grading scale (e.g., CBC/CDB, Standard 8-4-4, etc.)
    """
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='grading_scales')
    name = models.CharField(max_length=100, help_text="Name of the grading scale (e.g., CBC, Standard)")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Grading Scale'
        verbose_name_plural = 'Grading Scales'
        unique_together = ['school', 'name']

    def __str__(self):
        return f"{self.name} ({self.school.name})"


class GradingLevel(models.Model):
    """
    Specific levels within a grading scale.
    Example for CDB: Below Expectation (0-29%), etc.
    """
    scale = models.ForeignKey(GradingScale, on_delete=models.CASCADE, related_name='levels')
    name = models.CharField(max_length=100, help_text="e.g., Exceeding Expectation")
    abbreviation = models.CharField(max_length=10, blank=True, help_text="e.g., EE, ME, AE, BE")
    min_score = models.DecimalField(
        max_digits=5, decimal_places=2, 
        help_text="Minimum percentage for this level (0-100)"
    )
    max_score = models.DecimalField(
        max_digits=5, decimal_places=2, 
        help_text="Maximum percentage for this level (0-100)"
    )
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Grading Level'
        verbose_name_plural = 'Grading Levels'
        ordering = ['-min_score']
        unique_together = ['scale', 'name']

    def __str__(self):
        return f"{self.name} ({self.min_score}% - {self.max_score}%)"


class Subject(models.Model):
    """
    Academic subjects offered by the school.
    """
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='subjects')
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, 
        related_name='subjects', blank=True, null=True
    )
    name = models.CharField(max_length=100, help_text="Subject name")
    code = models.CharField(max_length=10, help_text="Subject code (e.g., MATH, ENG)")
    description = models.TextField(blank=True)
    is_elective = models.BooleanField(default=False, help_text="Is this an elective subject?")
    is_examinable = models.BooleanField(default=True, help_text="Does this subject have exams?")
    
    # Grading configuration
    grading_scale = models.ForeignKey(
        GradingScale, on_delete=models.SET_NULL, 
        related_name='subjects', blank=True, null=True,
        help_text="The grading scale used for this subject"
    )
    max_marks = models.PositiveIntegerField(default=100, help_text="Maximum marks for the subject")
    pass_marks = models.PositiveIntegerField(default=40, help_text="Minimum marks to pass")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        ordering = ['name']
        unique_together = ['school', 'code']
    
    def get_grade(self, score_percentage):
        """
        Returns the GradingLevel for a given score percentage.
        """
        if not self.grading_scale:
            return None
        return self.grading_scale.levels.filter(
            min_score__lte=score_percentage, 
            max_score__gte=score_percentage
        ).first()

    def __str__(self):
        return f"{self.name} ({self.code})"


class ClassSubject(models.Model):
    """
    Links subjects to specific classes.
    This allows different classes to have different subjects.
    """
    grade_class = models.ForeignKey(GradeClass, on_delete=models.CASCADE, related_name='class_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='class_subjects')
    # teacher will be added when Teacher model is available
    periods_per_week = models.PositiveIntegerField(default=4, help_text="Number of periods per week")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Class Subject'
        verbose_name_plural = 'Class Subjects'
        ordering = ['grade_class__level', 'subject__name']
        unique_together = ['grade_class', 'subject']
    
    def __str__(self):
        return f"{self.grade_class.name} - {self.subject.name}"


class ClassPeriod(models.Model):
    """
    Defines the timing for lessons (e.g., Period 1, Break, Lunch).
    """
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='periods')
    name = models.CharField(max_length=50, help_text="e.g., Period 1, Morning Break")
    start_time = models.TimeField()
    end_time = models.TimeField()
    order = models.PositiveIntegerField(help_text="Display order")
    is_break = models.BooleanField(default=False, help_text="Is this a break/non-teaching period?")
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Class Period'
        verbose_name_plural = 'Class Periods'
        ordering = ['order', 'start_time']
        unique_together = ['school', 'order']

    def __str__(self):
        return f"{self.name} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"


class Lesson(models.Model):
    """
    A specific timetable entry linking a subject, teacher, and stream to a period.
    """
    DAY_CHOICES = [
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (0, 'Sunday'),
    ]

    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name='timetable')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lessons')
    period = models.ForeignKey(ClassPeriod, on_delete=models.CASCADE, related_name='lessons')
    day_of_week = models.PositiveSmallIntegerField(choices=DAY_CHOICES)
    
    # Optional fields
    room = models.CharField(max_length=50, blank=True, help_text="Specific room if different from stream room")
    # teacher = models.ForeignKey('teachers.Teacher', ...) - Will be linked when Teacher model is ready
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
        unique_together = ['stream', 'period', 'day_of_week']
        ordering = ['day_of_week', 'period__order']

    def __str__(self):
        return f"{self.get_day_of_week_display()} - {self.period.name}: {self.subject.name}"

class AcademicCalendarEvent(models.Model):
    """
    Academic calendar events (holidays, exams, sports days, etc.)
    """
    EVENT_TYPE_CHOICES = [
        ('holiday', 'Public Holiday'),
        ('break', 'School Break'),
        ('exam', 'Examination'),
        ('meeting', 'Meeting'),
        ('sports', 'Sports Event'),
        ('cultural', 'Cultural Event'),
        ('ceremony', 'Ceremony'),
        ('other', 'Other'),
    ]
    
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='calendar_events')
    academic_year = models.ForeignKey(
        AcademicYear, on_delete=models.CASCADE, 
        related_name='calendar_events', blank=True, null=True
    )
    term = models.ForeignKey(
        Term, on_delete=models.CASCADE, 
        related_name='calendar_events', blank=True, null=True
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='other')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Leave blank for single-day events")
    is_all_day = models.BooleanField(default=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    
    # Visibility
    is_public = models.BooleanField(default=True, help_text="Visible to all users")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Calendar Event'
        verbose_name_plural = 'Calendar Events'
        ordering = ['start_date', 'start_time']
    
    def __str__(self):
        return f"{self.title} ({self.start_date})"
