from django.db import models
from django.conf import settings
from courses.models import Course
import uuid
from django.utils import timezone

class CertificateTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    template_file = models.FileField(upload_to='certificate_templates/')
    background_image = models.ImageField(upload_to='cert_backgrounds/', blank=True, null=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_templates',
        limit_choices_to={'role__in': ['teacher', 'admin']}
    )
    
    def __str__(self):
        return self.name

class Certificate(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('issued', 'Issued'),
        ('revoked', 'Revoked'),
    ]
    
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='certificates',
        limit_choices_to={'role': 'student'}
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    certificate_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    template = models.ForeignKey(CertificateTemplate, on_delete=models.SET_NULL, null=True)
    issued_at = models.DateTimeField(blank=True, null=True)
    completion_date = models.DateField()
    final_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    verification_code = models.CharField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-issued_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.course.title} Certificate"
    
    def save(self, *args, **kwargs):
        if not self.verification_code:
            self.verification_code = f"CONV-{str(self.certificate_id)[:8].upper()}"
        super().save(*args, **kwargs)
    
    def issue_certificate(self):
        self.status = 'issued'
        self.issued_at = timezone.now()
        self.save()
    
    @property
    def is_valid(self):
        return self.status == 'issued'

class CertificateVerification(models.Model):
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE, related_name='verifications')
    verified_at = models.DateTimeField(auto_now_add=True)
    verified_by_ip = models.GenericIPAddressField(blank=True, null=True)
    verifier_info = models.TextField(blank=True)  # Browser/device info
    
    def __str__(self):
        return f"Verification for {self.certificate.verification_code}"
