from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Badge, EarnedBadge

# Create your views here.

class BadgeListView(ListView):
    template_name = 'badges/list.html'

class BadgeDetailView(DetailView):
    template_name = 'badges/detail.html'

class MyBadgesView(LoginRequiredMixin, TemplateView):
    template_name = 'badges/my_badges.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get earned badges
        earned_badges = EarnedBadge.objects.filter(
            user=user
        ).select_related('badge', 'related_course').order_by('-earned_at')
        
        # Get available badges (not yet earned)
        earned_badge_ids = earned_badges.values_list('badge_id', flat=True)
        available_badges = Badge.objects.filter(
            is_active=True
        ).exclude(id__in=earned_badge_ids)
        
        context.update({
            'earned_badges': earned_badges,
            'available_badges': available_badges,
            'total_badges': Badge.objects.filter(is_active=True).count(),
            'earned_count': earned_badges.count(),
            'total_points': sum(badge.badge.points for badge in earned_badges),
        })
        
        return context

class BadgeCreateView(LoginRequiredMixin, CreateView):
    template_name = 'badges/create.html'

class BadgeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'badges/edit.html'
