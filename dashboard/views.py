from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from bugs.models import Bug, BugHistory
from projects.models import Project
from django.db.models import Count, Case, When, IntegerField, Q

@login_required
def dashboard(request):
    """Main dashboard view."""
    # Get bugs assigned to the user
    assigned_bugs = Bug.objects.filter(assigned_to=request.user).order_by('-updated_at')[:5]
    
    # Get projects the user is a member of
    user_projects = Project.objects.filter(members=request.user)
    
    # Get recent bug activity across all projects
    recent_activity = BugHistory.objects.order_by('-timestamp')[:10]
    
    # Get bug statistics for projects the user is involved with
    project_stats = []
    for project in user_projects:
        bugs = Bug.objects.filter(project=project)
        stats = {
            'project': project,
            'total_bugs': bugs.count(),
            'open_bugs': bugs.filter(status='open').count(),
            'in_progress_bugs': bugs.filter(status='in_progress').count(),
            'resolved_bugs': bugs.filter(status='resolved').count(),
            'closed_bugs': bugs.filter(status='closed').count(),
        }
        project_stats.append(stats)
    
    context = {
        'assigned_bugs': assigned_bugs,
        'user_projects': user_projects,
        'recent_activity': recent_activity,
        'project_stats': project_stats
    }
    
    return render(request, 'dashboard/index.html', context)

@login_required
def my_bugs(request):
    """Display bugs reported by or assigned to the user."""
    reported_bugs = Bug.objects.filter(reported_by=request.user).order_by('-created_at')
    assigned_bugs = Bug.objects.filter(assigned_to=request.user).order_by('-updated_at')
    
    context = {
        'reported_bugs': reported_bugs,
        'assigned_bugs': assigned_bugs
    }
    
    return render(request, 'dashboard/my_bugs.html', context)

@login_required
def my_projects(request):
    """Display projects the user is involved with."""
    managed_projects = Project.objects.filter(manager=request.user)
    member_projects = Project.objects.filter(members=request.user).exclude(manager=request.user)
    
    context = {
        'managed_projects': managed_projects,
        'member_projects': member_projects
    }
    
    return render(request, 'dashboard/my_projects.html', context)

@login_required
def recent_activity(request):
    """Display recent activity across the system."""
    # Get bugs recently modified
    recent_bugs = Bug.objects.order_by('-updated_at')[:20]
    
    # Get recent bug history entries
    bug_history = BugHistory.objects.order_by('-timestamp')[:50]
    
    context = {
        'recent_bugs': recent_bugs,
        'bug_history': bug_history
    }
    
    return render(request, 'dashboard/recent_activity.html', context)

@login_required
def statistics(request):
    """Display system-wide statistics."""
    # Get total counts
    total_projects = Project.objects.count()
    total_bugs = Bug.objects.count()
    
    # Get bug status distribution
    bug_status_counts = Bug.objects.values('status').annotate(count=Count('status'))
    
    # Get bug priority distribution
    bug_priority_counts = Bug.objects.values('priority').annotate(count=Count('priority'))
    
    # Get bug severity distribution
    bug_severity_counts = Bug.objects.values('severity').annotate(count=Count('severity'))
    
    # Get projects with most bugs
    project_bug_counts = Project.objects.annotate(bug_count=Count('bugs')).order_by('-bug_count')[:10]
    
    # Get bugs by month (for charts)
    bug_by_month = Bug.objects.extra(select={'month': "EXTRACT(month FROM created_at)"}).values('month').annotate(count=Count('id')).order_by('month')
    
    context = {
        'total_projects': total_projects,
        'total_bugs': total_bugs,
        'bug_status_counts': bug_status_counts,
        'bug_priority_counts': bug_priority_counts,
        'bug_severity_counts': bug_severity_counts,
        'project_bug_counts': project_bug_counts,
        'bug_by_month': bug_by_month
    }
    
    return render(request, 'dashboard/statistics.html', context)
