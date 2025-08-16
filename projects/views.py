from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Project, ProjectVersion
from django.utils import timezone

@login_required
def project_list(request):
    """Display list of all projects."""
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
def create_project(request):
    """Create a new project."""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        project = Project.objects.create(
            name=name,
            description=description,
            manager=request.user
        )
        
        # Add creator as member
        project.members.add(request.user)
        
        messages.success(request, f'Project "{name}" has been created.')
        return redirect('projects:project_detail', project_id=project.id)
    
    return render(request, 'projects/create_project.html')

@login_required
def project_detail(request, project_id):
    """Display project details."""
    project = get_object_or_404(Project, id=project_id)
    versions = project.versions.all()
    bugs = project.bugs.all()
    
    context = {
        'project': project,
        'versions': versions,
        'bugs': bugs,
    }
    
    return render(request, 'projects/project_detail.html', context)

@login_required
def edit_project(request, project_id):
    """Edit project details."""
    project = get_object_or_404(Project, id=project_id)
    
    # Ensure user has permission to edit (manager or admin)
    if request.user != project.manager and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this project.')
        return redirect('projects:project_detail', project_id=project.id)
    
    if request.method == 'POST':
        project.name = request.POST.get('name', project.name)
        project.description = request.POST.get('description', project.description)
        
        # Handle end date if provided
        end_date = request.POST.get('end_date')
        if end_date:
            project.end_date = end_date
        
        project.save()
        messages.success(request, f'Project "{project.name}" has been updated.')
        return redirect('projects:project_detail', project_id=project.id)
    
    return render(request, 'projects/edit_project.html', {'project': project})

@login_required
def delete_project(request, project_id):
    """Delete a project."""
    project = get_object_or_404(Project, id=project_id)
    
    # Ensure user has permission to delete (manager or admin)
    if request.user != project.manager and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this project.')
        return redirect('projects:project_detail', project_id=project.id)
    
    if request.method == 'POST':
        project_name = project.name
        project.delete()
        messages.success(request, f'Project "{project_name}" has been deleted.')
        return redirect('projects:project_list')
    
    return render(request, 'projects/delete_project.html', {'project': project})

@login_required
def version_list(request, project_id):
    """Display list of all versions for a project."""
    project = get_object_or_404(Project, id=project_id)
    versions = project.versions.all()
    
    return render(request, 'projects/version_list.html', {
        'project': project,
        'versions': versions
    })

@login_required
def create_version(request, project_id):
    """Create a new version for a project."""
    project = get_object_or_404(Project, id=project_id)
    
    # Ensure user has permission (manager or admin)
    if request.user != project.manager and not request.user.is_staff:
        messages.error(request, 'You do not have permission to add versions to this project.')
        return redirect('projects:project_detail', project_id=project.id)
    
    if request.method == 'POST':
        version_number = request.POST.get('version_number')
        release_date = request.POST.get('release_date', timezone.now().date())
        notes = request.POST.get('notes', '')
        
        ProjectVersion.objects.create(
            project=project,
            version_number=version_number,
            release_date=release_date,
            notes=notes
        )
        
        messages.success(request, f'Version {version_number} has been created.')
        return redirect('projects:version_list', project_id=project.id)
    
    return render(request, 'projects/create_version.html', {'project': project})

@login_required
def version_detail(request, project_id, version_id):
    """Display version details."""
    project = get_object_or_404(Project, id=project_id)
    version = get_object_or_404(ProjectVersion, id=version_id, project=project)
    bugs = version.bugs.all()
    
    return render(request, 'projects/version_detail.html', {
        'project': project,
        'version': version,
        'bugs': bugs
    })

@login_required
def edit_version(request, project_id, version_id):
    """Edit version details."""
    project = get_object_or_404(Project, id=project_id)
    version = get_object_or_404(ProjectVersion, id=version_id, project=project)
    
    # Ensure user has permission (manager or admin)
    if request.user != project.manager and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit versions for this project.')
        return redirect('projects:version_detail', project_id=project.id, version_id=version.id)
    
    if request.method == 'POST':
        version.version_number = request.POST.get('version_number', version.version_number)
        version.release_date = request.POST.get('release_date', version.release_date)
        version.notes = request.POST.get('notes', version.notes)
        version.save()
        
        messages.success(request, f'Version {version.version_number} has been updated.')
        return redirect('projects:version_detail', project_id=project.id, version_id=version.id)
    
    return render(request, 'projects/edit_version.html', {
        'project': project,
        'version': version
    })

@login_required
def delete_version(request, project_id, version_id):
    """Delete a version."""
    project = get_object_or_404(Project, id=project_id)
    version = get_object_or_404(ProjectVersion, id=version_id, project=project)
    
    # Ensure user has permission (manager or admin)
    if request.user != project.manager and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete versions from this project.')
        return redirect('projects:version_detail', project_id=project.id, version_id=version.id)
    
    if request.method == 'POST':
        version_number = version.version_number
        version.delete()
        messages.success(request, f'Version {version_number} has been deleted.')
        return redirect('projects:version_list', project_id=project.id)
    
    return render(request, 'projects/delete_version.html', {
        'project': project,
        'version': version
    })

@login_required
def manage_members(request, project_id):
    """Manage project members."""
    project = get_object_or_404(Project, id=project_id)
    
    # Ensure user has permission (manager or admin)
    if request.user != project.manager and not request.user.is_staff:
        messages.error(request, 'You do not have permission to manage members for this project.')
        return redirect('projects:project_detail', project_id=project.id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        
        if user_id:
            user = get_object_or_404(User, id=user_id)
            
            if action == 'add':
                project.members.add(user)
                messages.success(request, f'{user.username} has been added to the project.')
            elif action == 'remove':
                # Prevent removing the manager from members
                if user == project.manager:
                    messages.error(request, 'Cannot remove the project manager from members.')
                else:
                    project.members.remove(user)
                    messages.success(request, f'{user.username} has been removed from the project.')
        
        return redirect('projects:manage_members', project_id=project.id)
    
    # Get all users that are not already members
    current_members = project.members.all()
    available_users = User.objects.exclude(id__in=current_members.values_list('id', flat=True))
    
    return render(request, 'projects/manage_members.html', {
        'project': project,
        'current_members': current_members,
        'available_users': available_users
    })
