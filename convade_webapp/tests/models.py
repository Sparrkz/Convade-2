from django.db import models
from django.conf import settings
from django.utils import timezone
from courses.models import Course

class Test(models.Model):
    TEST_TYPES = [
        ('quiz', 'Quiz'),
        ('exam', 'Exam'),
        ('assignment', 'Assignment'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tests')
    test_type = models.CharField(max_length=10, choices=TEST_TYPES, default='quiz')
    duration_minutes = models.PositiveIntegerField(default=30)
    max_attempts = models.PositiveIntegerField(default=1)
    passing_score = models.PositiveIntegerField(default=70)  # Percentage
    is_published = models.BooleanField(default=False)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tests',
        limit_choices_to={'role': 'teacher'}
    )
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    @property
    def total_questions(self):
        return self.questions.count()
    
    @property
    def is_active(self):
        now = timezone.now()
        if self.start_time and self.end_time:
            return self.start_time <= now <= self.end_time
        return self.is_published

class Question(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('text', 'Text Answer'),
        ('essay', 'Essay'),
    ]
    
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=15, choices=QUESTION_TYPES)
    points = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)
    explanation = models.TextField(blank=True)
    
    class Meta:
        ordering = ['order']
        unique_together = ['test', 'order']
    
    def __str__(self):
        return f"{self.test.title} - Q{self.order}"

class AnswerChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.question} - {self.choice_text[:50]}"

class TestSubmission(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
    ]
    
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='test_submissions',
        limit_choices_to={'role': 'student'}
    )
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='submissions')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='in_progress')
    attempt_number = models.PositiveIntegerField(default=1)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(blank=True, null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    time_taken_minutes = models.PositiveIntegerField(blank=True, null=True)
    
    class Meta:
        unique_together = ['student', 'test', 'attempt_number']
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.test.title} (Attempt {self.attempt_number})"
    
    def submit(self):
        self.status = 'submitted'
        self.submitted_at = timezone.now()
        if self.started_at:
            time_diff = self.submitted_at - self.started_at
            self.time_taken_minutes = int(time_diff.total_seconds() / 60)
        self.save()
    
    @property
    def is_passed(self):
        if self.score is not None:
            return self.score >= self.test.passing_score
        return False

class StudentAnswer(models.Model):
    submission = models.ForeignKey(TestSubmission, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choices = models.ManyToManyField(AnswerChoice, blank=True)
    text_answer = models.TextField(blank=True)
    points_earned = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_correct = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['submission', 'question']
    
    def __str__(self):
        return f"{self.submission} - {self.question}"
