from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.db import transaction
from django.db.models import Count, Avg, Q, Max
from .models import Test, Question, AnswerChoice, TestSubmission
from .forms import TestForm, QuestionForm, AnswerChoiceForm, QuestionFormSet
from courses.models import Course

# Create your views here.

class TestListView(LoginRequiredMixin, ListView):
    model = Test
    template_name = 'tests/list.html'
    context_object_name = 'tests'
    paginate_by = 12
    
    def get_queryset(self):
        if self.request.user.is_teacher:
            # Teachers see their own tests
            return Test.objects.filter(
                created_by=self.request.user
            ).select_related('course').annotate(
                submission_count=Count('submissions')
            ).order_by('-created_at')
        else:
            # Students see published tests from their enrolled courses
            enrolled_courses = Course.objects.filter(
                enrollments__student=self.request.user,
                enrollments__is_active=True
            )
            return Test.objects.filter(
                course__in=enrolled_courses,
                is_published=True
            ).select_related('course', 'created_by').order_by('-created_at')

class TestDetailView(LoginRequiredMixin, DetailView):
    model = Test
    template_name = 'tests/detail.html'
    context_object_name = 'test'
    
    def get_queryset(self):
        if self.request.user.is_teacher:
            return Test.objects.filter(created_by=self.request.user)
        else:
            # Students can only view tests from courses they're enrolled in
            enrolled_courses = Course.objects.filter(
                enrollments__student=self.request.user,
                enrollments__is_active=True
            )
            return Test.objects.filter(
                course__in=enrolled_courses,
                is_published=True
            )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test = self.get_object()
        
        if self.request.user.is_teacher:
            # Teacher view - show analytics
            context['questions'] = test.questions.all().order_by('order')
            context['submissions'] = test.submissions.all().select_related('student')
            context['total_submissions'] = test.submissions.count()
            context['average_score'] = test.submissions.filter(
                score__isnull=False
            ).aggregate(avg_score=Avg('score'))['avg_score'] or 0
        else:
            # Student view - show their attempts
            context['user_submissions'] = test.submissions.filter(
                student=self.request.user
            ).order_by('-started_at')
            context['can_attempt'] = (
                context['user_submissions'].count() < test.max_attempts and
                test.is_active
            )
        
        return context

class TestCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Test
    form_class = TestForm
    template_name = 'tests/create.html'
    
    def test_func(self):
        return self.request.user.is_teacher
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Test created successfully! Now add questions to complete your test.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('tests:add_questions', kwargs={'pk': self.object.pk})

class AddQuestionsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'tests/add_questions.html'
    
    def test_func(self):
        test = get_object_or_404(Test, pk=self.kwargs['pk'])
        return self.request.user.is_teacher and test.created_by == self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test = get_object_or_404(Test, pk=self.kwargs['pk'])
        context['test'] = test
        context['questions'] = test.questions.all().order_by('order')
        return context
    
    def post(self, request, *args, **kwargs):
        test = get_object_or_404(Test, pk=self.kwargs['pk'])
        
        # Handle adding a new question
        question_text = request.POST.get('question_text')
        question_type = request.POST.get('question_type')
        points = request.POST.get('points', 1)
        explanation = request.POST.get('explanation', '')
        
        if question_text and question_type:
            # Get the next order number
            last_order = test.questions.aggregate(
                max_order=Max('order')
            )['max_order'] or 0
            
            question = Question.objects.create(
                test=test,
                question_text=question_text,
                question_type=question_type,
                points=int(points),
                explanation=explanation,
                order=last_order + 1
            )
            
            # Handle answer choices for multiple choice questions
            if question_type == 'multiple_choice':
                choices = request.POST.getlist('choices[]')
                correct_choices = request.POST.getlist('correct_choices[]')
                
                for i, choice_text in enumerate(choices):
                    if choice_text.strip():
                        AnswerChoice.objects.create(
                            question=question,
                            choice_text=choice_text,
                            is_correct=str(i) in correct_choices,
                            order=i
                        )
            
            elif question_type == 'true_false':
                correct_answer = request.POST.get('true_false_answer')
                AnswerChoice.objects.create(
                    question=question,
                    choice_text='True',
                    is_correct=(correct_answer == 'true'),
                    order=0
                )
                AnswerChoice.objects.create(
                    question=question,
                    choice_text='False',
                    is_correct=(correct_answer == 'false'),
                    order=1
                )
            
            messages.success(request, 'Question added successfully!')
        
        return redirect('tests:add_questions', pk=test.pk)

class TakeTestView(LoginRequiredMixin, TemplateView):
    template_name = 'tests/take.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test = get_object_or_404(Test, pk=self.kwargs['pk'])
        
        # Check if user can take this test
        if not test.is_active:
            messages.error(self.request, 'This test is not currently available.')
            return redirect('tests:detail', pk=test.pk)
        
        # Check enrollment
        if not test.course.enrollments.filter(
            student=self.request.user, 
            is_active=True
        ).exists():
            messages.error(self.request, 'You must be enrolled in this course to take the test.')
            return redirect('courses:detail', pk=test.course.pk)
        
        # Check attempts
        user_attempts = test.submissions.filter(student=self.request.user).count()
        if user_attempts >= test.max_attempts:
            messages.error(self.request, 'You have reached the maximum number of attempts for this test.')
            return redirect('tests:detail', pk=test.pk)
        
        context['test'] = test
        context['questions'] = test.questions.all().order_by('order')
        context['attempt_number'] = user_attempts + 1
        
        return context

class SubmitTestView(LoginRequiredMixin, TemplateView):
    template_name = 'tests/submit.html'

class TestResultsView(LoginRequiredMixin, TemplateView):
    template_name = 'tests/results.html'

class TestUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Test
    form_class = TestForm
    template_name = 'tests/edit.html'
    
    def test_func(self):
        test = self.get_object()
        return self.request.user.is_teacher and test.created_by == self.request.user
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, 'Test updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('tests:detail', kwargs={'pk': self.object.pk})

class MyTestsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Test
    template_name = 'tests/my_tests.html'
    context_object_name = 'tests'
    paginate_by = 12
    
    def test_func(self):
        return self.request.user.is_teacher
    
    def get_queryset(self):
        return Test.objects.filter(
            created_by=self.request.user
        ).select_related('course').annotate(
            submission_count=Count('submissions'),
            average_score=Avg('submissions__score')
        ).order_by('-created_at')
