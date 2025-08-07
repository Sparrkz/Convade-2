from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# ---popup event----
from django.http import JsonResponse
from .models import PopupEvent, PopupClick
from django.views.decorators.csrf import csrf_exempt


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


# -----pop up------
@csrf_exempt
def record_popup_click(request):
    if request.method == "POST":
        active_popup = PopupEvent.objects.filter(is_active=True).first()
        if active_popup:
            ip = get_client_ip(request)
            PopupClick.objects.create(event=active_popup, ip_address=ip)
        return JsonResponse({"status": "logged"})
    return JsonResponse({"status": "failed"}, status=400)

def get_client_ip(request):
    x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded:
        return x_forwarded.split(',')[0]
    return request.META.get('REMOTE_ADDR')
    clicked_at = models.DateTimeField(auto_now_add=True)

def get_active_popup(request):
    popup = PopupEvent.objects.filter(is_active=True).first()
    if popup:
        return JsonResponse({
            "title": popup.title,
            "message": popup.message,
            "url": popup.google_form_url
        })
    return JsonResponse({}, status=204)