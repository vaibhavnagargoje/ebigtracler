from django.contrib import admin
from .models import Bug, BugAttachment, BugComment, BugHistory

class BugAttachmentInline(admin.TabularInline):
    model = BugAttachment
    extra = 0

class BugCommentInline(admin.TabularInline):
    model = BugComment
    extra = 0

class BugHistoryInline(admin.TabularInline):
    model = BugHistory
    extra = 0
    readonly_fields = ('user', 'action', 'timestamp')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Bug)
class BugAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'project', 'status', 'priority', 'severity', 'reported_by', 'assigned_to')
    list_filter = ('status', 'priority', 'severity', 'project')
    search_fields = ('title', 'description', 'tags')
    inlines = [BugAttachmentInline, BugCommentInline, BugHistoryInline]
    date_hierarchy = 'created_at'

@admin.register(BugAttachment)
class BugAttachmentAdmin(admin.ModelAdmin):
    list_display = ('bug', 'filename', 'uploaded_by', 'uploaded_at')
    list_filter = ('uploaded_at', 'uploaded_by')
    search_fields = ('filename', 'bug__title')

@admin.register(BugComment)
class BugCommentAdmin(admin.ModelAdmin):
    list_display = ('bug', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'bug__title')

@admin.register(BugHistory)
class BugHistoryAdmin(admin.ModelAdmin):
    list_display = ('bug', 'user', 'action', 'timestamp')
    list_filter = ('timestamp', 'user')
    search_fields = ('action', 'bug__title')
    readonly_fields = ('bug', 'user', 'action', 'timestamp')
