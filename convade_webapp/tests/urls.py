from django.urls import path
from . import views

app_name = 'tests'

urlpatterns = [
    path('', views.TestListView.as_view(), name='list'),
    path('my-tests/', views.MyTestsView.as_view(), name='my_tests'),
    path('create/', views.TestCreateView.as_view(), name='create'),
    path('<int:pk>/', views.TestDetailView.as_view(), name='detail'),
    path('<int:pk>/add-questions/', views.AddQuestionsView.as_view(), name='add_questions'),
    path('<int:pk>/take/', views.TakeTestView.as_view(), name='take'),
    path('<int:pk>/submit/', views.SubmitTestView.as_view(), name='submit'),
    path('<int:pk>/results/', views.TestResultsView.as_view(), name='results'),
    path('<int:pk>/edit/', views.TestUpdateView.as_view(), name='edit'),
] 