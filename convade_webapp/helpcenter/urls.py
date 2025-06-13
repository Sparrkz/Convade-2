from django.urls import path
from . import views

app_name = 'helpcenter'

urlpatterns = [
    path('', views.HelpCenterView.as_view(), name='index'),
    path('articles/', views.ArticleListView.as_view(), name='articles'),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('support/', views.SupportTicketCreateView.as_view(), name='support'),
    path('tickets/', views.TicketListView.as_view(), name='tickets'),
    path('tickets/<int:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'),
] 