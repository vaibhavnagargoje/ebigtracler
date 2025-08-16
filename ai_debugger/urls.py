from django.urls import path
from . import views

app_name = 'ai_debugger'

urlpatterns = [
    path('', views.analysis_home, name='analysis_home'),
    path('submit/', views.submit_analysis, name='submit_analysis'),
    path('history/', views.analysis_history, name='analysis_history'),
    path('results/<int:analysis_id>/', views.analysis_results, name='analysis_results'),
]
