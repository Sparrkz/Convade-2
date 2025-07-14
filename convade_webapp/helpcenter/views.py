from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class HelpCenterView(TemplateView):
    template_name = 'helpcenter/index.html'

class TermsAndConditionsView(TemplateView):
    template_name = 'helpcenter/terms.html'

class PolicyView(TemplateView):
    template_name = 'helpcenter/policy.html'

class ArticleListView(ListView):
    template_name = 'helpcenter/articles.html'

class ArticleDetailView(DetailView):
    template_name = 'helpcenter/article_detail.html'

class FAQView(TemplateView):
    template_name = 'helpcenter/faq.html'

class SupportTicketCreateView(LoginRequiredMixin, CreateView):
    template_name = 'helpcenter/support.html'

class TicketListView(LoginRequiredMixin, ListView):
    template_name = 'helpcenter/tickets.html'

class TicketDetailView(LoginRequiredMixin, DetailView):
    template_name = 'helpcenter/ticket_detail.html'
