from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AIAnalysisRequest
import json

@login_required
def analysis_home(request):
    """Home page for AI code analysis feature."""
    # Get user's recent analyses
    recent_analyses = AIAnalysisRequest.objects.filter(
        submitted_by=request.user
    ).order_by('-submitted_at')[:5]
    
    return render(request, 'ai_debugger/home.html', {
        'recent_analyses': recent_analyses
    })

@login_required
def submit_analysis(request):
    """Submit code for AI analysis."""
    if request.method == 'POST':
        code = request.POST.get('code')
        language = request.POST.get('language')
        
        if not code:
            messages.error(request, 'Please provide code to analyze.')
            return redirect('ai_debugger:submit_analysis')
        
        # Create analysis request
        analysis = AIAnalysisRequest.objects.create(
            code=code,
            language=language,
            submitted_by=request.user,
            status='pending'
        )
        
        # In a real application, you would trigger the AI analysis here
        # For demonstration, we'll just update the status
        
        # Simulate AI processing
        analysis.status = 'processing'
        analysis.save()
        
        # For demo purposes, let's provide some mock results
        mock_results = {
            'issues': [
                {
                    'type': 'bug',
                    'line': 10,
                    'description': 'Potential null reference exception',
                    'severity': 'high',
                    'suggestion': 'Add null check before accessing this property'
                },
                {
                    'type': 'improvement',
                    'line': 15,
                    'description': 'Inefficient algorithm detected',
                    'severity': 'medium',
                    'suggestion': 'Consider using a hash map for better performance'
                }
            ],
            'summary': 'The code has 1 potential bug and 1 performance issue.',
            'quality_score': 75
        }
        
        # Save mock results
        analysis.results = json.dumps(mock_results)
        analysis.status = 'completed'
        analysis.save()
        
        messages.success(request, 'Your code has been submitted for analysis.')
        return redirect('ai_debugger:analysis_results', analysis_id=analysis.id)
    
    return render(request, 'ai_debugger/submit_analysis.html')

@login_required
def analysis_history(request):
    """View history of all analyses performed by the user."""
    analyses = AIAnalysisRequest.objects.filter(
        submitted_by=request.user
    ).order_by('-submitted_at')
    
    return render(request, 'ai_debugger/analysis_history.html', {
        'analyses': analyses
    })

@login_required
def analysis_results(request, analysis_id):
    """View the results of a specific analysis."""
    analysis = get_object_or_404(AIAnalysisRequest, id=analysis_id)
    
    # Ensure user has permission to view this analysis
    if analysis.submitted_by != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to view this analysis.')
        return redirect('ai_debugger:analysis_home')
    
    # Parse the results from JSON if available
    results = None
    if analysis.results:
        try:
            results = json.loads(analysis.results)
        except json.JSONDecodeError:
            results = None
    
    return render(request, 'ai_debugger/analysis_results.html', {
        'analysis': analysis,
        'results': results
    })
