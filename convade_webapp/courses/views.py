
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
import requests
from django.conf import settings

class PaymentMethodSelectView(LoginRequiredMixin, TemplateView):
    template_name = 'courses/payment_method_select.html'

    def get(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['pk'])
        return render(request, self.template_name, {'course': course})

# Paystack and Flutterwave payment initiation stubs
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class PaystackInitView(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['pk'])
        user = request.user
        amount = int(float(course.price) * 100)  # Paystack expects amount in kobo
        paystack_secret = getattr(settings, 'PAYSTACK_SECRET_KEY', None)
        if not paystack_secret:
            return render(request, 'courses/payment_error.html', {'message': 'Paystack secret key not set.'})
        headers = {
            'Authorization': f'Bearer {paystack_secret}',
            'Content-Type': 'application/json',
        }
        callback_url = request.build_absolute_uri(reverse('courses:payment_confirmed', kwargs={'pk': course.pk}))
        data = {
            'email': user.email,
            'amount': amount,
            'callback_url': callback_url,
        }
        response = requests.post('https://api.paystack.co/transaction/initialize', json=data, headers=headers)
        if response.status_code == 200 and response.json().get('status'):
            auth_url = response.json()['data']['authorization_url']
            return redirect(auth_url)
        else:
            error_msg = response.json().get('message', 'Paystack payment initialization failed.')
            return render(request, 'courses/payment_error.html', {'message': error_msg})

@method_decorator(csrf_exempt, name='dispatch')
class FlutterwaveInitView(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['pk'])
        user = request.user
        amount = float(course.price)
        flutterwave_secret = getattr(settings, 'FLUTTERWAVE_SECRET_KEY', None)
        if not flutterwave_secret:
            return render(request, 'courses/payment_error.html', {'message': 'Flutterwave secret key not set.'})
        headers = {
            'Authorization': f'Bearer {flutterwave_secret}',
            'Content-Type': 'application/json',
        }
        callback_url = request.build_absolute_uri(reverse('courses:payment_confirmed', kwargs={'pk': course.pk}))
        tx_ref = f"CV-{course.pk}-{user.pk}-{user.id}-{user.username}"
        data = {
            "tx_ref": tx_ref,
            "amount": amount,
            "currency": "NGN",  # Use NGN for test mode
            "redirect_url": callback_url,
            "customer": {
                "email": user.email,
                "name": f"{user.first_name} {user.last_name}",
            },
            "customizations": {
                "title": course.title,
                "description": f"Payment for {course.title}",
            }
        }
        response = requests.post('https://api.flutterwave.com/v3/payments', json=data, headers=headers)
        if response.status_code == 200 and response.json().get('status') == 'success':
            link = response.json()['data']['link']
            return redirect(link)
        else:
            error_msg = response.json().get('message', 'Flutterwave payment initialization failed.')
            return render(request, 'courses/payment_error.html', {'message': error_msg})


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import EnrollmentForm
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from .models import Course, CourseContent, CourseCategory, Enrollment, HomeCourse, EnrollmentApplication
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

from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, FormView
from .forms import CourseForm, CourseSearchForm, EnrollmentForm

class EnrollView(LoginRequiredMixin, CreateView):
    model = EnrollmentApplication
    form_class = EnrollmentForm
    template_name = 'courses/enroll.html'

    def get_success_url(self):
        return reverse('courses:enroll_success', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, pk=self.kwargs['pk'])
        return context

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial.update({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        })
        # You can pre-populate more fields from the user's profile if they exist
        return initial

    def form_valid(self, form):
        course = get_object_or_404(Course, pk=kwargs['pk'])

        if Enrollment.objects.filter(student=self.request.user, course=course).exists():
            messages.warning(request, 'You are already enrolled in this course!')
            return redirect('courses:detail', pk=course.pk)

        form.instance.student = self.request.user
        form.instance.course = course

        response = super().form_valid(form)

        messages.success(self.request, 'Your enrollment application has been submitted successfully!')

        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user,
            course=course,
            defaults={'is_active': True}
        )
        if created:
            matric_no = f"CV{enrollment.pk:05d}"
            enrollment.matric_no = matric_no
            enrollment.save()
            self.request.session['matric_no'] = matric_no

        return response


# Step 3: Show course info and payment CTA
class EnrollSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'courses/enroll_success.html'

    def get(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['pk'])
        matric_no = ''
        try:
            from .models import Enrollment
            enrollment = Enrollment.objects.get(student=request.user, course=course)
            matric_no = enrollment.matric_no or ''
        except Exception:
            matric_no = ''
        return render(request, self.template_name, {'course': course, 'matric_no': matric_no})


# Step 4: Payment page (redirect to Paystack or show payment instructions)
class PaymentView(LoginRequiredMixin, TemplateView):
    template_name = 'courses/payment_receipt_upload.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'course': get_object_or_404(Course, pk=kwargs['pk'])})

    def post(self, request, *args, **kwargs):
        # Save uploaded receipt (implement as needed)
        receipt = request.FILES.get('receipt')
        # Here you would save the receipt to the Enrollment or a related model
        # For now, just simulate confirmation
        return redirect('courses:payment_confirmed', pk=kwargs['pk'])


# Step 5: Payment confirmation page

class PaymentConfirmedView(LoginRequiredMixin, TemplateView):
    template_name = 'courses/payment_confirmed.html'

    def get(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['pk'])
        flutterwave_ref = request.GET.get('tx_ref')
        payment_verified = False
        message = ''
        if flutterwave_ref:
            secret = getattr(settings, 'FLUTTERWAVE_SECRET_KEY', None)
            headers = {'Authorization': f'Bearer {secret}'}
            url = f'https://api.flutterwave.com/v3/transactions/verify_by_reference?tx_ref={flutterwave_ref}'
            resp = requests.get(url, headers=headers)
            data = resp.json()
            if data.get('status') == 'success' and data['data']['status'] == 'successful':
                payment_verified = True
            else:
                message = data.get('message', 'Flutterwave verification failed.')
        else:
            message = 'No payment reference provided.'

        # Mark enrollment as paid if verified
        if payment_verified:
            try:
                enrollment = Enrollment.objects.get(student=request.user, course=course)
                enrollment.is_active = True  # or set a paid flag if you have one
                enrollment.save()
            except Enrollment.DoesNotExist:
                pass
            return render(request, self.template_name, {'course': course, 'success': True})
        else:
            return render(request, self.template_name, {'course': course, 'success': False, 'message': message})

class CourseContentView(LoginRequiredMixin, TemplateView):
    template_name = 'courses/content.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, pk=kwargs['pk'], is_published=True)

        # Check enrollment and payment
        try:
            enrollment = Enrollment.objects.get(student=self.request.user, course=course)
            if not enrollment.is_active:
                messages.error(self.request, 'You must complete payment to access course content.')
                return redirect('courses:payment', pk=course.pk)
            context['enrollment'] = enrollment
            context['course'] = course
            context['contents'] = course.contents.all().order_by('order')
        except Enrollment.DoesNotExist:
            messages.error(self.request, 'You must enroll and pay to access course content.')
            return redirect('courses:payment', pk=course.pk)

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
