from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class BadgeListView(ListView):
    template_name = 'badges/list.html'

class BadgeDetailView(DetailView):
    template_name = 'badges/detail.html'

class MyBadgesView(LoginRequiredMixin, TemplateView):
    template_name = 'badges/my_badges.html'

class BadgeCreateView(LoginRequiredMixin, CreateView):
    template_name = 'badges/create.html'

class BadgeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'badges/edit.html'
