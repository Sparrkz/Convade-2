from django.db import models
from django.conf import settings
from courses.models import Course
from tests.models import Test

class UserActivity(models.Model):
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('course_view', 'Course View'),
        ('test_start', 'Test Started'),
        ('test_submit', 'Test Submitted'),
        ('badge_earned', 'Badge Earned'),
        ('certificate_issued', 'Certificate Issued'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    additional_data = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()}"

class CourseAnalytics(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='analytics')
    total_enrollments = models.PositiveIntegerField(default=0)
    completed_enrollments = models.PositiveIntegerField(default=0)
    average_completion_time_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Analytics for {self.course.title}"
    
    @property
    def completion_rate(self):
        if self.total_enrollments > 0:
            return round((self.completed_enrollments / self.total_enrollments) * 100, 2)
        return 0

class TestAnalytics(models.Model):
    test = models.OneToOneField(Test, on_delete=models.CASCADE, related_name='analytics')
    total_attempts = models.PositiveIntegerField(default=0)
    passed_attempts = models.PositiveIntegerField(default=0)
    average_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    average_time_minutes = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Analytics for {self.test.title}"
    
    @property
    def pass_rate(self):
        if self.total_attempts > 0:
            return round((self.passed_attempts / self.total_attempts) * 100, 2)
        return 0

class SystemAnalytics(models.Model):
    date = models.DateField(unique=True)
    total_users = models.PositiveIntegerField(default=0)
    active_users = models.PositiveIntegerField(default=0)
    new_registrations = models.PositiveIntegerField(default=0)
    total_courses = models.PositiveIntegerField(default=0)
    total_tests_taken = models.PositiveIntegerField(default=0)
    total_certificates_issued = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"System Analytics for {self.date}"
