from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class TestListView(ListView):
    template_name = 'tests/list.html'

class TestDetailView(DetailView):
    template_name = 'tests/detail.html'

class TakeTestView(LoginRequiredMixin, TemplateView):
    template_name = 'tests/take.html'

class SubmitTestView(LoginRequiredMixin, TemplateView):
    template_name = 'tests/submit.html'

class TestResultsView(LoginRequiredMixin, TemplateView):
    template_name = 'tests/results.html'

class TestCreateView(LoginRequiredMixin, CreateView):
    template_name = 'tests/create.html'

class TestUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'tests/edit.html'
