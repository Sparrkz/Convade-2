from django.db import models
from django.conf import settings
from courses.models import Course

class Badge(models.Model):
    BADGE_TYPES = [
        ('course_completion', 'Course Completion'),
        ('test_score', 'Test Score Achievement'),
        ('streak', 'Learning Streak'),
        ('participation', 'Participation'),
        ('custom', 'Custom Achievement'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES)
    icon = models.ImageField(upload_to='badges/', blank=True, null=True)
    points = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_badges',
        limit_choices_to={'role__in': ['teacher', 'admin']}
    )
    
    def __str__(self):
        return self.name
    
    @property
    def earned_count(self):
        return self.earned_badges.count()

class BadgeRule(models.Model):
    RULE_TYPES = [
        ('course_complete', 'Complete Course'),
        ('test_pass', 'Pass Test with Score'),
        ('login_streak', 'Login Streak Days'),
        ('custom', 'Custom Rule'),
    ]
    
    badge = models.OneToOneField(Badge, on_delete=models.CASCADE, related_name='rule')
    rule_type = models.CharField(max_length=15, choices=RULE_TYPES)
    target_course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    required_score = models.PositiveIntegerField(blank=True, null=True)  # For test-based badges
    required_count = models.PositiveIntegerField(default=1)  # For streak or multiple completions
    custom_condition = models.TextField(blank=True)  # For custom rules
    
    def __str__(self):
        return f"{self.badge.name} - {self.get_rule_type_display()}"

class EarnedBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='earned_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='earned_badges')
    earned_at = models.DateTimeField(auto_now_add=True)
    related_course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['user', 'badge']
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"
