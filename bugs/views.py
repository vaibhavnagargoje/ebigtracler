from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Bug, BugAttachment, BugComment, BugHistory
from projects.models import Project, ProjectVersion

@login_required
def bug_list(request):
    """Display list of all bugs."""
    bugs = Bug.objects.all()
    
    # Filter by project if specified
    project_id = request.GET.get('project')
    if project_id:
        bugs = bugs.filter(project_id=project_id)
    
    # Filter by status if specified
    status = request.GET.get('status')
    if status:
        bugs = bugs.filter(status=status)
    
    # Filter by priority if specified
    priority = request.GET.get('priority')
    if priority:
        bugs = bugs.filter(priority=priority)
    
    return render(request, 'bugs/bug_list.html', {'bugs': bugs})

@login_required
def create_bug(request):
    """Create a new bug."""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        project_id = request.POST.get('project')
        version_id = request.POST.get('project_version')
        priority = request.POST.get('priority')
        severity = request.POST.get('severity')
        
        # Create the bug
        bug = Bug.objects.create(
            title=title,
            description=description,
            project_id=project_id,
            reported_by=request.user,
            priority=priority,
            severity=severity,
        )
        
        # Set project version if provided
        if version_id:
            bug.project_version_id = version_id
            bug.save()
        
        # Create history entry
        BugHistory.objects.create(
            bug=bug,
            user=request.user,
            action=f"Created bug"
        )
        
        # Handle file attachments
        if 'attachments' in request.FILES:
            for file in request.FILES.getlist('attachments'):
                BugAttachment.objects.create(
                    bug=bug,
                    file=file,
                    filename=file.name,
                    uploaded_by=request.user
                )
        
        messages.success(request, f'Bug "{title}" has been created.')
        return redirect('bugs:bug_detail', bug_id=bug.id)
    
    # Get projects for the form
    projects = Project.objects.all()
    
    return render(request, 'bugs/create_bug.html', {'projects': projects})

@login_required
def bug_detail(request, bug_id):
    """Display bug details."""
    bug = get_object_or_404(Bug, id=bug_id)
    comments = bug.comments.all()
    attachments = bug.attachments.all()
    history = bug.history.all()
    
    context = {
        'bug': bug,
        'comments': comments,
        'attachments': attachments,
        'history': history
    }
    
    return render(request, 'bugs/bug_detail.html', context)

@login_required
def edit_bug(request, bug_id):
    """Edit bug details."""
    bug = get_object_or_404(Bug, id=bug_id)
    
    if request.method == 'POST':
        old_title = bug.title
        old_priority = bug.priority
        old_severity = bug.severity
        old_status = bug.status
        
        bug.title = request.POST.get('title', bug.title)
        bug.description = request.POST.get('description', bug.description)
        bug.priority = request.POST.get('priority', bug.priority)
        bug.severity = request.POST.get('severity', bug.severity)
        bug.status = request.POST.get('status', bug.status)
        
        # Assign to user if specified
        assigned_to_id = request.POST.get('assigned_to')
        if assigned_to_id:
            bug.assigned_to_id = assigned_to_id
        
        # Update project version if specified
        version_id = request.POST.get('project_version')
        if version_id:
            bug.project_version_id = version_id
        
        bug.save()
        
        # Create history entries for changes
        changes = []
        if old_title != bug.title:
            changes.append(f"Changed title from '{old_title}' to '{bug.title}'")
        if old_priority != bug.priority:
            changes.append(f"Changed priority from '{old_priority}' to '{bug.priority}'")
        if old_severity != bug.severity:
            changes.append(f"Changed severity from '{old_severity}' to '{bug.severity}'")
        if old_status != bug.status:
            changes.append(f"Changed status from '{old_status}' to '{bug.status}'")
            
            # Set resolved date if status changed to resolved
            if bug.status == 'resolved' and old_status != 'resolved':
                bug.resolved_at = timezone.now()
                bug.save()
        
        for change in changes:
            BugHistory.objects.create(
                bug=bug,
                user=request.user,
                action=change
            )
        
        messages.success(request, f'Bug #{bug.id} has been updated.')
        return redirect('bugs:bug_detail', bug_id=bug.id)
    
    # Get data for form
    projects = Project.objects.all()
    versions = ProjectVersion.objects.filter(project=bug.project)
    
    context = {
        'bug': bug,
        'projects': projects,
        'versions': versions
    }
    
    return render(request, 'bugs/edit_bug.html', context)

@login_required
def delete_bug(request, bug_id):
    """Delete a bug."""
    bug = get_object_or_404(Bug, id=bug_id)
    
    if request.method == 'POST':
        bug_id = bug.id
        bug.delete()
        messages.success(request, f'Bug #{bug_id} has been deleted.')
        return redirect('bugs:bug_list')
    
    return render(request, 'bugs/delete_bug.html', {'bug': bug})

@login_required
def change_status(request, bug_id):
    """Change the status of a bug."""
    bug = get_object_or_404(Bug, id=bug_id)
    
    if request.method == 'POST':
        old_status = bug.status
        new_status = request.POST.get('status')
        
        if new_status and new_status != old_status:
            bug.status = new_status
            
            # Set resolved date if status changed to resolved
            if new_status == 'resolved' and old_status != 'resolved':
                bug.resolved_at = timezone.now()
                
            bug.save()
            
            # Create history entry
            BugHistory.objects.create(
                bug=bug,
                user=request.user,
                action=f"Changed status from '{old_status}' to '{new_status}'"
            )
            
            messages.success(request, f'Bug status updated to {new_status}.')
        
        return redirect('bugs:bug_detail', bug_id=bug.id)
    
    return render(request, 'bugs/change_status.html', {'bug': bug})

@login_required
def add_comment(request, bug_id):
    """Add a comment to a bug."""
    bug = get_object_or_404(Bug, id=bug_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        
        if content:
            comment = BugComment.objects.create(
                bug=bug,
                author=request.user,
                content=content
            )
            
            # Create history entry
            BugHistory.objects.create(
                bug=bug,
                user=request.user,
                action=f"Added comment: {content[:50]}..."
            )
            
            messages.success(request, 'Your comment has been added.')
        
        return redirect('bugs:bug_detail', bug_id=bug.id)
    
    return render(request, 'bugs/add_comment.html', {'bug': bug})

@login_required
def delete_comment(request, bug_id, comment_id):
    """Delete a comment."""
    bug = get_object_or_404(Bug, id=bug_id)
    comment = get_object_or_404(BugComment, id=comment_id, bug=bug)
    
    # Only allow the author or admin to delete
    if request.user != comment.author and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this comment.')
        return redirect('bugs:bug_detail', bug_id=bug.id)
    
    if request.method == 'POST':
        comment.delete()
        
        # Create history entry
        BugHistory.objects.create(
            bug=bug,
            user=request.user,
            action=f"Deleted a comment"
        )
        
        messages.success(request, 'Comment has been deleted.')
        return redirect('bugs:bug_detail', bug_id=bug.id)
    
    return render(request, 'bugs/delete_comment.html', {'bug': bug, 'comment': comment})

@login_required
def add_attachment(request, bug_id):
    """Add an attachment to a bug."""
    bug = get_object_or_404(Bug, id=bug_id)
    
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            
            attachment = BugAttachment.objects.create(
                bug=bug,
                file=file,
                filename=file.name,
                uploaded_by=request.user
            )
            
            # Create history entry
            BugHistory.objects.create(
                bug=bug,
                user=request.user,
                action=f"Added attachment: {file.name}"
            )
            
            messages.success(request, f'Attachment "{file.name}" has been added.')
        
        return redirect('bugs:bug_detail', bug_id=bug.id)
    
    return render(request, 'bugs/add_attachment.html', {'bug': bug})

@login_required
def delete_attachment(request, bug_id, attachment_id):
    """Delete an attachment."""
    bug = get_object_or_404(Bug, id=bug_id)
    attachment = get_object_or_404(BugAttachment, id=attachment_id, bug=bug)
    
    # Only allow the uploader or admin to delete
    if request.user != attachment.uploaded_by and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this attachment.')
        return redirect('bugs:bug_detail', bug_id=bug.id)
    
    if request.method == 'POST':
        filename = attachment.filename
        attachment.delete()
        
        # Create history entry
        BugHistory.objects.create(
            bug=bug,
            user=request.user,
            action=f"Deleted attachment: {filename}"
        )
        
        messages.success(request, f'Attachment "{filename}" has been deleted.')
        return redirect('bugs:bug_detail', bug_id=bug.id)
    
    return render(request, 'bugs/delete_attachment.html', {'bug': bug, 'attachment': attachment})

@login_required
def search_bugs(request):
    """Search bugs by keyword, project, status, etc."""
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    priority = request.GET.get('priority', '')
    severity = request.GET.get('severity', '')
    project_id = request.GET.get('project', '')
    
    bugs = Bug.objects.all()
    
    # Apply filters if provided
    if query:
        bugs = bugs.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        )
    if status:
        bugs = bugs.filter(status=status)
    if priority:
        bugs = bugs.filter(priority=priority)
    if severity:
        bugs = bugs.filter(severity=severity)
    if project_id:
        bugs = bugs.filter(project_id=project_id)
    
    # Get data for filter dropdowns
    projects = Project.objects.all()
    
    context = {
        'bugs': bugs,
        'projects': projects,
        'query': query,
        'selected_status': status,
        'selected_priority': priority,
        'selected_severity': severity,
        'selected_project': project_id
    }
    
    return render(request, 'bugs/search_bugs.html', context)
