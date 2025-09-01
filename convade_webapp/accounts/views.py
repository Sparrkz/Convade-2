from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from courses.models import Course, Enrollment

# Create your views here.

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Get latest enrollment for matric_no
        latest_enrollment = user.enrollments.order_by('-enrolled_at').first()
        context['matric_no'] = latest_enrollment.matric_no if latest_enrollment else ''

        # Ensure date_of_birth is available (from user or profile)
        dob = user.date_of_birth
        if not dob and hasattr(user, 'profile'):
            dob = user.profile.preferred_start_date or None
        context['date_of_birth'] = dob
        return context

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_student:
            # Student dashboard context
            enrollments = Enrollment.objects.filter(
                student=user, 
                is_active=True
            ).select_related('course', 'course__instructor')
            
            context.update({
                'enrolled_courses': enrollments,
                'total_courses': enrollments.count(),
                'completed_courses': enrollments.filter(progress=100).count(),
                'in_progress_courses': enrollments.filter(progress__gt=0, progress__lt=100).count(),
                # Recent courses (last 3)
                'recent_courses': enrollments.order_by('-enrolled_at')[:3],
            })
            
        elif user.is_teacher:
            # Teacher dashboard context
            taught_courses = Course.objects.filter(
                instructor=user
            ).annotate(
                student_count=Count('enrollments', filter=Q(enrollments__is_active=True))
            )
            
            context.update({
                'taught_courses': taught_courses,
                'total_courses': taught_courses.count(),
                'published_courses': taught_courses.filter(is_published=True).count(),
                'draft_courses': taught_courses.filter(is_published=False).count(),
                'total_students': taught_courses.aggregate(
                    total=Count('enrollments', filter=Q(enrollments__is_active=True))
                )['total'] or 0,
                # Recent courses (last 3)
                'recent_courses': taught_courses.order_by('-created_at')[:3],
            })
        
        return context

class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/settings.html'
