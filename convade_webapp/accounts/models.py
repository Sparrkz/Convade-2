from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
    
    @property
    def is_student(self):
        return self.role == 'student'
    
    @property
    def is_teacher(self):
        return self.role == 'teacher'
    
    @property
    def is_admin(self):
        return self.role == 'admin'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    middle_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    highest_qualification = models.CharField(max_length=100, blank=True)
    current_status = models.CharField(max_length=100, blank=True)
    field_of_study = models.CharField(max_length=100, blank=True)
    mode_of_learning = models.CharField(max_length=100, blank=True)
    preferred_start_date = models.DateField(blank=True, null=True)
    motivation = models.TextField(blank=True)
    career_aspiration = models.CharField(max_length=100, blank=True)
    sponsorship = models.CharField(max_length=100, blank=True)
    payment_plan = models.CharField(max_length=100, blank=True)
    proof_of_payment = models.FileField(upload_to='proof_of_payment/', blank=True, null=True)
    has_laptop = models.BooleanField(default=False)
    has_internet = models.BooleanField(default=False)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    agree_terms = models.BooleanField(default=False)
    agree_attendance = models.BooleanField(default=False)
    agree_privacy = models.BooleanField(default=False)
    passport_photo = models.ImageField(upload_to='passport_photos/', blank=True, null=True)
    id_card = models.FileField(upload_to='id_cards/', blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
