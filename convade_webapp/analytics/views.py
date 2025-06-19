from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Avg, Sum, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from courses.models import Course, Enrollment
from tests.models import Test, TestSubmission
from badges.models import Badge, EarnedBadge
from certifications.models import Certificate
from accounts.models import User
from .models import UserActivity, CourseAnalytics, TestAnalytics, SystemAnalytics

# Create your views here.

class AnalyticsDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'analytics/dashboard.html'

    def test_func(self):
        return self.request.user.is_teacher or self.request.user.is_admin
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_teacher:
            # Teacher Analytics
            context.update(self.get_teacher_analytics(user))
        elif user.is_admin:
            # Admin Analytics
            context.update(self.get_admin_analytics())
        
        return context
    
    def get_teacher_analytics(self, teacher):
        # Get teacher's courses
        courses = Course.objects.filter(instructor=teacher)
        
        # Basic stats
        total_courses = courses.count()
        published_courses = courses.filter(is_published=True).count()
        total_students = Enrollment.objects.filter(
            course__instructor=teacher,
            is_active=True
        ).values('student').distinct().count()
        
        # Course enrollments
        total_enrollments = Enrollment.objects.filter(
            course__instructor=teacher,
            is_active=True
        ).count()
        
        # Test statistics
        tests = Test.objects.filter(created_by=teacher)
        total_tests = tests.count()
        published_tests = tests.filter(is_published=True).count()
        total_test_submissions = TestSubmission.objects.filter(
            test__created_by=teacher
        ).count()
        
        # Revenue (if courses have prices)
        total_revenue = 0
        for course in courses:
            enrollment_count = course.enrollments.filter(is_active=True).count()
            total_revenue += (course.price or 0) * enrollment_count
        
        # Recent activity
        recent_enrollments = Enrollment.objects.filter(
            course__instructor=teacher,
            is_active=True
        ).select_related('student', 'course').order_by('-enrolled_at')[:10]
        
        recent_submissions = TestSubmission.objects.filter(
            test__created_by=teacher,
            status='submitted'
        ).select_related('student', 'test').order_by('-submitted_at')[:10]
        
        # Course performance
        course_stats = courses.annotate(
            enrollment_count=Count('enrollments', filter=Q(enrollments__is_active=True)),
            completion_rate=Avg('enrollments__progress')
        ).order_by('-enrollment_count')[:5]
        
        # Test performance
        test_stats = tests.annotate(
            submission_count=Count('submissions'),
            avg_score=Avg('submissions__score')
        ).order_by('-submission_count')[:5]
        
        # Calculate pass rate manually for each test
        for test in test_stats:
            total_submissions = test.submissions.count()
            if total_submissions > 0:
                passed_submissions = test.submissions.filter(score__gte=test.passing_score).count()
                test.pass_rate = (passed_submissions / total_submissions) * 100
            else:
                test.pass_rate = 0
        
        # Monthly enrollment trends (last 6 months)
        six_months_ago = timezone.now() - timedelta(days=180)
        monthly_enrollments = []
        for i in range(6):
            month_start = six_months_ago + timedelta(days=30*i)
            month_end = month_start + timedelta(days=30)
            count = Enrollment.objects.filter(
                course__instructor=teacher,
                enrolled_at__range=[month_start, month_end]
            ).count()
            monthly_enrollments.append({
                'month': month_start.strftime('%b %Y'),
                'count': count
            })
        
        return {
            'total_courses': total_courses,
            'published_courses': published_courses,
            'total_students': total_students,
            'total_enrollments': total_enrollments,
            'total_tests': total_tests,
            'published_tests': published_tests,
            'total_test_submissions': total_test_submissions,
            'total_revenue': total_revenue,
            'recent_enrollments': recent_enrollments,
            'recent_submissions': recent_submissions,
            'course_stats': course_stats,
            'test_stats': test_stats,
            'monthly_enrollments': monthly_enrollments,
        }
    
    def get_admin_analytics(self):
        # System-wide statistics
        total_users = User.objects.count()
        total_students = User.objects.filter(role='student').count()
        total_teachers = User.objects.filter(role='teacher').count()
        total_courses = Course.objects.count()
        published_courses = Course.objects.filter(is_published=True).count()
        total_tests = Test.objects.count()
        total_enrollments = Enrollment.objects.filter(is_active=True).count()
        
        # Recent activity
        recent_users = User.objects.order_by('-date_joined')[:10]
        recent_courses = Course.objects.select_related('instructor').order_by('-created_at')[:10]
        
        return {
            'total_users': total_users,
            'total_students': total_students,
            'total_teachers': total_teachers,
            'total_courses': total_courses,
            'published_courses': published_courses,
            'total_tests': total_tests,
            'total_enrollments': total_enrollments,
            'recent_users': recent_users,
            'recent_courses': recent_courses,
        }

class CourseAnalyticsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'analytics/courses.html'

    def test_func(self):
        return self.request.user.is_teacher or self.request.user.is_admin
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_teacher:
            courses = Course.objects.filter(instructor=user)
        else:
            courses = Course.objects.all()
        
        # Detailed course analytics
        course_analytics = courses.annotate(
            enrollment_count=Count('enrollments', filter=Q(enrollments__is_active=True)),
            completed_count=Count('enrollments', filter=Q(enrollments__progress=100)),
            avg_progress=Avg('enrollments__progress')
        ).order_by('-enrollment_count')
        
        # Calculate revenue manually for each course
        for course in course_analytics:
            enrollment_count = course.enrollments.filter(is_active=True).count()
            course.total_revenue = (course.price or 0) * enrollment_count
        
        context['course_analytics'] = course_analytics
        return context

class TestAnalyticsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'analytics/tests.html'

    def test_func(self):
        return self.request.user.is_teacher or self.request.user.is_admin
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_teacher:
            tests = Test.objects.filter(created_by=user)
        else:
            tests = Test.objects.all()
        
        # Detailed test analytics
        test_analytics = tests.annotate(
            submission_count=Count('submissions'),
            avg_score=Avg('submissions__score'),
            avg_time=Avg('submissions__time_taken_minutes')
        ).order_by('-submission_count')
        
        # Calculate pass/fail counts manually for each test
        for test in test_analytics:
            test.pass_count = test.submissions.filter(score__gte=test.passing_score).count()
            test.fail_count = test.submissions.filter(score__lt=test.passing_score).count()
        
        context['test_analytics'] = test_analytics
        return context

class UserAnalyticsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'analytics/users.html'

    def test_func(self):
        return self.request.user.is_admin
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # User statistics
        user_stats = {
            'total_users': User.objects.count(),
            'active_users': User.objects.filter(is_active=True).count(),
            'students': User.objects.filter(role='student').count(),
            'teachers': User.objects.filter(role='teacher').count(),
            'admins': User.objects.filter(role='admin').count(),
        }
        
        # Registration trends
        thirty_days_ago = timezone.now() - timedelta(days=30)
        daily_registrations = []
        for i in range(30):
            day = thirty_days_ago + timedelta(days=i)
            count = User.objects.filter(
                date_joined__date=day.date()
            ).count()
            daily_registrations.append({
                'date': day.strftime('%Y-%m-%d'),
                'count': count
            })
        
        context.update({
            'user_stats': user_stats,
            'daily_registrations': daily_registrations,
        })
        return context

class ReportsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'analytics/reports.html'
    
    def test_func(self):
        return self.request.user.is_teacher or self.request.user.is_admin
