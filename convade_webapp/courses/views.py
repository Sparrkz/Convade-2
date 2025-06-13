from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class CourseListView(ListView):
    template_name = 'courses/list.html'

class CourseDetailView(DetailView):
    template_name = 'courses/detail.html'

class EnrollView(LoginRequiredMixin, TemplateView):
    template_name = 'courses/enroll.html'

class CourseContentView(LoginRequiredMixin, TemplateView):
    template_name = 'courses/content.html'

class MyCourseListView(LoginRequiredMixin, ListView):
    template_name = 'courses/my_courses.html'

class CourseCreateView(LoginRequiredMixin, CreateView):
    template_name = 'courses/create.html'

class CourseUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'courses/edit.html'
