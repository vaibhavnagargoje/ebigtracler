from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('my-bugs/', views.my_bugs, name='my_bugs'),
    path('my-projects/', views.my_projects, name='my_projects'),
    path('recent-activity/', views.recent_activity, name='recent_activity'),
    path('stats/', views.statistics, name='statistics'),
]
