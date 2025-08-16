from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('create/', views.create_project, name='create_project'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('<int:project_id>/delete/', views.delete_project, name='delete_project'),
    path('<int:project_id>/versions/', views.version_list, name='version_list'),
    path('<int:project_id>/versions/create/', views.create_version, name='create_version'),
    path('<int:project_id>/versions/<int:version_id>/', views.version_detail, name='version_detail'),
    path('<int:project_id>/versions/<int:version_id>/edit/', views.edit_version, name='edit_version'),
    path('<int:project_id>/versions/<int:version_id>/delete/', views.delete_version, name='delete_version'),
    path('<int:project_id>/members/', views.manage_members, name='manage_members'),
]
