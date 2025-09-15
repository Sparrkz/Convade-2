from django.db import models
from django.conf import settings
from django.utils import timezone

class CourseCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Course Categories'

    def __str__(self):
        return self.name

class Course(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='taught_courses',
        limit_choices_to={'role': 'teacher'}
    )
    categories = models.ManyToManyField(CourseCategory, related_name='courses', blank=True)  # ← Moved here
    difficulty = models.CharField(max_length=12, choices=DIFFICULTY_CHOICES, default='beginner')
    duration_hours = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        default_permissions = ('add', 'change', 'delete', 'view')
    
    def __str__(self):
        return self.title
    
    @property
    def enrolled_students_count(self):
        return self.enrollments.filter(is_active=True).count()

class CourseContent(models.Model):
    CONTENT_TYPES = [
        ('video', 'Video'),
        ('text', 'Text'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contents')
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    content = models.TextField()  # For text content or video URLs
    file_attachment = models.FileField(upload_to='course_content/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_free = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
        unique_together = ['course', 'order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='enrollments',
        limit_choices_to={'role': 'student'}
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    progress = models.PositiveIntegerField(default=0)  # Progress percentage
    completed_at = models.DateTimeField(blank=True, null=True)
    matric_no = models.CharField(max_length=32, blank=True, null=True, unique=True)
    
    class Meta:
        unique_together = ['student', 'course']
    
    def __str__(self):
        return f"{self.student.username} - {self.course.title}"
    
    def mark_as_completed(self):
        self.progress = 100
        self.completed_at = timezone.now()
        self.save()



class HomeCourse(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    number_of_lessons = models.PositiveIntegerField()
    duration = models.CharField(max_length=50)  # e.g. "120h 45min"
    reviews_count = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='courses/')
    course_url = models.URLField(blank=True, null=True)  # link to course page

    class Meta:
        verbose_name = "Home Course"
        verbose_name_plural = "Home Courses"

    def __str__(self):
        return self.title

class EnrollmentApplication(models.Model):
    # Link to user and course
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollment_applications')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollment_applications')

    # Personal Information
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    nationality = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    CONTACT_CHOICES = [('phone', 'Phone'), ('whatsapp', 'WhatsApp'), ('email', 'Email')]
    preferred_contact_method = models.CharField(max_length=10, choices=CONTACT_CHOICES)

    # Educational Background
    QUALIFICATION_CHOICES = [('secondary', 'Secondary School'), ('undergraduate', 'Undergraduate'), ('graduate', 'Graduate'), ('other', 'Other')]
    highest_qualification = models.CharField(max_length=20, choices=QUALIFICATION_CHOICES)
    STATUS_CHOICES = [('student', 'Student'), ('graduate', 'Graduate'), ('professional', 'Working Professional'), ('entrepreneur', 'Entrepreneur')]
    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    field_of_study = models.CharField(max_length=100, blank=True, null=True)

    # Course Preferences
    LEARNING_MODE_CHOICES = [('online', 'Online Live Classes'), ('self_paced', 'Self-paced'), ('hybrid', 'Hybrid')]
    mode_of_learning = models.CharField(max_length=20, choices=LEARNING_MODE_CHOICES)
    preferred_start_date = models.DateField()

    # Motivation and Aspirations
    motivation = models.TextField()
    ASPIRATION_CHOICES = [('tech_career', 'Tech Career'), ('startup', 'Start-up'), ('freelancing', 'Freelancing'), ('job_readiness', 'Job Readiness')]
    career_aspiration = models.CharField(max_length=20, choices=ASPIRATION_CHOICES)

    # Financial Information
    SPONSORSHIP_CHOICES = [('self', 'Self'), ('parent', 'Parent'), ('employer', 'Employer'), ('scholarship', 'Scholarship')]
    sponsorship = models.CharField(max_length=20, choices=SPONSORSHIP_CHOICES)
    PAYMENT_PLAN_CHOICES = [('full', 'Full'), ('installment', 'Installment'), ('subscription', 'Subscription')]
    payment_plan = models.CharField(max_length=20, choices=PAYMENT_PLAN_CHOICES)

    # Technical Readiness
    has_laptop = models.BooleanField(default=False)
    has_internet = models.BooleanField(default=False)

    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_relationship = models.CharField(max_length=50)
    emergency_contact_phone = models.CharField(max_length=20)

    # Agreements
    agree_terms = models.BooleanField()
    agree_attendance = models.BooleanField()
    agree_privacy = models.BooleanField()

    # Document Uploads
    passport_photo = models.ImageField(upload_to='enrollment_passports/')
    id_card = models.ImageField(upload_to='enrollment_ids/')

    # Admin fields
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')

    def __str__(self):
        return f"Application for {self.first_name} {self.last_name} - {self.course.title}"
