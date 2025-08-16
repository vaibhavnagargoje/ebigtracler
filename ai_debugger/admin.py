from django.contrib import admin
from .models import AIAnalysisRequest

@admin.register(AIAnalysisRequest)
class AIAnalysisRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'submitted_by', 'language', 'status', 'submitted_at')
    list_filter = ('status', 'language', 'submitted_at')
    search_fields = ('submitted_by__username', 'code')
    readonly_fields = ('submitted_at',)
