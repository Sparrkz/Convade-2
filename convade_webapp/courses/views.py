from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from .models import Course, CourseContent, CourseCategory, Enrollment, HomeCourse
from .forms import CourseForm, CourseSearchForm

# Create your views here.

class CourseListView(ListView):
    model = Course
    template_name = 'courses/list.html'
    context_object_name = 'courses'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Course.objects.filter(is_published=True).annotate(
            student_count=Count('enrollments', filter=Q(enrollments__is_active=True))
        ).select_related('instructor').prefetch_related('categories')
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(instructor__first_name__icontains=search_query) |
                Q(instructor__last_name__icontains=search_query)
            )
        
        # Category filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(categories=category)
        
        # Difficulty filter
        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Price filter
        price_filter = self.request.GET.get('price')
        if price_filter == 'free':
            queryset = queryset.filter(price=0)
        elif price_filter == 'paid':
            queryset = queryset.filter(price__gt=0)
        
        # Sorting
        sort = self.request.GET.get('sort', '-created_at')
        if sort == 'price_low':
            queryset = queryset.order_by('price')
        elif sort == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort == 'popular':
            queryset = queryset.order_by('-student_count')
        elif sort == 'newest':
            queryset = queryset.order_by('-created_at')
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CourseCategory.objects.all()
        context['search_form'] = CourseSearchForm(self.request.GET)
        context['current_filters'] = {
            'search': self.request.GET.get('search', ''),
            'category': self.request.GET.get('category', ''),
            'difficulty': self.request.GET.get('difficulty', ''),
            'price': self.request.GET.get('price', ''),
            'sort': self.request.GET.get('sort', 'newest'),
        }
        return context

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/detail.html'
    context_object_name = 'course'
    
    def get_queryset(self):
        return Course.objects.filter(is_published=True).select_related('instructor').prefetch_related('categories', 'contents')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        
        # Check if user is enrolled
        if self.request.user.is_authenticated:
            try:
                enrollment = Enrollment.objects.get(student=self.request.user, course=course)
                context['is_enrolled'] = True
                context['enrollment'] = enrollment
            except Enrollment.DoesNotExist:
                context['is_enrolled'] = False
        else:
            context['is_enrolled'] = False
        
        # Get course content
        context['contents'] = course.contents.all().order_by('order')
        context['free_contents'] = course.contents.filter(is_free=True).order_by('order')
        
        # Similar courses
        context['similar_courses'] = Course.objects.filter(
            categories__in=course.categories.all(),
            is_published=True
        ).exclude(pk=course.pk).distinct()[:4]
        
        return context

class EnrollView(LoginRequiredMixin, TemplateView):
    template_name = 'courses/enroll.html'
    
    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk, is_published=True)
        
        # Check if already enrolled
        if Enrollment.objects.filter(student=request.user, course=course).exists():
            messages.warning(request, 'You are already enrolled in this course!')
            return redirect('courses:detail', pk=course.pk)
        
        # Create enrollment
        enrollment = Enrollment.objects.create(
            student=request.user,
            course=course,
            is_active=True
        )
        
        messages.success(request, f'Successfully enrolled in {course.title}!')
        return redirect('courses:content', pk=course.pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, pk=kwargs['pk'], is_published=True)
        return context

class CourseContentView(LoginRequiredMixin, TemplateView):
    template_name = 'courses/content.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, pk=kwargs['pk'], is_published=True)
        
        # Check enrollment
        try:
            enrollment = Enrollment.objects.get(student=self.request.user, course=course)
            context['enrollment'] = enrollment
            context['course'] = course
            context['contents'] = course.contents.all().order_by('order')
        except Enrollment.DoesNotExist:
            messages.error(self.request, 'You must be enrolled to access course content.')
            return redirect('courses:detail', pk=course.pk)
        
        return context

class MyCourseListView(LoginRequiredMixin, ListView):
    template_name = 'courses/my_courses.html'
    context_object_name = 'enrollments'
    paginate_by = 12
    
    def get_queryset(self):
        return Enrollment.objects.filter(
            student=self.request.user,
            is_active=True
        ).select_related('course', 'course__instructor').order_by('-enrolled_at')

class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/create.html'
    success_url = reverse_lazy('courses:list')
    
    def test_func(self):
        return self.request.user.is_teacher or self.request.user.is_admin
    
    def form_valid(self, form):
        form.instance.instructor = self.request.user
        messages.success(self.request, 'Course created successfully!')
        return super().form_valid(form)

class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/edit.html'
    
    def test_func(self):
        course = self.get_object()
        return (self.request.user == course.instructor or 
                self.request.user.is_admin)
    
    def get_success_url(self):
        return reverse('courses:detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Course updated successfully!')
        return super().form_valid(form)

# API Views for AJAX requests
def course_search_api(request):
    """API endpoint for course search autocomplete"""
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    courses = Course.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query),
        is_published=True
    )[:10]
    
    results = [{
        'id': course.id,
        'title': course.title,
        'instructor': course.instructor.get_full_name(),
        'price': str(course.price)
    } for course in courses]
    
    return JsonResponse({'results': results})

def update_progress(request, pk):
    """Update course progress"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    course = get_object_or_404(Course, pk=pk)
    try:
        enrollment = Enrollment.objects.get(student=request.user, course=course)
        progress = int(request.POST.get('progress', 0))
        enrollment.progress = min(max(progress, 0), 100)
        enrollment.save()
        
        if enrollment.progress == 100 and not enrollment.completed_at:
            enrollment.mark_as_completed()
            return JsonResponse({
                'success': True, 
                'completed': True,
                'message': 'Congratulations! You have completed the course!'
            })
        
        return JsonResponse({'success': True, 'progress': enrollment.progress})
    except Enrollment.DoesNotExist:
        return JsonResponse({'error': 'Not enrolled in this course'}, status=400)


# def home(request):
#     courses = HomeCourse.objects.all()
#     print("Courses in DB:", courses)  # check terminal
#     return render(request, 'base/home.html', {'courses': courses})
