from django.urls import path
from . import views

app_name = 'bugs'

urlpatterns = [
    path('', views.bug_list, name='bug_list'),
    path('create/', views.create_bug, name='create_bug'),
    path('<int:bug_id>/', views.bug_detail, name='bug_detail'),
    path('<int:bug_id>/edit/', views.edit_bug, name='edit_bug'),
    path('<int:bug_id>/delete/', views.delete_bug, name='delete_bug'),
    path('<int:bug_id>/status/', views.change_status, name='change_status'),
    path('<int:bug_id>/comment/', views.add_comment, name='add_comment'),
    path('<int:bug_id>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('<int:bug_id>/attach/', views.add_attachment, name='add_attachment'),
    path('<int:bug_id>/attach/<int:attachment_id>/delete/', views.delete_attachment, name='delete_attachment'),
    path('search/', views.search_bugs, name='search_bugs'),
]
