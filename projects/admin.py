from django.contrib import admin
from .models import Project, ProjectVersion

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('name', 'description', 'manager__username')
    filter_horizontal = ('members',)

@admin.register(ProjectVersion)
class ProjectVersionAdmin(admin.ModelAdmin):
    list_display = ('project', 'version_number', 'release_date')
    list_filter = ('release_date', 'project')
    search_fields = ('version_number', 'project__name', 'notes')
